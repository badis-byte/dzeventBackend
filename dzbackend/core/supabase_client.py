# core/supabase_client.py
from supabase import create_client, Client

SUPABASE_URL = "https://jkcqgchkidxxtrjhmmha.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImprY3FnY2hraWR4eHRyamhtbWhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1NTY2MjUsImV4cCI6MjA4MTEzMjYyNX0.JxIMVWPhZJYKNOXF-aGHlH_Nptunx_9PZRuzDoL1kvU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
