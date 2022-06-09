# load to big query

from google.cloud import bigquery
import logging
from logging import INFO
import pandas as pd
import pandas_gbq
import sys

logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging

def load_to_gbq() -> None:
    """
    creates a Google BigQuery dataset and table, and loads a pandas dataframe to it
    """
    # Instantiate big query client api which will create a dataset
    client = bigquery.Client()
    # Tell the client to use "poke_battler_table" as the dataset name to create in the project
    dataset_id = f"{client.project}.poke_battler_data"
    # Pass dataset_id to bigquery's Dataset class to build a reference
    dataset = bigquery.Dataset(dataset_id)
    # Assign the datasets server location to US
    dataset.location = "US"
    # Tell the client to create the dataset on google big query with the completed information
    dataset = client.create_dataset(dataset, exists_ok=False, timeout=30)
    # If successful, log the creation of the dataset
    logger.info(f"Created dataset: '{dataset.dataset_id}' in '{client.project}'.")


    # Project to look for when creating a table,
    project_id = "deb-01-346205"
    # dataset to insert the table into
    table_id = "poke_battler_data.pokemon"

    # Loading transformed dataframe into google big query with the specified project/dataset as targets and a specified table schema.
    logger.info(f"Loading dataframe to: '{dataset.dataset_id}'...")
    # Reset dataframe index before loading to bigquery, because bigquery does not support/display dataframe indexes. English_name would not show in table. Set to new df so the old one's index can still be called for battler functions
    poke_df = pd.read_csv("pokemon.csv")
    pandas_gbq.to_gbq(poke_df, table_id, project_id=project_id, if_exists="fail", api_method="load_csv", table_schema=[
        {'name': 'national_number', 'type': 'INT64'}, 
        {'name': 'gen', 'type': 'STRING'}, 
        {'name': 'name', 'type': 'STRING'}, 
        {'name': 'primary_type', 'type': 'STRING'}, 
        {'name': 'secondary_type', 'type': 'STRING'}, 
        {'name': 'classification', 'type': 'STRING'}, 
        {'name': 'height_m', 'type': 'FLOAT64'}, 
        {'name': 'weight_kg', 'type': 'FLOAT64'}, 
        {'name': 'hp', 'type': 'INT64'}, 
        {'name': 'attack', 'type': 'INT64'}, 
        {'name': 'defense', 'type': 'INT64'}, 
        {'name': 'sp_attack', 'type': 'INT64'}, 
        {'name': 'sp_defense', 'type': 'INT64'}, 
        {'name': 'speed', 'type': 'INT64'}, 
        {'name': 'abilities_0', 'type': 'STRING'}, 
        {'name': 'abilities_1', 'type': 'STRING'}, 
        {'name': 'abilities_2', 'type': 'STRING'},
        {'name': 'abilities_hidden', 'type': 'STRING'},
        {'name': 'against_normal', 'type': 'FLOAT64'},
        {'name': 'against_fire', 'type': 'FLOAT64'},
        {'name': 'against_water', 'type': 'FLOAT64'},
        {'name': 'against_electric', 'type': 'FLOAT64'},
        {'name': 'against_grass', 'type': 'FLOAT64'},
        {'name': 'against_ice', 'type': 'FLOAT64'},
        {'name': 'against_fighting', 'type': 'FLOAT64'},
        {'name': 'against_poison', 'type': 'FLOAT64'},
        {'name': 'against_ground', 'type': 'FLOAT64'},
        {'name': 'against_flying', 'type': 'FLOAT64'},
        {'name': 'against_psychic', 'type': 'FLOAT64'},
        {'name': 'against_bug', 'type': 'FLOAT64'},
        {'name': 'against_rock', 'type': 'FLOAT64'},
        {'name': 'against_ghost', 'type': 'FLOAT64'},
        {'name': 'against_dragon', 'type': 'FLOAT64'},
        {'name': 'against_dark', 'type': 'FLOAT64'},
        {'name': 'against_steel', 'type': 'FLOAT64'},
        {'name': 'against_fairy', 'type': 'FLOAT64'},
        {'name': 'is_sublegendary', 'type': 'INT64'},
        {'name': 'is_legendary', 'type': 'INT64'},
        {'name': 'is_mythical', 'type': 'INT64'},
        {'name': 'description', 'type': 'STRING'},
        {'name': 'wins', 'type': 'INT64'},
        {'name': 'losses', 'type': 'INT64'}])
    logger.info(f"Successfully loaded dataframe into '{dataset.dataset_id}'.")

load_to_gbq()