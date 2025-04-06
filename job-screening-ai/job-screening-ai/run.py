import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Change to the src directory
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Import and run the application
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True) 