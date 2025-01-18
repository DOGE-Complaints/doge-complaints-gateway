import jwt
import datetime
import os
# Ваш секрет из Supabase
jwt_secret = os.getenv('SUPABASE_JWT_SECRET1')

# Create JWT token
payload = {
    "sub": "user_id",  # Unique identifier for the user (can be any)
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expiration time
    "aud": "authenticated",  # Token audience, check Supabase settings
}
token = jwt.encode(payload, jwt_secret, algorithm="HS256")

print("DOGECOMPLAINTS: Your JWT secret:", jwt_secret)
print("DOGECOMPLAINTS: Your JWT:", token)
