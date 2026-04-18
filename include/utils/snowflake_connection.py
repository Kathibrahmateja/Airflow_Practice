"""Snowflake connection setup utilities."""
import json
import os
from pathlib import Path
from airflow.models import Connection
from airflow import settings


def load_snowflake_credentials(creds_file: str) -> dict:
    """
    Load Snowflake credentials from JSON file.
    
    Args:
        creds_file: Path to the credentials JSON file
        
    Returns:
        Dictionary containing Snowflake credentials
        
    Raises:
        FileNotFoundError: If credentials file doesn't exist
        json.JSONDecodeError: If JSON is malformed
    """
    creds_path = Path(creds_file)
    
    if not creds_path.exists():
        raise FileNotFoundError(f"Credentials file not found: {creds_file}")
    
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    return creds.get('snowflake', {})


def create_snowflake_connection(conn_id: str = 'snowflake_default'):
    """
    Create or update Snowflake connection in Airflow.
    
    Args:
        conn_id: Connection ID to use (default: 'snowflake_default')
    """
    # Get credentials file path - relative to config directory
    project_root = Path(__file__).resolve().parent.parent.parent
    config_dir = project_root / 'config'
    creds_file = config_dir / 'snowflake_credentials.json'
    
    # Load credentials
    creds = load_snowflake_credentials(str(creds_file))
    
    # Validate required fields
    required_fields = ['user', 'password', 'account']
    missing_fields = [field for field in required_fields if field not in creds]
    if missing_fields:
        raise ValueError(f"Missing required fields in credentials: {missing_fields}")
    
    # Build connection URI
    # Snowflake connection format: snowflake://user:password@account/database/schema
    user = creds['user']
    password = creds['password']
    account = creds['account']
    database = creds.get('database', '')
    schema = creds.get('schema', '')
    
    # URL encode password to handle special characters
    from urllib.parse import quote
    password_encoded = quote(password, safe='')
    
    # Build the connection URI
    conn_uri = f"snowflake://{user}:{password_encoded}@{account}"
    if database:
        conn_uri += f"/{database}"
    if schema:
        conn_uri += f"/{schema}"
    
    # Build extra JSON with all Snowflake connection parameters
    # SnowflakeHook looks for these in the extra field
    extra = {
        "account": creds.get('account', ''),
        "user": creds.get('user', ''),
        "password": creds.get('password', ''),
        "warehouse": creds.get('warehouse', ''),
        "database": creds.get('database', ''),
        "schema": creds.get('schema', ''),
        "role": creds.get('role', '')
    }
    
    # Remove empty values
    extra = {k: v for k, v in extra.items() if v}
    
    # Get or create connection
    session = settings.Session()
    
    # Check if connection already exists
    existing_conn = session.query(Connection).filter(Connection.conn_id == conn_id).first()
    
    if existing_conn:
        # Update existing connection
        existing_conn.conn_type = 'snowflake'
        existing_conn.host = account
        existing_conn.login = user
        existing_conn.password = creds['password']
        existing_conn.schema = database
        existing_conn.extra = json.dumps(extra)
        print(f"Updated existing connection: {conn_id}")
    else:
        # Create new connection
        new_conn = Connection(
            conn_id=conn_id,
            conn_type='snowflake',
            host=account,
            login=user,
            password=creds['password'],
            schema=database,
            extra=json.dumps(extra)
        )
        session.add(new_conn)
        print(f"Created new connection: {conn_id}")
    
    session.commit()
    session.close()
    print(f"Snowflake connection '{conn_id}' successfully configured!")
    print(f"Connection details - Account: {account}, User: {user}, DB: {database}, Schema: {schema}")


if __name__ == '__main__':
    create_snowflake_connection('snowflake_default')
