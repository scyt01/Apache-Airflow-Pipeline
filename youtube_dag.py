# Import libraries
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from fetch_youtube_data import fetch_youtube_data
from load_data_to_mongo import load_data_to_mongo
import os

# Obtain topic from topic.txt
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")
with open(AIRFLOW_HOME + "/dags/topic.txt", "r") as file:
    # Assumption: topic.txt can contain text that are in uppercase and it is better to query with lowercase
    topic = file.read().lower()
    print(topic)

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 24),
    'retries': 1,
}

# Define DAG
with DAG(
    dag_id='is459_assignment_youtube',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    # Define tasks
    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=fetch_youtube_data,
        # Put a large number > 100 to use in fetch_youtube_data.py for loop to meet the requirement
        # YouTube has both shorts and videos (long-form)
        # fetch_youtube_data.py only extracts data from videos (long-form)
        op_kwargs={"topic": topic, "max_results": 150}
    )

    task_2 = PythonOperator(
        task_id='task_2',
        python_callable=load_data_to_mongo,
        op_kwargs={"topic": topic}
    )

    # Set task dependencies
    # Task 1 runs before Task 2
    task_1 >> task_2
