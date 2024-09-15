# 21BCT0321_ML
## AI Intern Task

### Project Overview
This project is an AI-powered document retrieval system that utilizes a Flask-based API for querying a MongoDB database. The system processes user queries, retrieves relevant documents, and ranks them using the BM25 page ranking algorithm. The backend is designed to handle user-specific queries with request throttling and session logging.

#### The project is divided into multiple components:

Database Connection (db.py)
Main Functionality (main.py)
Package Installations (installations.py)
Query Access (query_access.py)
Query Processing (query.py)
Flask Application (app_start.py)

### Features
1. User-Based Request Management
Tracks the number of requests made by a user.
Limits the number of requests (set to 5).
Throws HTTP 429 status code if the user exceeds the limit.
2. MongoDB for Data Storage
Stores user data and document information.
Manages request counts for each user.
3. BM25 Ranking Algorithm
The system employs the BM25 ranking algorithm, a state-of-the-art technique for scoring documents based on the query’s relevance. BM25 adjusts weights depending on term frequency and document length, making it an ideal choice for retrieval tasks where precision is required.

### File Descriptions
1. db.py: Database Connection
This file handles the connection to the MongoDB database. It connects to the MongoDB Atlas cluster and returns a client to interact with the database.

```python
from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient('your_connection_string')
    db = client['DocumentsTrial']
    return db
```

2. main.py: Main Function
This is the entry point for the application. It manages the overall flow of the backend, from initialization to handling requests, installing dependencies, and running the Flask app.

3. installations.py: Installations and Setup
This script installs the required packages like Flask and PyMongo. It is executed at the start of the application to ensure all dependencies are met.

```python
import os

os.system("pip install flask")
os.system("pip install pymongo")
```

4. query_access.py: Accessing Queries
This script handles incoming queries by checking user limits and preparing them for further processing.

```python
def handle_query(query, user_id):
    # Check if user exists, limit their requests, and process the query
    pass
```
5. query.py: Query Processing
Here, the queries are tokenized and passed to the BM25 ranking algorithm to fetch and rank the most relevant documents from the database.

```python
def bm25_ranking(documents, query):
    # Process documents and rank them using BM25
    pass
```
6. app_start.py: Flask Application
This script contains the Flask app that serves the API, managing /health and /search endpoints for the client to interact with.
```python
from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return "API is healthy"

@app.route('/search')
def search():
    # Handle user query and return ranked documents
    pass

if __name__ == "__main__":
    app.run(debug=True)
```

Here, the query and query_access scripts are supporting scripts that can be used when implementing distributed caching. The system currently runs without the need for these two scripts.

### Endpoints

- **`/health`**: Returns a random response to check if the API is active.
- **`/search`**: Returns a list of top results for the given query. Parameters:
  - `text`: The prompt text.
  - `top_k`: Number of results to fetch.
  - `threshold`: Threshold for similarity score.


### BM25 Ranking Algorithm
BM25 (Best Matching 25) is a term-based ranking function used for retrieving relevant documents in response to a query. It calculates the relevance score by analyzing term frequency, inverse document frequency, and length of the document. BM25 is widely used due to its effectiveness in producing accurate search results.

The below image shows an example of a search query, where two articles are matched to a keyword and are ranked on the basis of BM25 score.
![image](https://github.com/user-attachments/assets/db547be5-68b7-4b33-96e9-d36066d34045)


## Future Improvements

### Distributed Caching 
Distributed caching is a technique used to enhance application performance by storing data across multiple servers. For this project, incorporating distributed caching can provide several benefits:

### Improved Performance:

Reduced Latency: By caching frequently accessed data, response times are significantly reduced.
Increased Throughput: Multiple cache servers can handle more requests, improving the system's scalability.
Scalability:

Horizontal Scaling: Adding more cache servers to handle increased load.
Load Balancing: Distributing requests across multiple cache servers to prevent bottlenecks.
Fault Tolerance:

High Availability: Data remains accessible even if one cache server fails.
Data Replication: Ensuring data availability through replication across servers.

### Recommended Distributed Caching Solutions
Redis: An in-memory data structure store known for its speed and versatility.
Memcached: A high-performance distributed memory object caching system.
Apache Ignite: Provides distributed caching with in-memory computing.
Hazelcast: An in-memory data grid with caching capabilities.

### Integration Steps
Setup: Install and configure the distributed caching solution.
Connection: Integrate the cache with the application using appropriate client libraries.
Caching Logic: Implement caching for frequently accessed data.
Configuration: Set up cache expiry and eviction policies to manage data lifecycle.
Monitoring: Use tools to monitor cache performance and ensure reliability.

### Enhanced Cache Strategies:

Cache Warming: Pre-load frequently accessed data into the cache.
Hierarchical Caching: Implement different tiers of caching for various data types.
Machine Learning Integration:

Utilize caching for storing intermediate results or model predictions to reduce computation time.
Incorporating distributed caching into this system will lead to improved performance and scalability, especially as data access patterns become more complex and the volume of requests increases.

1. Distributed Cache
Using a distributed caching system (e.g., Redis or Memcached) could drastically improve response times and reduce the load on MongoDB by storing frequent queries and their results temporarily. This would especially be beneficial for high-traffic systems or those with large datasets.

2. Scalability Enhancements
By implementing horizontal scaling for both the database and the application, the system can handle more users and larger datasets. Additionally, the Flask app could be deployed using a production-grade server like Gunicorn or uWSGI for better performance and security.

## Dockerizing the Flask Application
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask to be accessible
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app_start.py
ENV FLASK_ENV=development  # For production, set this to 'production'

# Run Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
```
Build the Docker Image: Navigate to your project directory and run the following command to build the Docker image:
```bash
docker build -t flask-app:latest .
```
This command will create an image named flask-app using the instructions provided in the Dockerfile.

Run the Docker Container: Once the image is built, you can run the container using:
```bash
docker run -p 5000:5000 flask-app
```
Stopping the Container
To stop the container, press CTRL+C in the terminal where it is running. Alternatively, you can list and stop the container using Docker commands:

List running containers:
```bash
docker ps
```
Stop the container:
```bash
docker stop <container_id>
```
Replace <container_id> with the ID of the running container, which you get from the docker ps command.

### Future Improvements with Docker
Using Docker Compose: If your application grows, you may want to use Docker Compose to run multiple services like MongoDB and Flask together. Docker Compose allows you to define and manage multi-container Docker applications more easily.

Production Readiness: For production environments, you might want to use a WSGI server like gunicorn instead of the built-in Flask server, as it's better suited for handling multiple requests and scaling.

## Setup Instructions

Clone the repository:
```bash
git clone https://github.com/ekta2306/21BCT0321_ML.git
```
Install the required packages:
```bash
pip install -r 21BCT0321_ML\requirements.txt
```
MongoDB Setup:
Ensure you have a MongoDB instance running. You can either use a local MongoDB instance or a cloud MongoDB Atlas instance.
Update the MongoDB connection string in db.py:
```python
from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient("mongodb+srv://<username>:<password>@cluster_url/database_name")
    return client
```
Run the application:
```bash
python 21BCT0321_ML\main.py
```

## Using the API
###Check Health:
```bash
curl http://127.0.0.1:5000/health
```
### Search:
```bash
curl "http://127.0.0.1:5000/search?user_id=<user_name>"
```
### Search with keyword:
```bash
curl "http://127.0.0.1:5000/search?user_id=<user_name>&text=<keyword>"
```
