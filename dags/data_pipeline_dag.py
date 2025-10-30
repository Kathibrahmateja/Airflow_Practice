"""
Data Pipeline DAG for processing city weather data.
This DAG performs the following tasks:
1. Loads city data from cities.csv
2. Retrieves weather data from OpenWeatherMap API
3. Merges the city and weather data
4. Loads the merged data into a PostgreSQL database
5. Performs cleanup operations
6. Sends email notification about job status
"""

from datetime import datetime, timedelta

from sqlalchemy import create_engine, text
import urllib.parse
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import snowflake.connector
import pandas as pd
import requests
import os
from pathlib import Path
import logging
from typing import Dict, List

# Constants
CITIES_FILE = str(Path(__file__).resolve().parent.joinpath('cities.csv'))
WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
WEATHER_API_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
EMAIL_RECIPIENT = <email_name>

def load_cities_data(**context) -> None:
    """
    Load city data from CSV file and push to XCom.
    """
    try:
        # Resolve and log the path used to load the cities file (helps debugging inside containers)
        cities_path = Path(CITIES_FILE)
        logging.info(f"Looking for cities file at: {cities_path}")
        if not cities_path.exists():
            # List files in the DAGs directory to help troubleshoot mounting issues
            dag_dir = cities_path.parent
            listing = [p.name for p in dag_dir.iterdir()] if dag_dir.exists() else []
            logging.error(f"cities.csv not found at {cities_path}. Files in {dag_dir}: {listing}")
            raise FileNotFoundError(f"cities.csv not found at {cities_path}")

        df = pd.read_csv(cities_path)
        # Convert DataFrame to list of dictionaries for easier XCom passing
        cities_data = df.to_dict('records')
        context['task_instance'].xcom_push(key='cities_data', value=cities_data)
        logging.info(f"Successfully loaded {len(cities_data)} cities")
    except Exception as e:
        logging.error(f"Error loading cities data: {str(e)}")
        raise

