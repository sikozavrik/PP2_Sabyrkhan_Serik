"""
TSIS 1: PhoneBook - Extended Contact Management
Console application (psycopg2 + PostgreSQL).

Run:  python phonebook.py
"""
import csv
import json
from contextlib import contextmanager
from datetime import date

import psycopg2

from tsis.config import PAGE_SIZE, PAGINATION_FUNCTION
from tsis.connect import get_connection

PHONE_TYPES = ("home", "work", "mobile")

# Whitelist for sorting (user input is never put into SQL directly)
SORT_OPTIONS = {
    "name": "c.first_name",
    "birthday": "c.birthday NULLS LAST, c.first_name",
    "date": "c.created_at, c.id",
}

LIST_HEADERS = ["ID", "Name", "Email", "Birthday", "Group", "Phones", "Added"]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
@contextmanager
def db():
    """Cursor inside a transaction: commit on success, rollback on error."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    finally:
        conn.close()


def safe(func):
    """Show database errors nicely instead of crashing the program."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.Error as e:
            message = (e.diag.message_primary if e.diag else None) or str(e)
            print(f"\n[Database error] {message}")
        except (OSError, json.JSONDecodeError) as e:
            print(f"\n[File error] {e}")
    return wrapper


def ask(prompt, default=None):
    value = input(prompt).strip()
    return value if value else default


def print_table(headers, rows):
    rows = [["-" if v is None or v == "" else str(v) for v in row] for row in rows]
    if not rows:
        print("\nNothing found.")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(value))
    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    print(line)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(v.ljust(w) for v, w in zip(row, widths)) + " |")
    print(line)
    print(f"{len(rows)} row(s)")


def parse_birthday(value):
    """Return a date or None. Prints a warning for a wrong format."""
    if not value:
        return None
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        print(f"  ! Wrong birthday '{value}' (use YYYY-MM-DD) - ignored.")
        return None


def clean_phones(phones):
    """Keep only valid phones; unknown type becomes 'mobile'."""
    result = []
    for item in phones or []:
        number = str(item.get("phone", "")).strip()
        ptype = str(item.get("type") or "mobile").strip().lower()
        if not number:
            continue
        if ptype not in PHONE_TYPES:
            print(f"  ! Unknown phone type '{ptype}' for {number} - using 'mobile'.")
            ptype = "mobile"
        result.append({"phone": number, "type": ptype})
    return result


def get_group_id(cur, group_name):
    """Find a group (case-insensitive) or create it."""
    name = (group_name or "Other").strip() or "Other"
    cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (name,))
    return cur.fetchone()[0]


def find_contact_id(cur, name):
    cur.execute(
        "SELECT id FROM contacts WHERE LOWER(first_name) = LOWER(%s) LIMIT 1", (name,)
    )
    row = cur.fetchone()
    return row[0] if row else None


def save_contact(cur, rec, existing_id=None):
    """Insert a new contact, or overwrite an existing one (with all phones)."""
    group_id = get_group_id(cur, rec.get("group"))
    birthday = parse_birthday(rec.get("birthday"))
    phones = clean_phones(rec.get("phones"))
    main_phone = phones[0]["phone"] if phones else None  # keeps old column in sync

    if existing_id:
        cur.execute(
            "UPDATE contacts SET email=%s, birthday=%s, group_id=%s, phone=%s WHERE id=%s",
            (rec.get("email") or None, birthday, group_id, main_phone, existing_id),
        )
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing_id,))
        contact_id = existing_id
    else:
        cur.execute(
            "INSERT INTO contacts (first_name, email, birthday, group_id, phone) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (rec["name"], rec.get("email") or None, birthday, group_id, main_phone),
        )
        contact_id = cur.fetchone()[0]

    for p in phones:
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, p["phone"], p["type"]),
        )


# ---------------------------------------------------------------------
# 3.2 Search, filter, sort
# ---------------------------------------------------------------------
def fetch_contacts(where="", params=(), sort="name"):
    sql = f"""
        SELECT c.id, c.first_name, c.email, c.birthday, g.name,
               string_agg(p.type || ': ' || p.phone, ', ' ORDER BY p.id),
               c.created_at::date
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where}
        GROUP BY c.id, c.first_name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {SORT_OPTIONS[sort]}
    """
    with db() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def choose_sort():
    choice = (ask("Sort by name / birthday / date added [name]: ", "name")).lower()
    if choice in ("date added", "added"):
        choice = "date"
    if choice not in SORT_OPTIONS:
        print("Unknown option, using 'name'.")
        choice = "name"
    return choice


