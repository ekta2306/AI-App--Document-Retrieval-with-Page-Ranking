import pymongo
from pymongo import MongoClient
import urllib.parse

def get_mongo_client():
    # For another mongoDB databse, replace with respective credentials
    username = urllib.parse.quote_plus("trial-user")
    password = urllib.parse.quote_plus("trial-user")

    connection_string = f"mongodb+srv://{username}:{password}@cluster0.tm97tgc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Connect to MongoDB Atlas
    return MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)


def get_database():
    # Access the database and collection
    client=get_mongo_client()
    return client['DocumentsTrial']  