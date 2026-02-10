import json
from pymongo import MongoClient
import os

# 1. Connect to MongoDB
client = MongoClient("localhost:27017")
db = client.datasets
collection = db.datasets_law

# 2. List of your JSON files
json_files = [
    "datasets/entry1.json",
    "datasets/entry2.json",
    "datasets/entry3.json",
    "datasets/entry4.json",
    "datasets/entry5.json",
    "datasets/entry6.json",
    "datasets/entry7.json",
    "datasets/entry8.json",
    "datasets/entry9.json",
    "datasets/entry10.json",
    "datasets/entry11.json",
    "datasets/metadata.json"
]

all_data = []

for file_path in json_files:
    if os.path.getsize(file_path) == 0:
        print(f"Warning: {file_path} is empty, skipping.")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                all_data.extend(data)  # add all entries if it's a list
            else:
                all_data.append(data)  # add single entry
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_path}: {e}")

# 3. Insert all data into MongoDB
if all_data:
    collection.insert_many(all_data)
    print(f"Inserted {len(all_data)} documents successfully!")
else:
    print("No valid data to insert.")
