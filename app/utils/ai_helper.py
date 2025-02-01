from dotenv import load_dotenv
import requests
import jwt
import datetime
import os
import openai
import anthropic
load_dotenv()

# Setting up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Setting up Anthropic API (Claude)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')
print(f"SUPABASE_JWT_SECRET: {SUPABASE_JWT_SECRET}")
SUPABASE_FUNCTION_URL = os.getenv('SUPABASE_FUNCTION_URL')
print(f"SUPABASE_FUNCTION_URL: {SUPABASE_FUNCTION_URL}")

cached_token = None
cached_token_expiration = None

def get_cached_jwt():

    print(f"Getting cached JWT...")
    global cached_token, cached_token_expiration

    # Проверяем, есть ли токен в кэше и он ещё действителен
    if cached_token and cached_token_expiration > datetime.datetime.utcnow():
        print(f"Cached JWT found: {cached_token}")
        return cached_token

    # Создаём новый токен
    payload = {
        "sub": "user_id",  # Уникальный ID пользователя
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Время жизни токена
        "aud": "authenticated",  # Аудитория
    }
    cached_token = jwt.encode(payload, SUPABASE_JWT_SECRET, algorithm="HS256")
    cached_token_expiration = payload["exp"]

    print(f"New token created: {cached_token}")
    print(f"Token expiration: {cached_token_expiration}")

    return cached_token

def vectorize_text(text: str):
    print(f"Vectorizing text: {text}")
    print(f"SUPABASE_SERVICE_ROLE: get_cached_jwt()")
    headers = {
        "Authorization": f"Bearer {get_cached_jwt()}",
        "Content-Type": "application/json",
    }
    print(f"Headers: {headers}")
    payload = {"input": text}
    print(f"Payload: {payload}")

    try:
        response = requests.post(SUPABASE_FUNCTION_URL, json=payload, headers=headers)
        
        # Проверка успешности запроса
        if response.status_code == 200:
            embeddings = response.json().get("embedding")
            
            return embeddings
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Response headers: {response.headers}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def sumamrise_text(text: str):
    print(f"Sumamrising text: {text}")
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Summarise the complaint: " + text}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None