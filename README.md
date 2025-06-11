# Apache Airflow Individual Project - Web Scraping and Data Pipeline

The project is to create a data pipeline with Apache Airflow DAG to retrieve at least 100 video data from YouTube based on a dynamic topic (stored in topic.txt) through Python Selenium web scraping and store the video data into MongoDB database

## Solution

Watch **[video](https://www.youtube.com/watch?v=RsWLrtI_8Kc)** for the solution and steps of setting up a new DAG with custom Python scripts:

- Show how to start Apache Airflow in Ubuntu

```
source airflow_env/bin/activate
cd $AIRFLOW_HOME
airflow db init
airflow scheduler
airflow webserver
```

- Launch and open Apache Airflow UI
  - Available at http://localhost/8080
- Show where to place new DAG files and how to verify in the Apache Airflow UI
- Explain the logic in the two python scripts (fetch_youtube_data.py and load_data_to_mongo.py)
- Show how to run/execute this new DAG
- Show how to verify that the DAG execution was successful
  1. Show intermediate file(s) generated
  2. Show MongoDB collection with actual data (no duplicates)

## Data Pipeline Architecture

<img width="600" alt="Data Pipeline Architecture" src="Data Pipeline Architecture.png">
