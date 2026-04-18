# Airflow Practice Project

An Apache Airflow project demonstrating best practices for data pipeline orchestration, including weather data processing, Snowflake integration, and expense tracking.

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Available DAGs](#-available-dags)
- [Configuration](#-configuration)
- [Docker Setup](#-docker-setup)

## 📁 Project Structure

```
airflow_practice/
├── dags/                          # DAG definitions organized by purpose
│   ├── weather_pipeline/          # Weather data pipeline
│   ├── snowflake_setup/           # Snowflake connection setup
│   └── simple_tasks/              # Example DAGs
├── include/                        # Shared utilities and data
│   ├── utils/                     # Helper functions
│   ├── data/                      # Data files (cities.csv)
│   └── sqlscripts/                # SQL initialization files
├── config/                         # Configuration files
├── plugins/                        # Custom Airflow extensions
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Custom Airflow image
└── requirements.txt                # Python dependencies
```

👉 See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed structure documentation.

## ✨ Features

- **Weather Pipeline DAG**: Fetch city weather data, merge with city info, and load to Snowflake
- **Snowflake Integration**: Secure connection setup with JSON-based credentials
- **Snowflake Setup DAG**: Create and test Snowflake connections from Airflow UI
- **Simple Examples**: Basic task dependency examples for learning
- **Docker Support**: Complete Docker Compose setup with PostgreSQL and MSSQL
- **Utility Modules**: Reusable components for data loading, connection management, and expense tracking

## 🔧 Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- OpenWeatherMap API key (optional, for weather pipeline)
- Snowflake account (optional, for database integration)

## 🚀 Quick Start

### 1. Initialize Airflow

```bash
cd Airflow_Practice
docker compose up -d
```

This starts:
- Airflow Webserver (http://localhost:8081)
- Airflow Scheduler
- PostgreSQL (metadata database)
- MSSQL (optional data warehouse)

### 2. Access Airflow UI

- **URL**: http://localhost:8081
- **Username**: airflow
- **Password**: airflow

### 3. Configure Snowflake (Optional)

Update credentials in `config/snowflake_credentials.json`:

```json
{
  "snowflake": {
    "user": "your_username",
    "password": "your_password",
    "account": "your_account_id",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema"
  }
}
```

### 4. Trigger a DAG

1. Go to Airflow UI
2. Find a DAG (e.g., `task_dependency`, `snowflake_connection_setup`)
3. Click "Trigger DAG"

## 📊 Available DAGs

### 1. **task_dependency** (Simple Example)
- **Purpose**: Demonstrates basic task dependencies
- **Tasks**: task1 → task2
- **Schedule**: Daily
- **Tags**: examples, simple

### 2. **city_weather_pipeline** (Main Pipeline)
- **Purpose**: Fetch weather data and load to Snowflake
- **Tasks**: 
  - Load cities from CSV
  - Fetch weather from API
  - Merge data
  - Load to Snowflake
  - Cleanup
  - Send notification
- **Schedule**: Daily
- **Tags**: weather, api, cities
- **Requires**: OPENWEATHER_API_KEY, Snowflake credentials

### 3. **snowflake_connection_setup** (Setup)
- **Purpose**: Create and test Snowflake connections
- **Tasks**:
  - Display credentials info
  - Setup Snowflake connection
  - Test connection
- **Schedule**: One-time
- **Tags**: snowflake, setup

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Available variables:
- `AIRFLOW_SMTP_USER` - Email for notifications
- `AIRFLOW_SMTP_PASSWORD` - Email app password
- `OPENWEATHER_API_KEY` - Weather API key
- `SNOWFLAKE_*` - Snowflake credentials

### Snowflake Credentials

**Method 1: JSON File (Recommended)**
- Update `config/snowflake_credentials.json`
- Automatically loaded by utilities

**Method 2: Environment Variables**
- Set `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, etc.
- Used as fallback if JSON credentials don't exist

## 🐳 Docker Setup

### Build Custom Image

```bash
docker compose build
```

### View Logs

```bash
# Scheduler logs
docker compose logs airflow-scheduler

# Webserver logs
docker compose logs airflow-webserver

# All services
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```

### Clean Everything

```bash
docker compose down -v  # includes volumes
```

## 🛠️ Setting Up Snowflake Connection in Airflow

### Option 1: Via Setup DAG (Recommended)

1. Go to Airflow UI
2. Trigger `snowflake_connection_setup` DAG
3. Check DAG logs for status

### Option 2: Via Python Script

```bash
docker compose exec airflow-webserver python /opt/airflow/dags/include/utils/snowflake_connection.py
```

### Option 3: Via Airflow UI

1. Admin → Connections → Create
2. Connection ID: `snowflake_default`
3. Connection Type: `Snowflake`
4. Host: Your Account ID
5. Schema: Your Snowflake schema
6. Extra JSON:
```json
{
  "warehouse": "your_warehouse",
  "role": "your_role"
}
```

## 📚 Utilities

### snowflake_connection.py
- `load_snowflake_credentials()` - Load credentials from JSON
- `create_snowflake_connection()` - Create Airflow connection

### data_loader.py
- `load_csv_with_spark()` - Load CSV files using PySpark

### expense_calculator.py
- `ExpenseCalculator` - Interactive expense tracking with PySpark

## 🔗 Useful Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Snowflake Airflow Provider](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📝 License

This project is provided as-is for educational and practice purposes.

## ✅ Checklist

- [ ] Create `.env` file with your credentials
- [ ] Update `config/snowflake_credentials.json` (if using Snowflake)
- [ ] Run `docker compose up -d` to start services
- [ ] Access Airflow UI at http://localhost:8081
- [ ] Trigger a DAG to test setup
- [ ] Check logs for any errors

---

**Maintained with ❤️ for Airflow learning and practice**
