import sys
import os
import threading
import time

def run_api():
    """Run the Flask API server."""
    os.chdir('app')
    subprocess.run([sys.executable, 'api.py'])

def run_streamlit():
    """Run the Streamlit app."""
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'pages/home.py'])

if __name__ == '__main__':
    # Start API in a separate thread
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    # Wait a bit for API to start
    time.sleep(2)

    # Start Streamlit
    run_streamlit()

import subprocess
import sys
import os
import time

if __name__ == '__main__':
    # Start API server
    os.chdir('app')
    api_process = subprocess.Popen([sys.executable, 'api.py'])
    os.chdir('..')

    # Wait a bit for API to start
    time.sleep(2)

    # Start Streamlit app
    streamlit_process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'pages/home.py'])

    # Wait for both to finish (they won't, but in case)
    api_process.wait()
    streamlit_process.wait()
