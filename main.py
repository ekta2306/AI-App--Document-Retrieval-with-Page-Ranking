import app_start
import subprocess
from app_start import app  # Import the Flask app from app.py
import os

#if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    # Run the external Python file to install packages
subprocess.run(['python', 'ML-copy\installations.py'], check=True)

    # Now import and use the installed packages
    #import query_access
#query_access.get_query()
    
if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)