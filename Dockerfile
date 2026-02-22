FROM apache/airflow:2.7.1

USER root

# Install Microsoft ODBC Driver dependencies
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    # Install system packages required for ODBC and building some DB drivers
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
       build-essential gcc g++ python3-dev freetds-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Pre-install setuptools and upgrade setuptools_scm to avoid conflicts
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir "setuptools_scm>=9.0"

# Install Airflow providers and required packages (avoid pymssql which has build conflicts; use pyodbc + ODBC driver instead)
RUN pip install --no-cache-dir \
    pyodbc \
    snowflake-sqlalchemy \
    apache-airflow-providers-common-sql