@safe
def show_all():
    print_table(LIST_HEADERS, fetch_contacts(sort=choose_sort()))


@safe
def filter_by_group():
    with db() as cur:
        cur.execute("SELECT name FROM groups ORDER BY id")
        groups = [r[0] for r in cur.fetchall()]
    print("Groups: " + ", ".join(f"{i}) {g}" for i, g in enumerate(groups, 1)))
    choice = ask("Choose a group (number or name): ")
    if not choice:
        return
    if choice.isdigit() and 1 <= int(choice) <= len(groups):
        choice = groups[int(choice) - 1]
    rows = fetch_contacts("WHERE LOWER(g.name) = LOWER(%s)", (choice,), choose_sort())
    print_table(LIST_HEADERS, rows)


@safe
def search_by_email():
    text = ask("Email contains (e.g. gmail): ")
    if not text:
        return
    rows = fetch_contacts("WHERE c.email ILIKE %s", (f"%{text}%",), choose_sort())
    print_table(LIST_HEADERS, rows)


@safe
def search_everything():
    text = ask("Search (name, email or any phone): ")
    if not text:
        return
    with db() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (text,))
        rows = cur.fetchall()
    print_table(["ID", "Name", "Email", "Birthday", "Group", "Phones"], rows)


@safe
def browse_pages():
    """Paginated navigation using the Practice 8 database function."""
    page = 0
    while True:
        try:
            with db() as cur:
                cur.execute(
                    f"SELECT * FROM {PAGINATION_FUNCTION}(%s, %s)",
                    (PAGE_SIZE, page * PAGE_SIZE),
                )
                headers = [d[0] for d in cur.description]
                rows = cur.fetchall()
        except psycopg2.Error as e:
            print(f"\n[Database error] {e.diag.message_primary or e}")
            print(f"Check PAGINATION_FUNCTION ('{PAGINATION_FUNCTION}') in config.py.")
            return

        if not rows and page > 0:
            print("\nThis is the last page.")
            page -= 1
            continue

        print(f"\n--- Page {page + 1} ---")
        print_table(headers, rows)
        command = (ask("[n]ext / [p]rev / [q]uit: ", "q")).lower()
        if command in ("n", "next"):
            if len(rows) < PAGE_SIZE:
                print("This is the last page.")
            else:
                page += 1
        elif command in ("p", "prev"):
            if page == 0:
                print("This is the first page.")
            else:
                page -= 1
        elif command in ("q", "quit"):
            return


# ---------------------------------------------------------------------
# Add contact / phone / group (console input for the new data model)
# ---------------------------------------------------------------------
@safe
def add_contact():
    name = ask("Name: ")
    if not name:
        print("Name is required.")
        return
    rec = {
        "name": name,
        "email": ask("Email (optional): "),
        "birthday": ask("Birthday YYYY-MM-DD (optional): "),
        "group": ask("Group (Family/Work/Friend/Other) [Other]: ", "Other"),
        "phones": [],
    }
    while True:
        number = ask("Phone (empty to finish): ")
        if not number:
            break
        ptype = ask("Type home/work/mobile [mobile]: ", "mobile").lower()
        rec["phones"].append({"phone": number, "type": ptype})

    with db() as cur:
        existing = find_contact_id(cur, name)
        if existing:
            print(f"Contact '{name}' already exists. Use import to overwrite.")
            return
        save_contact(cur, rec)
    print("Contact added.")


@safe
def add_phone_console():
    name = ask("Contact name: ")
    number = ask("New phone: ")
    ptype = ask("Type home/work/mobile [mobile]: ", "mobile").lower()
    with db() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, number, ptype))
    print("Phone added.")


@safe
def move_to_group_console():
    name = ask("Contact name: ")
    group = ask("Group name (created if it does not exist): ")
    with db() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
    print("Contact moved.")


