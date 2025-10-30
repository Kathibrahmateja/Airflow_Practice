# Airflow Data Engineering Challenge

This repository contains a solution for the Data Engineering coding challenge, implementing an Apache Airflow DAG that processes city weather data.

## Project Structure

- `dags/`
  - `data_pipeline_dag.py`: Main DAG file implementing the data pipeline
  - `cities.csv`: Sample input data with city information

## Prerequisites

- Docker and Docker Compose
- OpenWeatherMap API key
- Email account for notifications

## Setup Instructions

1. Clone this repository:
```bash
git clone https://github.com/Kathibrahmateja/Airflow_Practice.git
cd Airflow_Practice
```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the following variables in `.env`:
     - `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
     - `EMAIL_RECIPIENT`: Your email for notifications
     - SMTP settings for email notifications

3. Start Airflow services:
```bash
docker-compose up -d
```

4. Access Airflow web interface:
- URL: http://localhost:8081
- Username: airflow
- Password: airflow

## DAG Details

The `city_weather_pipeline` DAG performs the following tasks:

1. Loads city data from `cities.csv`
2. Retrieves weather data from OpenWeatherMap API
3. Merges the city and weather data
4. Loads the data into SQL Server tables (cities, weather, and city_weather)
5. Performs cleanup operations
6. Sends an email notification

Schedule: Daily at midnight

## Testing

To test the DAG:

1. Ensure Airflow is running
2. Navigate to the Airflow UI
3. Enable the `city_weather_pipeline` DAG
4. Trigger the DAG manually or wait for the scheduled run

## Stopping Airflow

To stop all Airflow services:
```bash
docker-compose down
```

To stop and delete volumes:
```bash
docker-compose down -v
```

This repository contains an Apache Airflow setup using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. Clone this repository:
```bash
git clone https://github.com/Kathibrahmateja/Airflow_Practice.git
cd Airflow_Practice
```

2. Start the Airflow services:
```bash
docker-compose up -d
```

3. Access the Airflow web interface:
- URL: http://localhost:8080
- Username: airflow
- Password: airflow

## Project Structure

- `dags/`: Place your DAG files here
- `logs/`: Contains Airflow task logs
- `plugins/`: Place custom Airflow plugins here

## Stopping Airflow

To stop all Airflow services:
```bash
docker-compose down
```

To stop and delete volumes (this will delete the database):
```bash
docker-compose down -v
```