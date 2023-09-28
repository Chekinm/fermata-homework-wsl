"""
MongoDB Database Setup and Index Creation

This script is responsible for setting up the MongoDB database
connection and creating indexes
to optimize database queries for your application. It uses the PyMongo library
to interact with MongoDB.

Usage:
- Configure the MongoDB connection details and database/collection names in
'config.config'.


Dependencies:
- Ensure that you have installed the PyMongo library.
- The configuration settings for MongoDB, including the URI, database name,
and collection names,
  should be defined in 'config.config'.
"""

from pymongo import MongoClient
from config.config import (MONGODB_URI,
                           MONGODB_DB_NAME,
                           MONGODB_IMAGE_COLLECTION_NAME,
                           MONGODB_GROUPS_COLLECTION_NAME,
                           )

# Establish a connection to the MongoDB server
client = MongoClient(MONGODB_URI)

# Access the specified MongoDB database
db = client[MONGODB_DB_NAME]

# Access the collections in the database
images_collection = db[MONGODB_IMAGE_COLLECTION_NAME]
groups_collection = db[MONGODB_GROUPS_COLLECTION_NAME]

# Create indexes for optimized database queries
images_collection.create_index([("status", 1), ("created_at", -1)])
groups_collection.create_index([("name", 1)])