# ---------------------------------------------------------------------
# 3.3 Import / Export
# ---------------------------------------------------------------------
@safe
def export_json():
    path = ask("File name [contacts_export.json]: ", "contacts_export.json")
    with db() as cur:
        cur.execute(
            "SELECT c.id, c.first_name, c.email, c.birthday, g.name "
            "FROM contacts c LEFT JOIN groups g ON g.id = c.group_id ORDER BY c.first_name"
        )
        contacts = cur.fetchall()
        cur.execute("SELECT contact_id, phone, type FROM phones ORDER BY id")
        phones = {}
        for contact_id, number, ptype in cur.fetchall():
            phones.setdefault(contact_id, []).append({"phone": number, "type": ptype})

    data = [
        {
            "name": name,
            "email": email,
            "birthday": birthday.isoformat() if birthday else None,
            "group": group,
            "phones": phones.get(cid, []),
        }
        for cid, name, email, birthday, group in contacts
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} contact(s) to {path}")


def import_records(records):
    """Insert records; on duplicate name ask: skip or overwrite."""
    added = updated = skipped = 0
    with db() as cur:
        for rec in records:
            name = (rec.get("name") or "").strip()
            if not name:
                continue
            rec["name"] = name
            existing_id = find_contact_id(cur, name)
            if existing_id:
                while True:
                    answer = ask(f"Contact '{name}' already exists. [s]kip or [o]verwrite? ", "s").lower()
                    if answer in ("s", "skip", "o", "overwrite"):
                        break
                if answer.startswith("s"):
                    skipped += 1
                    continue
                save_contact(cur, rec, existing_id)
                updated += 1
            else:
                save_contact(cur, rec)
                added += 1
    print(f"Done: {added} added, {updated} overwritten, {skipped} skipped.")


@safe
def import_json():
    path = ask("JSON file [contacts_export.json]: ", "contacts_export.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("JSON must contain a list of contacts.")
        return
    import_records(data)


@safe
def import_csv():
    """CSV columns: first_name, phone, phone_type, email, birthday, group.
    Several rows with the same name = several phones of one contact."""
    path = ask("CSV file [contacts.csv]: ", "contacts.csv")
    records = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = (row.get("first_name") or "").strip()
            if not name:
                continue
            rec = records.setdefault(
                name.lower(),
                {"name": name, "email": None, "birthday": None, "group": None, "phones": []},
            )
            for field in ("email", "birthday", "group"):
                value = (row.get(field) or "").strip()
                if value:
                    rec[field] = value
            number = (row.get("phone") or "").strip()
            if number:
                rec["phones"].append(
                    {"phone": number, "type": (row.get("phone_type") or "mobile").strip().lower()}
                )
    import_records(list(records.values()))


# ---------------------------------------------------------------------
# Extra feature: statistics by group
# ---------------------------------------------------------------------
@safe
def show_stats():
    with db() as cur:
        cur.execute(
            "SELECT g.name, COUNT(c.id) FROM groups g "
            "LEFT JOIN contacts c ON c.group_id = g.id "
            "GROUP BY g.id, g.name ORDER BY COUNT(c.id) DESC, g.name"
        )
        stats = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM contacts")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM phones")
        total_phones = cur.fetchone()[0]

    print("\n=== Contacts per group ===")
    for name, count in stats:
        percent = (count / total * 100) if total else 0
        bar = "#" * round(percent / 5)
        print(f"{name:<10} {count:>3}  {percent:5.1f}%  {bar}")
    print("-" * 40)
    print(f"Total contacts: {total} | Total phone numbers: {total_phones}")
    if stats and total:
        print(f"Biggest group: {stats[0][0]} ({stats[0][1]} contacts)")


# ---------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------
MENU = """
========== PHONEBOOK ==========
 1. Show all contacts (sortable)
 2. Filter by group
 3. Search by email
 4. Search everywhere (name / email / phones)
 5. Browse pages (next / prev / quit)
 6. Add contact
 7. Add phone to contact
 8. Move contact to group
 9. Export to JSON
10. Import from JSON
11. Import from CSV
12. Group statistics
 0. Exit
"""

ACTIONS = {
    "1": show_all,
    "2": filter_by_group,
    "3": search_by_email,
    "4": search_everything,
    "5": browse_pages,
    "6": add_contact,
    "7": add_phone_console,
    "8": move_to_group_console,
    "9": export_json,
    "10": import_json,
    "11": import_csv,
    "12": show_stats,
}


def main():
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
