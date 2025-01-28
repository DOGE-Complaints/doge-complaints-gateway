#submit complaint

from app.db import supabase
import uuid
from flask import Blueprint, request, jsonify
from app.utils.ai_helper import vectorize_text
from app.utils.geocoding import get_coordinates
from app.services.oauth_processers import connect_complaint_to_session
from app.utils.enumerators import ComplaintTimeType

submit_complaint_bp = Blueprint('submit_complaint', __name__)

@submit_complaint_bp.route('/generate-session', methods=['POST'])
def generate_session():
    
    session_id = uuid.uuid4()

    # validate uniqueness of session_id
    session_complaints = supabase.table('session_complaints').select('*').eq('session_id', session_id).execute()

    while session_complaints.data:
        session_id = uuid.uuid4()
        session_complaints = supabase.table('session_complaints').select('*').eq('session_id', session_id).execute()
    
    # create session in supabase
    supabase.table("session_complaints").insert({
        "session_id": session_id
    }).execute()

    return jsonify({"session_id": session_id}), 200

@submit_complaint_bp.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    print("Submitting complaint...")
    # Get JSON from request
    data = request.get_json()
    session_id = data.get("session_id")
    
    if (session_id is None):
        #generate randomg session_id with UUID
        session_id = str(uuid.uuid4())

    print(f"Received data: {data}")
    print(f"Received session_id: {session_id}")
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    complaint = data.get("complaint")
    if not complaint:
        return jsonify({"error": "Missing 'complaint' key in JSON"}), 400
    
    if session_id is None:
        return jsonify({"error": "Missing 'session_id' key in JSON"}), 400

    print(f"Complaint: {complaint}")

    if complaint.get("user") is None:
        return jsonify({"error": "Missing 'user' key in complaint"}), 400
    if complaint.get("description") is None:
        return jsonify({"error": "Missing 'description' key in complaint"}), 400
    if complaint.get("severity") is None:
        return jsonify({"error": "Missing 'severity' key in complaint"}), 400
    if complaint.get("impact_estimation") is None:
        return jsonify({"error": "Missing 'impact_estimation' key in complaint"}), 400
    if complaint.get("problem_status") is None:
        return jsonify({"error": "Missing 'problem_status' key in complaint"}), 400

    try:
        # Setting all fields to complaints table via supabase
        complaint_data = {
            "user_first_name": complaint.get("user").get("first_name"),
            "user_last_name": complaint.get("user").get("last_name"),
            "complaint_description": complaint.get("description"),
            "severity": complaint.get("severity"),
            "impact_estimation": complaint.get("impact_estimation"),
            "problem_status": complaint.get("problem_status")
        }

        if complaint.get("location") is None or complaint.get("location").get("details") is None:
            return jsonify({"error": "Missing 'location' key in complaint"}), 400
        
        # extracting location details for geo-location
        lat, lon = get_coordinates(complaint["location"]["details"])
        print(f"Coordinates: {lat}, {lon}")

        # Adding coordinates to complaint_data if they are not None
        if lat is not None and lon is not None:
            complaint_data["location_coords"] = f"SRID=4326;POINT({lon} {lat})"
        
        complaint_response = supabase.table("complaints").insert(complaint_data).execute()

        if not complaint_response.data:
            return jsonify({"error": "Failed to insert complaint into complaints table"}), 500

        complaint_id = complaint_response.data[0].get("id")
        print(f"Complaint ID: {complaint_id}")

        # Inserting schedule into 'complaint_time' table
        setComplaintTime(complaint_id, complaint)
        
        # Inserting categories into 'complaint_problem_categories' table
        setComplaintCategories(complaint_id, complaint)
        
        # Inserting related events into 'complaint_related_events' table
        setComplaintRelatedEvents(complaint_id, complaint)

        # connect complaint to session and previously validate if sesion_id is not already in session_complaints table
        session_complaints = supabase.table("session_complaints").select("*").eq("session_id", session_id).execute()
        if not session_complaints.data:
            connect_complaint_to_session(session_id, complaint_id)
            
    except Exception as e:
        print(f"Error: {e}")
        # Delete complaint if error occurs
        supabase.table("complaints").delete().eq("id", complaint_id).execute()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Complaint added successfully"}), 201

