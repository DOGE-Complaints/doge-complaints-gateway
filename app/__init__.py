from flask import Flask
from .services.proces_complaint import proces_complaint_bp
from supabase import create_client, Client
import os

supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def create_app():
    print("Creating the app...")
    app = Flask(__name__)
    print("App created successfully")
    #register blueprints
    app.register_blueprint(proces_complaint_bp, url_prefix='/api/v1/')
    print("Blueprint registered successfully")
    return app
