import psycopg2
from config import DB_CONFIG  

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connection OK:", conn.dsn)
        conn.close()
    except psycopg2.Error as e:
        print("Connection failed:", e)