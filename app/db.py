from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_SERVICE_ROLE: {os.getenv('SUPABASE_SERVICE_ROLE')}")
print(f"SUPABASE_ANON_KEY: {os.getenv('SUPABASE_ANON_KEY')}")
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_ROLE'))
