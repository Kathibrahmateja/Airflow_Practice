"""Data loading utilities for Airflow workflows."""
from pyspark.sql import SparkSession
import os
import warnings
import logging


# Suppress Hadoop/Spark initialization warnings (safe to ignore on Windows)
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger('py4j').setLevel(logging.ERROR)
logging.getLogger('pyspark').setLevel(logging.ERROR)


def load_csv_with_spark(csv_path: str, app_name: str = "DataLoader") -> 'DataFrame':
    """
    Load CSV file using PySpark.
    
    Args:
        csv_path: Path to the CSV file
        app_name: Spark application name
        
    Returns:
        PySpark DataFrame
    """
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    
    if os.path.exists(csv_path):
        df = spark.read.csv(csv_path, header=True, inferSchema=True)
        print(f"✓ Successfully loaded {csv_path}")
        print(f"  Total rows: {df.count()}")
        return df
    else:
        print(f"✗ Error: File not found at {csv_path}")
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
