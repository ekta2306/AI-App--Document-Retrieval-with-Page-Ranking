import app_start
from app_start import app  # Import the Flask app from app.py

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)