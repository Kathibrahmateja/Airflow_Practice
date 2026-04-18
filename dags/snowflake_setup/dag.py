"""
DAG to create and test Snowflake connection from credentials JSON file.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pathlib import Path
import logging
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# Import utilities from include
from include.utils.snowflake_connection import create_snowflake_connection, load_snowflake_credentials


def setup_snowflake_connection_task(**context):
    """
    Task to create Snowflake connection in Airflow.
    """
    try:
        logging.info("Starting Snowflake connection setup...")
        create_snowflake_connection('snowflake_default')
        logging.info("Snowflake connection created successfully in Airflow")
        context['task_instance'].xcom_push(key='setup_status', value='SUCCESS')
    except Exception as e:
        logging.error(f"Failed to create Snowflake connection: {str(e)}")
        context['task_instance'].xcom_push(key='setup_status', value='FAILED')
        raise


def test_snowflake_connection(**context):
    """
    Task to test Snowflake connection.
    Tests if the connection was created successfully in Airflow.
    """
    try:
        from airflow.models import Connection
        from airflow import settings
        
        session = settings.Session()
        conn = session.query(Connection).filter(Connection.conn_id == 'snowflake_default').first()
        
        if not conn:
            logging.warning("Connection 'snowflake_default' not found in Airflow")
            context['task_instance'].xcom_push(key='connection_status', value='NOT_FOUND')
            return
        
        # Display connection details
        logging.info(f"Connection ID: {conn.conn_id}")
        logging.info(f"Connection Type: {conn.conn_type}")
        logging.info(f"Host: {conn.host}")
        logging.info(f"Schema: {conn.schema}")
        logging.info(f"Extra: {conn.extra}")
        
        # Actual connection test (optional - may fail if Snowflake credentials are invalid)
        try:
            from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
            hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
            snowflake_conn = hook.get_conn()
            
            cursor = snowflake_conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            logging.info(f"Snowflake connection test successful! Result: {result}")
            context['task_instance'].xcom_push(key='connection_status', value='SUCCESS')
            
        except Exception as e:
            # Snowflake test failed - but connection was created in Airflow
            logging.warning(f"Snowflake test query failed (may be due to invalid credentials): {str(e)}")
            context['task_instance'].xcom_push(key='connection_status', value='CREATED_BUT_INVALID_CREDS')
        
    except Exception as e:
        logging.error(f"Failed to verify Snowflake connection: {str(e)}")
        context['task_instance'].xcom_push(key='connection_status', value='ERROR')
        raise


def display_credentials_info(**context):
    """
    Task to display loaded credentials info (for verification).
    """
    try:
        project_root = Path(__file__).resolve().parent.parent.parent
        config_dir = project_root / 'config'
        creds_file = config_dir / 'snowflake_credentials.json'
        
        logging.info(f"Loading credentials from: {creds_file}")
        creds = load_snowflake_credentials(str(creds_file))
        
        # Mask password for security
        masked_password = creds.get('password', 'NOT SET')
        if masked_password and len(masked_password) > 4:
            masked_password = masked_password[:2] + '***' + masked_password[-2:]
        
        info = {
            'account': creds.get('account', 'NOT SET'),
            'user': creds.get('user', 'NOT SET'),
            'password': masked_password,
            'warehouse': creds.get('warehouse', 'NOT SET'),
            'database': creds.get('database', 'NOT SET'),
            'schema': creds.get('schema', 'NOT SET'),
            'role': creds.get('role', 'NOT SET')
        }
        
        logging.info(f"Snowflake Credentials Loaded: {info}")
        context['task_instance'].xcom_push(key='creds_info', value=info)
        
    except Exception as e:
        logging.error(f"Failed to load credentials: {str(e)}")
        raise


# DAG configuration
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'snowflake_connection_setup',
    default_args=default_args,
    description='Create and test Snowflake connection from JSON credentials',
    schedule='@once',
    catchup=False,
    tags=['snowflake', 'setup']
)

# Tasks
info_task = PythonOperator(
    task_id='display_credentials_info',
    python_callable=display_credentials_info,
    dag=dag
)

setup_task = PythonOperator(
    task_id='setup_snowflake_connection',
    python_callable=setup_snowflake_connection_task,
    dag=dag
)

test_task = PythonOperator(
    task_id='test_snowflake_connection',
    python_callable=test_snowflake_connection,
    dag=dag
)

# Dependencies
info_task >> setup_task >> test_task
