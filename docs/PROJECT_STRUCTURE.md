# Airflow Practice - Project Structure

This document describes the Airflow project structure and organization following Apache Airflow best practices.

## Directory Structure

```
airflow_practice/
├── dags/                          # DAG files organized by purpose
│   ├── weather_pipeline/          # Weather data pipeline DAG package
│   │   ├── __init__.py
│   │   └── dag.py                 # Main DAG definition
│   ├── snowflake_setup/           # Snowflake connection setup DAG package
│   │   ├── __init__.py
│   │   └── dag.py                 # Setup and test tasks
│   └── simple_tasks/              # Simple example DAG package
│       ├── __init__.py
│       └── dag.py                 # Basic task dependency example
│
├── include/                        # Helper modules, utilities, and data
│   ├── __init__.py
│   ├── utils/                     # Utility functions and helper modules
│   │   ├── __init__.py
│   │   ├── snowflake_connection.py  # Snowflake connection utilities
│   │   ├── expense_calculator.py    # Expense tracker utility
│   │   └── data_loader.py           # Data loading utilities
│   ├── data/                      # Shared data files
│   │   └── cities.csv             # Sample city data
│   └── sqlscripts/                # SQL initialization scripts
│       └── init-db.sql            # Database initialization
│
├── plugins/                        # Custom Airflow plugins
│   └── (empty - for future custom operators/sensors)
│
├── config/                         # Configuration files
│   └── snowflake_credentials.json  # Snowflake connection credentials
│
├── logs/                           # Airflow logs directory (created at runtime)
│
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Custom Airflow Docker image
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project README
└── docs/                           # Documentation
    └── setup.md                    # Setup guide
```

## Key Points

### DAGs Organization
- Each DAG is organized in its own subdirectory as a Python package
- Each package contains an `__init__.py` and `dag.py` file
- This structure makes DAGs more maintainable and scalable

### Include Directory
- **utils/**: Reusable utility functions and helper modules
- **data/**: Shared data files accessible to all DAGs
- **sqlscripts/**: SQL scripts for database initialization

### Configuration
- Credentials stored in `config/` directory as JSON
- Loaded and used by utilities at runtime
- Never hardcode secrets - use environment variables or JSON credentials

### Docker Setup
- Custom Dockerfile extends Apache Airflow base image
- Installs additional dependencies (pyodbc, Snowflake connectors)
- Uses docker-compose for local development

## Running DAGs

1. **Initialize Airflow**:
   ```bash
   docker compose up -d
   ```

2. **Access Airflow UI**:
   - URL: http://localhost:8081
   - Username: airflow
   - Password: airflow

3. **Set Snowflake Credentials**:
   - Update `config/snowflake_credentials.json` with your details
   - Run snowflake_connection_setup DAG from the UI

4. **Trigger DAGs**:
   - Use Airflow UI to trigger DAGs manually or configure schedules

## Best Practices Applied

✓ DAGs organized in subdirectories  
✓ Separate utilities and configuration from DAGs  
✓ Credentials managed externally (not hardcoded)  
✓ Clear file naming and structure  
✓ Modular, reusable components  
✓ Environment-based configuration  
✓ Docker containerization for consistency  
