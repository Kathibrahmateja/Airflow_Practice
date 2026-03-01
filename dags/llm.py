from pyspark.sql import SparkSession
import os
import warnings
import logging


# Suppress Hadoop/Spark initialization warnings (safe to ignore on Windows)
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger('py4j').setLevel(logging.ERROR)
logging.getLogger('pyspark').setLevel(logging.ERROR)



spark = SparkSession.builder.appName("LLM").getOrCreate()

# Build correct path to cities.csv relative to DAG directory
dag_dir = os.path.dirname(os.path.abspath(__file__))
dag_dir = os.path.dirname(dag_dir)+"\source" # Move up from 'dags' to project root
csv_path = os.path.join(dag_dir, "cities.csv")

# Read CSV file
if os.path.exists(csv_path):
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    print(f"✓ Successfully loaded cities.csv from {csv_path}")
    print(f"  Total rows: {df.count()}")
    print("\nData preview:")
    df.show(10)
else:
    print(f"✗ Error: cities.csv not found at {csv_path}")
    print(f"  Available files in {dag_dir}:")
    for f in os.listdir(dag_dir):
        print(f"    - {f}")