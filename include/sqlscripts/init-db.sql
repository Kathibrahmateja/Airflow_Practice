-- Create Airflow database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'airflow')
BEGIN
    CREATE DATABASE airflow;
END
GO

-- Use the airflow database
USE airflow;
GO

-- Verify the database is ready
SELECT 'Airflow database is ready' AS status;
