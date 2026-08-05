import os

import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    raise RuntimeError("SUPABASE_DB_URL is not set. Add it to your .env file.")


def get_connection():
    """
    Opens a fresh connection and registers the pgvector type adapter on it,
    so Python lists can be passed/returned as vector columns transparently.
    """
    conn = psycopg2.connect(SUPABASE_DB_URL)
    register_vector(conn)
    return conn