def get_weather_data(**context) -> None:
    """
    Retrieve weather data from OpenWeatherMap API for each city.
    """
    cities_data = context['task_instance'].xcom_pull(key='cities_data', task_ids='load_cities')
    weather_data = []

    for city in cities_data:
        try:
            params = {
                'q': f"{city['city']},{city['country']}",
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(WEATHER_API_BASE_URL, params=params)
            response.raise_for_status()
            
            weather = response.json()
            weather_data.append({
                'city': city['city'],
                'temperature': weather['main']['temp'],
                'weather_description': weather['weather'][0]['description']
            })
            logging.info(f"Retrieved weather data for {city['city']}")
            
        except requests.RequestException as e:
            logging.error(f"Error fetching weather data for {city['city']}: {str(e)}")
            continue

    context['task_instance'].xcom_push(key='weather_data', value=weather_data)

def merge_data(**context) -> None:
    """
    Merge city and weather data.
    """
    try:
        ti = context['task_instance']
        cities_data = ti.xcom_pull(key='cities_data', task_ids='load_cities')
        weather_data = ti.xcom_pull(key='weather_data', task_ids='get_weather')

        if not cities_data:
            logging.error('No cities data found in XCom (key="cities_data"). Aborting merge.')
            raise ValueError('cities_data is empty or missing')

        # Ensure weather_data is a list (may be None if get_weather failed)
        if weather_data is None:
            logging.warning('No weather data found in XCom (key="weather_data"). Proceeding with empty weather set.')
            weather_data = []

        cities_df = pd.DataFrame(cities_data)
        weather_df = pd.DataFrame(weather_data)

        # Defensive: ensure both DataFrames have a 'city' column
        if 'city' not in cities_df.columns:
            logging.error(f"'city' column missing from cities_df. Columns: {list(cities_df.columns)}")
            raise KeyError("'city' column missing from cities data")

        if weather_df.empty:
            # Create empty weather_df with expected columns so merge won't fail
            weather_df = pd.DataFrame(columns=['city', 'temperature', 'weather_description'])
        elif 'city' not in weather_df.columns:
            logging.error(f"'city' column missing from weather_df. Columns: {list(weather_df.columns)}")
            # Attempt best-effort: if weather entries have a different city key, try to normalize
            # (common cases: 'name' or 'city_name')
            for alt in ('name', 'city_name'):
                if alt in weather_df.columns:
                    weather_df = weather_df.rename(columns={alt: 'city'})
                    logging.info(f"Renamed weather_df column '{alt}' to 'city'")
                    break
            else:
                raise KeyError("'city' column missing from weather data")

        merged_df = pd.merge(cities_df, weather_df, on='city', how='left')
        merged_data = merged_df.to_dict('records')

        ti.xcom_push(key='merged_data', value=merged_data)
        logging.info(f"Successfully merged city and weather data: {len(merged_data)} records")
    except Exception as e:
        logging.error(f"Error merging data: {str(e)}")
        raise

def load_to_database(**context) -> None:
    """
    Load merged data into PostgreSQL database.
    """
    try:
        merged_data = context['task_instance'].xcom_pull(key='merged_data', task_ids='merge_data')
        df = pd.DataFrame(merged_data)
        
        # Prefer environment variables for credentials; fall back to literals (not recommended for prod)
        user = os.getenv('SNOWFLAKE_USER', 'bkatti')
        password = os.getenv('SNOWFLAKE_PASSWORD', 'Divya558!@#$%^')
        account = os.getenv('SNOWFLAKE_ACCOUNT', 'RLUVVNN-FQ05221')
        warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        database = os.getenv('SNOWFLAKE_DATABASE', 'PRACTICE')
        schema = os.getenv('SNOWFLAKE_SCHEMA', 'TEST')

        # URL-encode credentials (password may contain characters like #, %, etc.)
        password_quoted = urllib.parse.quote_plus(password)

        # Create Snowflake SQLAlchemy engine (ensure password is URL-encoded so parsing doesn't break)
        engine = create_engine(
            f'snowflake://{user}:{password_quoted}@{account}/{database}/{schema}?warehouse={warehouse}'
        )
        
        # Create table if it doesn't exist
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS city_weather (
            city VARCHAR(100),
            country VARCHAR(2),
            population INTEGER,
            temperature FLOAT,
            weather_description VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        with engine.connect() as conn:
            result = conn.execute(text(create_table_sql))
            logging.info("Ensured city_weather table exists")

        df.to_sql(
            'city_weather',              # Target table name
            con=engine,              # SQLAlchemy connection
            if_exists='append',     # Options: 'fail', 'replace', 'append'
            index=False              # Don’t include DataFrame index
        )
        
        logging.info(f"Successfully loaded {len(df)} records into database")
    except Exception as e:
        logging.error(f"Error loading data to database: {str(e)}")
        raise

def cleanup(**context) -> None:
    """
    Perform cleanup operations.
    """
    try:
        # Clear XCom variables
        task_instance = context['task_instance']
        task_instance.xcom_push(key='cities_data', value=None)
        task_instance.xcom_push(key='weather_data', value=None)
        task_instance.xcom_push(key='merged_data', value=None)
        logging.info("Cleanup completed successfully")
    except Exception as e:
        logging.error(f"Error during cleanup: {str(e)}")
        raise

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [EMAIL_RECIPIENT],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    'city_weather_pipeline',
    default_args=default_args,
    description='A DAG to process city weather data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 10, 30),
    catchup=False,
    tags=['weather', 'api', 'cities'],
) as dag:

    # Task 1: Load cities data
    load_cities = PythonOperator(
        task_id='load_cities',
        python_callable=load_cities_data,
    )

    # Task 2: Get weather data
    get_weather = PythonOperator(
        task_id='get_weather',
        python_callable=get_weather_data,
    )

    # Task 3: Merge data
    merge_data_task = PythonOperator(
        task_id='merge_data',
        python_callable=merge_data,
    )

    # Task 4: Load to database
    load_to_db = PythonOperator(
        task_id='load_to_database',
        python_callable=load_to_database,
    )

    # Task 5: Cleanup
    cleanup_task = PythonOperator(
        task_id='cleanup',
        python_callable=cleanup,
    )

    # Task 6: Send email notification
    email_notification = EmailOperator(
        task_id='send_email',
        to=EMAIL_RECIPIENT,
        subject='City Weather Pipeline Status',
        html_content='The city weather pipeline has completed successfully!',
    )

    # Define task dependencies
    load_cities >> get_weather >> merge_data_task >> load_to_db >> cleanup_task >> email_notification