def setComplaintTime(complaint_id, complaint):
    if complaint.get("time") is None:
        return jsonify({"error": "Missing 'time' key in complaint"}), 400

    if complaint.get("time") is None or complaint.get("time").get("type") is None:
        return jsonify({"error": "Missing 'time.type' key in complaint"}), 400

    complaint_time_type = complaint.get("time").get("type")
    complaint_time_data = {
        "complaint_id": complaint_id,
        "type": complaint_time_type
    }

    if complaint_time_type == ComplaintTimeType.EXACT:
        complaint_time_data["exact_timestamp"] = complaint.get("time").get("value")
    elif complaint_time_type == ComplaintTimeType.DATE:
        complaint_time_data["date"] = complaint.get("time").get("value")
    elif complaint_time_type == ComplaintTimeType.DATE_RANGE:
        complaint_time_data["start_date"] = complaint.get("time").get("start_date")
        complaint_time_data["end_date"] = complaint.get("time").get("end_date")
    elif complaint_time_type == ComplaintTimeType.DATETIME_RANGE:
        complaint_time_data["start_datetime"] = complaint.get("time").get("start_datetime")
        complaint_time_data["end_datetime"] = complaint.get("time").get("end_datetime")
    elif complaint.get("time").get("time_interval"):
        complaint_time_data["time_interval"] = complaint.get("time").get("time_interval") #i.e. morning, evening
    elif complaint.get("time").get("approx_period"):
        complaint_time_data["approx_period"] = complaint.get("time").get("approx_period")

    print(f"Complaint time data: {complaint_time_data}")
    supabase.table("complaint_time").insert(complaint_time_data).execute()

def setComplaintCategories(complaint_id, complaint):
    if complaint.get("problem_categories") is None:
        return jsonify({"error": "Missing 'problem_categories' key in complaint"}), 400

    # Inserting categories in 'complaint_problem_categories' table
    print("Inserting categories...")
    for complaint_category in complaint["problem_categories"]:
        print(f"Complaint category: {complaint_category}")
        # validating if category exists in 'dictionary_problem_categories' table
        dictionary_response = supabase.table("dictionary_problem_categories").select("id").eq("category", complaint_category).execute()
        print(f"Dictionary response: {dictionary_response}")
        if dictionary_response.data:
            # if category exists, use its id
            category_id = dictionary_response.data[0]["id"]
            print(f"Category ID: {category_id}")
        else:
            print(f"Category does not exist, creating it...")
            # if category does not exist, create it in 'dictionary_problem_categories' table
            new_category = supabase.table("dictionary_problem_categories").insert({
                "category": complaint_category
            }).execute()

            print(f"New category: {new_category}")

            if not new_category.data:
                raise Exception(f"Failed to insert category '{complaint_category}' into dictionary.")

            category_id = new_category.data[0]["id"]
            print(f"New category ID: {category_id}")
            # get embedding for category
            category_embedding = vectorize_text(complaint_category)
            print(f"Category embedding: {category_embedding}")

            category_embedding_obj = {
                "category_id": category_id,
                "embedding": category_embedding
            }

            # insert embedding into problem_category_embeddings table
            supabase.table("problem_category_embeddings").insert(category_embedding_obj).execute()

            print(f"Category embedding inserted: {category_embedding_obj}")

        # insert relation between complaint and category
        supabase.table("complaint_problem_categories").insert({
            "complaint_id": complaint_id,
            "category_id": category_id
        }).execute()
        print(f"Complaint category relation inserted: {complaint_id} - {category_id}")
        
def setComplaintRelatedEvents(complaint_id, complaint):
    if complaint.get("related_events") is None:
        return jsonify({"error": "Missing 'related_events' key in complaint"}), 400

    # Inserting related events in 'complaint_related_events' table
    print("Inserting related events...")    
    for related_event in complaint["related_events"]:
        print(f"Related event: {related_event}")
        # validating if event exists in 'dictionary_related_events' table
        dictionary_response = supabase.table("dictionary_related_events").select("id").eq("event_name", related_event).execute()
        print(f"Dictionary response: {dictionary_response}")
        if dictionary_response.data:
            # if event exists, use its id
            event_id = dictionary_response.data[0]["id"]
            print(f"Event ID: {event_id}")
        else:
            print(f"Event does not exist, creating it...")
            # if event does not exist, create it in 'dictionary_related_events' table
            new_event = supabase.table("dictionary_related_events").insert({
                "event_name": related_event
            }).execute()

            print(f"New event: {new_event}")

            if not new_event.data:  
                raise Exception(f"Failed to insert event '{related_event}' into dictionary.")

            event_id = new_event.data[0]["id"]
            print(f"New event ID: {event_id}")
            #get embedding for event
            event_embedding = vectorize_text(related_event)
            print(f"Event embedding: {event_embedding}")

            event_embedding_obj = {
                "event_id": event_id,
                "embedding": event_embedding
            }

            # insert embedding into related_event_embeddings table
            supabase.table("related_event_embeddings").insert(event_embedding_obj).execute()
            print(f"Event embedding inserted: {event_embedding_obj}")

        # insert relation between complaint and event
        supabase.table("complaint_related_events").insert({
            "complaint_id": complaint_id,
            "event_id": event_id
        }).execute()
        print(f"Complaint event relation inserted: {complaint_id} - {event_id}")