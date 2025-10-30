## SQL Server Connection Setup

After starting the services, you need to configure the SQL Server connection in Airflow:

1. Open the Airflow web interface (http://localhost:8081)
2. Navigate to Admin > Connections
3. Click the + sign to add a new connection
4. Fill in the following details:
   - Connection Id: `mssql_default`
   - Connection Type: Microsoft SQL Server
   - Host: `mssql`
   - Schema: `airflow`
   - Login: `sa`
   - Password: `Airflow123!`
   - Port: `1433`
   - Extra: `{"driver": "ODBC Driver 17 for SQL Server"}`

## Email Notifications Setup

1. Update the `.env` file with your email settings:
```bash
AIRFLOW_SMTP_USER=your-email@gmail.com
AIRFLOW_SMTP_PASSWORD=your-app-specific-password  # Generate from Google Account
AIRFLOW_SMTP_MAIL_FROM=your-email@gmail.com
```

2. For Gmail:
   - Go to your Google Account settings
   - Enable 2-Step Verification
   - Generate an App Password for use with Airflow
   - Use this App Password in the .env file

## Database Schema

The DAG creates and maintains three tables:

1. `cities`:
   - `city` (VARCHAR(100), PRIMARY KEY)
   - `country` (VARCHAR(2))
   - `population` (INTEGER)

2. `weather`:
   - `city` (VARCHAR(100), PRIMARY KEY)
   - `temperature` (FLOAT)
   - `weather_description` (VARCHAR(100))
   - `created_at` (DATETIME)

3. `city_weather`:
   - `city` (VARCHAR(100), PRIMARY KEY)
   - `country` (VARCHAR(2))
   - `population` (INTEGER)
   - `temperature` (FLOAT)
   - `weather_description` (VARCHAR(100))
   - `created_at` (DATETIME)