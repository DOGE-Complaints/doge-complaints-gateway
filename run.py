from app import create_app

print("Starting the application...")
import os
print(f"Current working directory: {os.getcwd()}")
from dotenv import find_dotenv
print(f"Loading .env from: {find_dotenv()}")

# Create an instance of the application
app = create_app()

# Entry point
if __name__ == '__main__':
    # Run the application with the specified host and port
    
    print("Starting the application...")
    app.run(host='0.0.0.0', port=5001, debug=True)
