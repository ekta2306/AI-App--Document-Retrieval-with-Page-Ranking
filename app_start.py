
import flask
import flask_limiter
from flask import Flask, request, jsonify
import time
import threading
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from math import log
import re
import db
from bson import ObjectId

app = Flask(__name__)

# Setup Flask-Limiter to limit requests
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

db_inst=db.get_database()
users_collection = db_inst['Users']
articles_collection = db_inst["Articles"]

print(f"db: {type(db)}")
print(f"users_collection: {type(users_collection)}")

# Logging setup
logging.basicConfig(filename="api.log", level=logging.INFO)

# Scraping function (you can add your scraping logic here)
def scrape_articles():
    while True:
        articles = [
            {"title": "News article 1", "content": "Content of article 1", "score": 0.85, "date": "2024-09-10"},
            {"title": "News article 2", "content": "Content of article 2", "score": 0.75, "date": "2024-09-09"}
        ]
        articles_collection.insert_many(articles)
        time.sleep(3600)

initialized = False

@app.before_request
def before_request():
    global initialized
    if not initialized:
        print("Running setup for the first request")
        # Put your initialization code here
        thread = threading.Thread(target=scrape_articles, daemon=True)
        thread.start()
        initialized = True


#@app.before_first_request
#def activate_scraping_job():
#    thread = threading.Thread(target=scrape_articles)
#    thread.start()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is active"})

# Helper function for BM25 page ranking
def bm25_ranking(articles, query, k1=1.5, b=0.75):
    def tokenize(text):
        return re.findall(r'\w+', text.lower())

    N = len(articles)  
    avgdl = sum(len(tokenize(a['content'])) for a in articles) / N
    query_terms = tokenize(query)

    def idf(term):
        df = sum(1 for a in articles if term in tokenize(a['content']))
        return log((N - df + 0.5) / (df + 0.5) + 1)

    def bm25_score(article):
        score = 0
        doc_tokens = tokenize(article['content'])
        doc_len = len(doc_tokens)
        term_frequencies = {term: doc_tokens.count(term) for term in query_terms}

        for term in query_terms:
            if term in term_frequencies:
                tf = term_frequencies[term]
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_len / avgdl))
                score += idf(term) * (numerator / denominator)
        return score

    for article in articles:
        article['bm25_score'] = bm25_score(article)

    return sorted(articles, key=lambda x: x['bm25_score'], reverse=True)


def convert_objectid_to_str(articles):
    """Helper function to convert ObjectId to string in MongoDB documents"""
    for article in articles:
        if '_id' in article:
            article['_id'] = str(article['_id'])
    return articles

@app.route('/search', methods=['GET'])
@limiter.limit("5 per minute", override_defaults=False)
def search():
    start_time = time.time()

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = users_collection.find_one({"user_id": user_id})
    if user:
        if user['request_count'] >= 5:
            return jsonify({"error": "Too many requests"}), 429
        users_collection.update_one({"user_id": user_id}, {"$inc": {"request_count": 1}})
    else:
        users_collection.insert_one({"user_id": user_id, "request_count": 1})

    text = request.args.get('text')
    top_k = int(request.args.get('top_k', 5))
    threshold = float(request.args.get('threshold', 0.5))

    articles_collection.create_index([('content', 'text')])
    # Fetch documents from the MongoDB collection
    search_results = list(articles_collection.find({"$text": {"$search": text}}))
    search_results = convert_objectid_to_str(search_results)
    # Search MongoDB articles collection
    #search_results = list(articles_collection.find())
    
    # Apply BM25 ranking algorithm
    ranked_results = bm25_ranking(search_results, text)

    # Filter results based on score threshold and limit by top_k
    filtered_results = [res for res in ranked_results if res['bm25_score'] >= threshold][:top_k]

    inference_time = time.time() - start_time
    logging.info(f"User {user_id} made a request. Inference time: {inference_time:.2f} seconds.")

    return jsonify({"results": search_results, "inference_time": inference_time})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=5000)
