import datetime
import logging
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
# from airflow.hooks.http_hook import http_hook
from shared_functions import upsert_player_data


def retrieve_bulk_player_file(**context):
    import httpx

    local_file_path = "player_data_partial.parquet"

    http_conn_id = 'repository_raw_url'
    http_connection = BaseHook.get_connection(http_conn_id)

    file_endpoint = "chapter10/player_data_partial.parquet"

    file_url = f"{http_connection.host}{file_endpoint}"


    with httpx.Client() as client:
        response = client.get(file_url)
        response.raise_for_status()  
        with open(local_file_path, 'wb') as file:
            file.write(response.content)

    context['ti'].xcom_push(key='local_parquet_file_path', value=local_file_path)

def insert_update_player_data_bulk(**context):
    import pandas as pd
    
    local_parquet_file_path = context['ti'].xcom_pull(task_ids='bulk_file_retrieve', key='local_parquet_file_path')
    player_df = pd.read_parquet(local_parquet_file_path)
    player_json = player_df.to_json(orient='records')
    upsert_player_data(player_json)

# def insert_update_player_data_bulk(**context):
#     import sqlite3
#     import pandas as pd

# # Fetch the connection object
#     database_conn_id = 'analytics_database'
#     connection = BaseHook.get_connection(database_conn_id)
    
#     sqlite_db_path = connection.schema

#     local_parquet_file_path = context['ti'].xcom_pull(task_ids='bulk_file_retrieve', key='local_parquet_file_path')

#     if local_parquet_file_path:

#         player_df = pd.read_parquet(local_parquet_file_path)

        
#         # Use a context manager for the SQLite connection
#         with sqlite3.connect(sqlite_db_path) as conn:
#             cursor = conn.cursor()

#             # Insert each player record into the 'player' table
#             for _, player in player_df.iterrows():
#                 try:
#                     cursor.execute("""
#                     INSERT INTO player (player_id, gsis_id, first_name, last_name, position, last_changed_date) 
#                     VALUES (?, ?, ?, ?, ?, ?) 
#                     ON CONFLICT(player_id) DO UPDATE SET 
#                     gsis_id=excluded.gsis_id, first_name=excluded.first_name, last_name=excluded.last_name, 
#                     position=excluded.position, last_changed_date=excluded.last_changed_date
#                     """, (
#                         player['player_id'], player['gsis_id'], player['first_name'], 
#                         player['last_name'], player['position'], player['last_changed_date']
#                     ))
#                 except Exception as e:
#                     logging.error(f"Failed to insert player {player['player_id']}: {e}")
#                     raise
                    
#     else:
#         logging.warning("No player data found.")
#         raise ValueError("No player data found. Task failed due to missing data.")

@dag(start_date=datetime.datetime(2024, 8, 7), schedule_interval=None, catchup=False)  
def bulk_player_file_load_dag():

    bulk_file_retrieve_task = PythonOperator(
        task_id='bulk_file_retrieve',
        python_callable=retrieve_bulk_player_file,
        provide_context=True,
    )

    player_sqlite_upsert_task = PythonOperator(
        task_id='player_sqlite_upsert',
        python_callable=insert_update_player_data_bulk,
        provide_context=True,
    )


    # Define the task dependencies
    bulk_file_retrieve_task >> player_sqlite_upsert_task

# Instantiate the DAG
dag_instance = bulk_player_file_load_dag()


