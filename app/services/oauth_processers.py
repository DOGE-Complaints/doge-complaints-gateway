from flask import Blueprint, request, jsonify, redirect
from app.db import supabase
import os
facebook_bp = Blueprint('facebook', __name__)

CHAT_GPT_URL = os.getenv('CHAT_GPT_URL')

@facebook_bp.route('/oauth/facebook-callback')
def facebook_callback():

    # get user_id and session_id from request

    facebook_user_id = request.args.get('user_id')
    session_id = request.args.get('state')
    callback_url = request.args.get('callback_url')

    # if callback is not starting with CHAT_GPT_URL, then set it to the default one
    if not callback_url.startswith(CHAT_GPT_URL):
        return jsonify({'error': 'Invalid callback_url'}), 400
    
    if not facebook_user_id or not session_id or not callback_url:
        return jsonify({'error': 'Missing required parameters'}), 400

    # create a new user in the database
    user_data = {
        'oauth_provider_user_id': facebook_user_id,
        'oauth_provider': 'facebook'
    }
    user_response = supabase.table('oauth_users').insert(user_data).execute()
    if not user_response.data:
        return jsonify({'error': 'Failed to create user'}), 500
    
    # retrieve from session_complaints by session_id
    session_complaints = supabase.table('session_complaints').select('*').eq('session_id', session_id).execute()
    if not session_complaints.data:
          print(f"Session not found for session_id: {session_id}")

    if session_complaints.data[0].get('user_id'):
        return jsonify({'message': 'User already linked to session'}), 200

    if not session_complaints.data:
        print(f"Session not found for session_id: {session_id}")
        return redirect(f"{callback_url}/")

    # Taking the user_id from the freshly created user
    user_id = user_response.data[0].get('id')

    # And linking it with the complaint in the session_complaint table in order to keep track of the user who created the complaint
    complaint_id = session_complaints.data[0]['complaint_id']
    if (complaint_id is not None):
        # update session_complaints with the user_id
        supabase.table('session_complaints').update({
            'user_id': user_id
        }).eq('session_id', session_id).execute()
    # redirect to the callback url concatenating the session_id
    return redirect(f"{callback_url}/{session_id}")


def connect_complaint_to_session(session_id, complaint_id):
    supabase.table('session_complaints').insert({
        'session_id': session_id,
        'complaint_id': complaint_id
    }).execute()
