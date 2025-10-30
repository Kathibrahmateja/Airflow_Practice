FROM apache/airflow:2.7.1

USER root

# Install Microsoft ODBC Driver dependencies
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Airflow providers and required packages
RUN pip install --no-cache-dir \
    apache-airflow-providers-microsoft-mssql \
    pyodbc