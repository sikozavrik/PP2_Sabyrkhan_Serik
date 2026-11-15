import os


DB_CONFIG = {
    "host": os.getenv("PB_HOST", "localhost"),
    "port": int(os.getenv("PB_PORT", "5432")),
    "dbname": os.getenv("PB_DBNAME", "phonebook"),
    "user": os.getenv("PB_USER", "postgres"),
    "password": os.getenv("PB_PASSWORD", "your_password_here"),
}

PAGE_SIZE = 3


PAGINATION_FUNCTION = "get_contacts_paginated"
