# References:
# https://hevodata.com/learn/airflow-mongodb-integration-for-api-data/
# https://hevodata.com/learn/json-to-mongodb-python/#7
# https://stackoverflow.com/questions/51734923/airflow-python-operator-writes-files-to-different-locations

def load_data_to_mongo(topic):
    # Import libraries
    import pymongo
    import json
    import os
    import time

    # Allow some buffer time to show that JSON file had been created
    time.sleep(5)

    topic_stripped = topic.replace(" ", "")
    database_name = topic_stripped + "DB"

    # MongoDB connection string
    connection_string = f"mongodb+srv://scyt:Bl00mar3h@cluster0.ivlin.mongodb.net/{database_name}?retryWrites=true&w=majority"

    # Create a MongoDB client
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]
    collection = db[topic_stripped]

    try:
        json_file_path = topic_stripped + ".json"

        if os.path.exists(json_file_path):
            # Open JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)

            # Insert data into MongoDB
            collection.insert_many(json_data)
            print("Successfully inserted data into MongoDB")

            # Delete the input JSON file from file system
            os.remove(json_file_path)
            print("Successfully deleted JSON file")

    except Exception as e:
        print(f"Error: {e}")
