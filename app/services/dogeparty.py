import os, requests
from ecdsa import SigningKey, SECP256k1
from hashlib import sha256

DOGEPARTY_API_URL = os.getenv("DOGEPARTY_API_URL")
HEADERS = {'Content-Type': 'application/json'}
DOGEPARTY_WALLET_ADDRESS = os.getenv("DOGEPARTY_WALLET_ADDRESS")
DOGEPARTY_PRIVATE_KEY = os.getenv("DOGEPARTY_PRIVATE_KEY")
AUTH = ('rpc', 'rpc')

TOKEN_QUANTITY = os.getenv("TOKEN_QUANTITY")

def call_api(method, params):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(DOGEPARTY_API_URL, headers=HEADERS, json=payload, auth=AUTH)
    return response.json()

def createComplaintToken(complaint, json_url):

    # get description for the token

    description = complaint['description']
    categories = complaint['categories']
    related_events = complaint['related_events']
    json_url = json_url

    full_description = f"{description}\n\nCategories: {', '.join(categories)}\nRelated Events: {', '.join(related_events)}\nMetadata: {json_url}"

    create_named_token(complaint['id'], TOKEN_QUANTITY, full_description, True)

def create_named_token(asset, quantity, description, divisible):
    """
    Create, sign and send a transaction to create a named token.

    :param asset: Name of the token (must be unique)
    :param quantity: Quantity of tokens
    :param description: Description of the token
    :param divisible: Divisibility of the token (True or False)
    :return: Signed transaction (signed_tx)
    """
    
    params = {
        "source": DOGEPARTY_WALLET_ADDRESS,
        "asset": asset,
        "quantity": quantity,
        "description": description,
        "divisible": divisible
    }

    # 1. Call API to create a token
    response = call_api("create_issuance", params)
    print(f"Response from API: {response}")

    if 'result' in response:
        raw_tx = response['result']
        print(f"Необработанная транзакция (raw_tx): {raw_tx}")

        # 2. Sign the transaction
        try:
            signed_tx = sign_transaction(raw_tx)
            print(f"Signed transaction (signed_tx): {signed_tx}")
        except Exception as e:
            raise Exception(f"Ошибка при подписании транзакции: {e}")

        # 3. Send the transaction
        try:
            result = send_signed_transaction(signed_tx)
            print(f"Result of sending the transaction: {result}")
            return signed_tx
        except Exception as e:
            raise Exception(f"Ошибка при отправке транзакции: {e}")
    else:
        error_message = response.get('error', {}).get('message', 'Unknown error')
        raise Exception(f"Error creating token: {error_message}")


# Метод для подписи транзакции
def sign_transaction(raw_tx):
    """
    Sign a transaction using the private key.

    :param raw_tx: Unsigned transaction as a string (hex)
    :return: Signed transaction
    """
    if not DOGEPARTY_PRIVATE_KEY:
        raise ValueError("Private key not set. Check the DOGEPARTY_PRIVATE_KEY environment variable.")

    try:
        # Convert the private key from hex to SigningKey object
        private_key_bytes = bytes.fromhex(DOGEPARTY_PRIVATE_KEY)
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

        # Hash the transaction to create a signature
        raw_tx_bytes = bytes.fromhex(raw_tx)
        tx_hash = sha256(raw_tx_bytes).digest()

        # Sign the hash
        signature = signing_key.sign_digest(tx_hash, sigencode=lambda r, s, order: r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))

        # Add the signature to the transaction (implementation depends on the API)
        signed_tx = raw_tx + signature.hex()

        return signed_tx
    except Exception as e:
        raise RuntimeError(f"Error signing transaction: {e}")

def send_signed_transaction(signed_tx):
    """
    Send a signed transaction to the Dogeparty network.

    :param signed_tx: Signed transaction (in hex format)
    :return: Response from Dogeparty API
    """
    payload = {
        "method": "sendrawtransaction",
        "params": [signed_tx],
        "jsonrpc": "2.0",
        "id": 0
    }
    
    try:
        # Send request
        response = requests.post(DOGEPARTY_API_URL, json=payload, auth=AUTH)
        response.raise_for_status()  # Check the response status
        
        # Process the response
        result = response.json()
        if 'result' in result:
            return f"Transaction sent successfully! TXID: {result['result']}"
        else:
            return f"Error: {result.get('error', {}).get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"

def get_utxo():
    """
    Get a list of unspent transactions (UTXO) for the specified wallet.

    :param wallet_address: Dogeparty wallet address
    :return: List of UTXO with txid and vout or an empty list
    """
    payload = {
        "method": "get_unspent_txouts",
        "params": {
            "addresses": [DOGEPARTY_WALLET_ADDRESS],
            "unconfirmed": True  # If you want to include unconfirmed transactions
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    try:
        response = requests.post(DOGEPARTY_API_URL, json=payload, auth=AUTH)
        response.raise_for_status()
        result = response.json().get('result', [])
        if result:
            # Return list of txid and vout
            return [{"txid": utxo["txid"], "vout": utxo["vout"]} for utxo in result]
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to API: {e}")
        return []
