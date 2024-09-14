import db  # Assuming db.py is correctly loaded
import fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import db
from db import get_database
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

def process_query(query_text):
    # Get the database and collection
    db_instance = db.get_database()
    collection = db_instance['Articles']
    collection.create_index([('content', 'text')])
    # Fetch documents from the MongoDB collection
    docs = list(collection.find({"$text": {"$search": query_text}}))
    
    if not docs:
        return "No documents found in the database."

    # Vectorize the documents
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    corpus = [doc['content'] for doc in docs]
    document_vectors = vectorizer.fit_transform(corpus)
    
    # Vectorize the query
    from sklearn.metrics.pairwise import cosine_similarity
    query_vector = vectorizer.transform([query_text])
    similarity_scores = cosine_similarity(query_vector, document_vectors).flatten()
    
    # Find the most similar document
    best_match_idx = similarity_scores.argmax()
    best_doc = docs[best_match_idx]
    
    return best_doc['content']
