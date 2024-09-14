from pymongo import MongoClient
import urllib.parse

# Replace these with your actual username, password, and cluster connection string
username = urllib.parse.quote_plus("FaultInOurStars")
password = urllib.parse.quote_plus("FaultInOurStars")
#cluster_url = "cluster0.mongodb.net"  # Your MongoDB cluster URL

# Replace 'myFirstDatabase' with the name of your database
connection_string = f"mongodb+srv://{username}:{password}@cluster0.tm97tgc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsCAFile=isrgrootx1.pem"

# Connect to MongoDB Atlas
client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True,tlsCAFile='/content/isrgrootx1.pem')

# Access the database and collection
db = client['DocumentsTrial']  # Replace with your database name
collection = db['Articles']  # Replace with your collection name