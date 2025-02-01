import requests
import os

url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET_API_KEY = os.getenv('PINATA_SECRET_API_KEY')
PINATA_JWT = os.getenv('PINATA_JWT')

def upload_to_pinata(json_data):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    
    payload = {
        "pinataOptions": {"cidVersion": 1},
        "pinataMetadata": {"name": "pinnie.json"},
        "pinataContent": json_data
    }
    
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    print("Response: ", response.json())

    ipfs_hash = response.json()['IpfsHash']
    return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
