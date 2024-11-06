import os
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

# Database connection parameters from environment variables
DB_PARAMS = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Create connection string
connection_string = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"

# Create engine
engine = create_engine(connection_string)

# Get the path to raw_data directory
dbt_project_path = Path("/usr/app/dbt_project")
raw_data_path = dbt_project_path / "database" / "raw_data"

# Load and insert data
try:
    # Load data from CSV files
    customers_df = pd.read_csv(raw_data_path / "customers.csv")
    orders_df = pd.read_csv(raw_data_path / "orders.csv")
    state_df = pd.read_csv(raw_data_path / "state.csv")

    # Insert data into PostgreSQL
    customers_df.to_sql("customers", engine, if_exists="replace", index=False)
    orders_df.to_sql("orders", engine, if_exists="replace", index=False)
    state_df.to_sql("state", engine, if_exists="replace", index=False)

    print("Data inserted successfully!")

except Exception as e:
    print(f"Error: {e}")
