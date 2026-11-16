import csv
import json
from connect import get_connection

def display_pagination_menu(conn):
    cursor = conn.cursor()
    limit = 5
    offset = 0
    sort_by = input("Sort by [name / birthday / date]: ").strip().lower()
    if sort_by not in ['name', 'birthday', 'date']:
        sort_by = 'name'

    while True:
        cursor.execute("SELECT * FROM get_paginated_contacts(%s, %s, %s)", (limit, offset, sort_by))
        rows = cursor.fetchall()
        
        print(f"\n--- Page (Offset: {offset}, Limit: {limit}, Sorted by: {sort_by}) ---")
        if not rows:
            print("No more records.")
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Birthday: {r[3]} | Group: {r[4]} | Created: {r[5]}")
        
        choice = input("\nCommands: [n]ext page, [p]rev page, [q]uit pagination: ").strip().lower()
        if choice == 'n':
            if len(rows) == limit:
                offset += limit
            else:
                print("You are on the last page.")
        elif choice == 'p':
            offset = max(0, offset - limit)
        elif choice == 'q':
            break
        else:
            print("Invalid command.")

def filter_by_group(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM groups")
    groups = [g[0] for g in cursor.fetchall()]
    print("Available groups:", groups)
    g_name = input("Enter group name to filter: ").strip()
    
    cursor.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name 
        FROM contacts c 
        JOIN groups g ON c.group_id = g.id 
        WHERE g.name ILIKE %s
    """, (g_name,))
    rows = cursor.fetchall()
    print(f"\n--- Contacts in group '{g_name}' ---")
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Birthday: {r[3]}")

def search_contacts_console(conn):
    query = input("Enter search query (name, phone, or email): ").strip()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cursor.fetchall()
    print(f"\n--- Search Results for '{query}' ---")
    for r in rows:
        print(f"Name: {r[1]} | Email: {r[2]} | Birthday: {r[3]} | Group: {r[4]} | Phone: {r[5]} ({r[6]})")

def export_to_json(conn, filename="contacts.json"):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name 
        FROM contacts c 
        LEFT JOIN groups g ON c.group_id = g.id
    """)
    rows = cursor.fetchall()
    
    contacts_list = []
    for row in rows:
        c_id, name, email, birthday, group_name = row
        cursor.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (c_id,))
        phones = [{"phone": p, "type": t} for p, t in cursor.fetchall()]
        
        contacts_list.append({
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": phones
        })
        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts_list, f, indent=4)
    print(f"Successfully exported contacts to {filename}")

def import_from_json(conn, filename="contacts.json"):
    cursor = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            contacts_list = json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    for c in contacts_list:
        name = c.get("name")
        email = c.get("email")
        birthday = c.get("birthday")
        group_name = c.get("group")
        phones = c.get("phones", [])

        cursor.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cursor.fetchone()

        if existing:
            contact_id = existing[0]
            choice = input(f"Contact '{name}' already exists. [s]kip or [o]verwrite? ").lower()
            if choice == 's':
                continue
            elif choice == 'o':
                cursor.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        
        group_id = None
        if group_name:
            cursor.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
            cursor.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            res = cursor.fetchone()
            if res:
                group_id = res[0]

        cursor.execute("""
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday if birthday else None, group_id))
        contact_id = cursor.fetchone()[0]

        for p in phones:
            cursor.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, p["phone"], p["type"]))
            
    conn.commit()
    print("JSON Import completed successfully!")

def import_csv(conn, filename="contacts.csv"):
    cursor = conn.cursor()
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name")
                email = row.get("email")
                birthday = row.get("birthday") or None
                group_name = row.get("group")
                phone = row.get("phone")
                phone_type = row.get("type", "mobile")

                group_id = None
                if group_name:
                    cursor.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
                    cursor.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                    res = cursor.fetchone()
                    if res:
                        group_id = res[0]

                cursor.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                existing = cursor.fetchone()
                if existing:
                    contact_id = existing[0]
                else:
                    cursor.execute("""
                        INSERT INTO contacts (name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, (name, email, birthday, group_id))
                    contact_id = cursor.fetchone()[0]

                if phone:
                    cursor.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, phone, phone_type))
        conn.commit()
        print("CSV Imported successfully!")
    except FileNotFoundError:
        print(f"File {filename} not found.")

def main():
    conn = get_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    while True:
        print("\n=== TSIS 1: PhoneBook Menu ===")
        print("1. Paginated navigation (with sort)")
        print("2. Filter contacts by group")
        print("3. Search contacts (name, phone, email)")
        print("4. Add phone to contact (Procedure)")
        print("5. Move contact to group (Procedure)")
        print("6. Export to JSON")
        print("7. Import from JSON")
        print("8. Import from CSV")
        print("9. Exit")
        
        choice = input("Select option (1-9): ").strip()
        
        if choice == '1':
            display_pagination_menu(conn)
        elif choice == '2':
            filter_by_group(conn)
        elif choice == '3':
            search_contacts_console(conn)
        elif choice == '4':
            name = input("Contact name: ")
            phone = input("Phone number: ")
            ptype = input("Type (home/work/mobile): ")
            cursor = conn.cursor()
            cursor.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
            conn.commit()
            print("Phone added successfully!")
        elif choice == '5':
            name = input("Contact name: ")
            gname = input("Group name: ")
            cursor = conn.cursor()
            cursor.execute("CALL move_to_group(%s, %s)", (name, gname))
            conn.commit()
            print("Contact moved to group successfully!")
        elif choice == '6':
            export_to_json(conn)
        elif choice == '7':
            import_from_json(conn)
        elif choice == '8':
            import_csv(conn)
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")
    
    conn.close()

if __name__ == "__main__":
    main()