#process complaint

from app.db import supabase
from flask import Blueprint, request, jsonify
from app.utils.ai_helper import vectorize_text
from app.utils.geocoding import get_coordinates
from app.utils.enumerators import ComplaintTimeType

proces_complaint_bp = Blueprint('process_complaint', __name__)

@proces_complaint_bp.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    print("Submitting complaint...")
    # Get JSON from request
    data = request.json
    print(f"Received data: {data}")
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    complaint = data.get("complaint")
    if not complaint:
        return jsonify({"error": "Missing 'complaint' key in JSON"}), 400

    print(f"Complaint: {complaint}")

    # Setting all fields to complaints table via supabase
    complaint_data = {
        "user_first_name": complaint.get("user").get("first_name"),
        "user_last_name": complaint.get("user").get("last_name"),
        "complaint_description": complaint.get("description"),
        "severity": complaint.get("severity"),
        "impact_estimation": complaint.get("impact_estimation"),
        "problem_status": complaint.get("problem_status")
    }

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

    # Inserting schedule into 'complaint_time' table

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

    supabase.table("complaint_time").insert(complaint_time_data).execute()

    # Inserting categories in 'complaint_problem_categories' table
    for complaint_category in complaint["problem_categories"]:
        # validating if category exists in 'dictionary_problem_categories' table
        dictionary_response = supabase.table("dictionary_problem_categories").select("id").eq("category", complaint_category).execute()

        if dictionary_response.data:
            # if category exists, use its id
            category_id = dictionary_response.data[0]["id"]
        else:
            # if category does not exist, create it in 'dictionary_problem_categories' table
            new_category = supabase.table("dictionary_problem_categories").insert({
                "category": complaint_category
            }).execute()

            print(f"New category: {new_category}")

            if not new_category.data:
                raise Exception(f"Failed to insert category '{complaint_category}' into dictionary.")

            category_id = new_category.data[0]["id"]

            # get embedding for category
            category_embedding = vectorize_text(complaint_category)
            print(f"Category embedding: {category_embedding}")

            category_embedding_obj = {
                "category_id": category_id,
                "embedding": category_embedding
            }

            # insert embedding into problem_category_embeddings table
            supabase.table("problem_category_embeddings").insert(category_embedding_obj).execute()

        # insert relation between complaint and category
        supabase.table("complaint_problem_categories").insert({
            "complaint_id": complaint_id,
            "category_id": category_id
        }).execute()
    
    # Inserting related events in 'complaint_related_events' table
    for related_event in complaint["related_events"]:
        # validating if event exists in 'dictionary_related_events' table
        dictionary_response = supabase.table("dictionary_related_events").select("id").eq("event_name", related_event).execute()

        if dictionary_response.data:
            # if event exists, use its id
            event_id = dictionary_response.data[0]["id"]
        else:
            # if event does not exist, create it in 'dictionary_related_events' table
            new_event = supabase.table("dictionary_related_events").insert({
                "event_name": related_event
            }).execute()

            print(f"New event: {new_event}")

            if not new_event.data:  
                raise Exception(f"Failed to insert event '{related_event}' into dictionary.")

            event_id = new_event.data[0]["id"]

            #get embedding for event
            event_embedding = vectorize_text(related_event)
            print(f"Event embedding: {event_embedding}")

            event_embedding_obj = {
                "event_id": event_id,
                "embedding": event_embedding
            }

            # insert embedding into related_event_embeddings table
            supabase.table("related_event_embeddings").insert(event_embedding_obj).execute()

        # insert relation between complaint and event
        supabase.table("complaint_related_events").insert({
            "complaint_id": complaint_id,
            "event_id": event_id
        }).execute()

    return jsonify({"message": "Complaint added successfully"}), 201