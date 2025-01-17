from opencage.geocoder import OpenCageGeocode
from app.db import supabase
import requests
import os
NOMINATUM_URL = "https://nominatim.openstreetmap.org/search"



DEFAULT_CITY = "Tallinn"
DEFAULT_COUNTRY = "Estonia"

def get_coordinates(location_details):

    # Check if address is already registered in dictionary and return coordinates
    
    print("location_details:", location_details)
    dictionary_response = supabase.table("location_directory").select("*").eq("location_details", location_details).execute()
    print("dictionary_response:", dictionary_response)
    if dictionary_response.data:
        # print address retrieved from dictionary with all parameters printed one by one
        print(f"location_details {location_details} already registered in dictionary table location_directory")
        print(f"Address retrieved from dictionary: {dictionary_response.data[0]}")
        print(f"Latitude: {dictionary_response.data[0]['latitude']}")
        print(f"Longitude: {dictionary_response.data[0]['longitude']}")

        return dictionary_response.data[0]["latitude"], dictionary_response.data[0]["longitude"]

    # Otherwise return getNominatumCoordinates(address)
    return getOpenCageCoordinates(location_details)

def getOpenCageCoordinates(location_details):
    geocoder = OpenCageGeocode(key=os.getenv('OPENCAGE_API_KEY'))
    results = geocoder.geocode(location_details)
    if results:
        return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    return None, None

# Глобальная переменная для токена
cached_token = None
cached_token_expiration = None


def getNominatumCoordinates(address):
    # if not, get coordinates from nominatum
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "Estonians888/1.0 (zeya.metsapuu@gmail.com)"
    }
    try:
        response = requests.get(NOMINATUM_URL, params=params, headers=headers)
        print(f"Response status: {response.status_code}, Response content: {response.text}")
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            # insert address into dictionary table address_directory
            supabase.table("address_directory").insert({
                "address": address,
                "latitude": data["lat"],
                "longitude": data["lon"],
                "city": DEFAULT_CITY,
                "country": DEFAULT_COUNTRY
            }).execute()
            return float(data["lat"]), float(data["lon"])
        return None, None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None, None