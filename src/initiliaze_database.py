from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError

from settings import (
    PSQL_USERNAME,
    PSQL_PASSWORD,
)

def db_details():
    user = PSQL_USERNAME
    password =PSQL_PASSWORD
    host = 'localhost'
    port = '5432'
    database = 'postgres'  # Connect to the default 'postgres' database

    return user, password, host, port, database


def check_database_exists(connection, db_name):
    result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
    return result.scalar() is not None


def drop_database_if_exists(connection, db_name):
    if check_database_exists(connection=connection, db_name=db_name):
        connection.execute(text(f'DROP DATABASE {db_name}'))
        logger.info(f'Database "{db_name}" dropped successfully.')
    else:
        logger.info(f'Database "{db_name}" does not exist.')


def create_new_database(connection, db_name):
            connection.execute(text(f'CREATE DATABASE {db_name}'))
            logger.info(f'Database "{db_name}" created successfully.')

            
def main():
    user, password, host, port, database = db_details()
    # Create an engine connected to the default database
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

    new_db_name = 'new_database'

    # Connect to the database and drop the target database if it exists, then create new database, then create tables
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")  # Set isolation level to autocommit
        try:
            drop_database_if_exists(connection=connection, db_name=new_db_name)
            create_new_database(connection=connection, db_name=new_db_name)

        except (ProgrammingError, OperationalError) as e:
            print(f'Error: {e}')


if __name__ == "__main__":
    main()