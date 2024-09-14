
import subprocess

# Run the external Python file to install packages
subprocess.run(['python', 'ML-copy\installations.py'], check=True)

# Now import and use the installed packages
import query_access

query_access.get_query()
