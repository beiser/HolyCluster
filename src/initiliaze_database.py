from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from settings import (
    PSQL_USERNAME,
    PSQL_PASSWORD,
)

# Define the database configuration
DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': PSQL_USERNAME,
    'password': PSQL_PASSWORD,
    'database': 'postgres'  # Connect to the default 'postgres' database to create a new one
}

# Create the engine to connect to the PostgreSQL server
engine = create_engine(URL(**DATABASE))

# The name of the new database you want to create
new_database_name = 'holly_cluster'

# Connect to the PostgreSQL server and create the new database
with engine.connect() as connection:
    connection.execute(f"CREATE DATABASE {new_database_name}")

print(f"Database '{new_database_name}' created successfully.")
