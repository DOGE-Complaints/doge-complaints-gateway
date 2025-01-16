from app import create_app

print("Starting the application...")

# Create an instance of the application
app = create_app()

# Entry point
if __name__ == '__main__':
    # Run the application with the specified host and port
    
    print("Starting the application...")
    app.run(host='0.0.0.0', port=5001, debug=True)
