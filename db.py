import pymongo
from pymongo import MongoClient
import urllib.parse

def get_mongo_client():
    # Replace these with your actual username, password, and cluster connection string
    username = urllib.parse.quote_plus("FaultInOurStars")
    password = urllib.parse.quote_plus("FaultInOurStars")
    #cluster_url = "cluster0.mongodb.net"  # Your MongoDB cluster URL

    # Replace 'myFirstDatabase' with the name of your database
    connection_string = f"mongodb+srv://{username}:{password}@cluster0.tm97tgc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Connect to MongoDB Atlas
    return MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)


def get_database():
    # Access the database and collection
    client=get_mongo_client()
    return client['DocumentsTrial']  # Replace with your database name