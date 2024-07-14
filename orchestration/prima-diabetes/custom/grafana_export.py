import os
import pandas as pd
from sqlalchemy import create_engine, text

import logging

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def create_table_if_not_exists(engine, table_name: str):
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    pregnancies INTEGER,
                    glucose INTEGER,
                    bloodpressure INTEGER,
                    skinthickness INTEGER,
                    insulin INTEGER,
                    bmi FLOAT,
                    diabetespedigreefunction FLOAT,
                    age INTEGER,
                    outcome INTEGER,
                    pred_outcome INTEGER,
                    index INTEGER
                )
            """
                )
            )
        logging.info("Table created or already exists.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")


def insert_dataframe_to_postgres(engine, df: pd.DataFrame, table_name: str):
    try:
        df.to_sql(table_name, engine, if_exists="append", index=False)
        logging.info("DataFrame inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting DataFrame: {e}")


def create_data_table(engine, data, table_name):
    create_table_if_not_exists(engine, table_name)
    insert_dataframe_to_postgres(engine, data, table_name)


@custom
def transform_custom(data, *args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    train_data, validation_data = data
    # PostgreSQL connection string
    DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    create_data_table(engine, train_data, "monitor_train_data_table")
    create_data_table(engine, validation_data, "monitor_validation_table")

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
