import psycopg2
from connect import get_connection

def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def upsert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def bulk_insert_contacts(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
    conn.commit()
    cur.close()
    conn.close()

def get_paginated_contacts(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def delete_contact(identifier):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s);", (identifier,))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    upsert_contact("Dino", "+77011234567")
    print("Search results:", search_contacts("Dino"))
    
    names = ["Siko", "Serik", "Sikozavr"]
    phones = ["+77029876543", "+77071112233", "invalid_phone"]
    bulk_insert_contacts(names, phones)
    
    print("Paginated records:", get_paginated_contacts(2, 0))
    delete_contact("Dino")