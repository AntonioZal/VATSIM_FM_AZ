#!/usr/bin/python3.12

import requests, sys, pyodbc
from collections import Counter

url = "https://data.vatsim.net/v3/vatsim-data.json"
pg_user = "pgadm"
pg_password = "M0cNLF9sHr0YkJl2"
pg_host = "localhost"
pg_port = "5432"
pg_database = "vatsim"

def vatsim_api_request():
    print("Requesting VATSIM data from API...")
    try:
        results = requests.get(url)

        if results.status_code == 200:
            print("Successfully retrieved VATSIM data.")
            return results.json()['pilots']
        else:
            print("Error retrieving VATSIM data from API.")
            sys.exit(1)

    except Exception as e:
        print(f"Error executing API request: {e}")
        sys.exit(1)

def filter_unique_pilots(pilots):
    print("Filtering pilots to remove duplicates...")
    names = [p['name'] for p in pilots]
    counts = Counter(names)

    for name, count in counts.items():
        if count > 1:
            print(f"Pilot {name} appears {count} times. Removing this pilot from data.")

    duplicate_names = {name for name, count in counts.items() if count > 1}
    unique_pilots = [p for p in pilots if p['name'] not in duplicate_names]

    print(f"{len(unique_pilots)} unique pilots remaining after filtering.")
    return unique_pilots

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        connection = pyodbc.connect(
            f"DRIVER={{PostgreSQL Unicode}};SERVER={pg_host};PORT={pg_port};DATABASE={pg_database};UID={pg_user};"
            f"PWD={pg_password}"
        )
        connection.autocommit = True
        cursor_db = connection.cursor()
        print("Successfully connected to the database.")
        return connection, cursor_db

    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def disconnect_from_db(connection, cursor_db):
    print("Disconnecting from the database...")
    try:
        cursor_db.close()
        connection.close()
        print("Successfully disconnected from the database.")

    except Exception as e:
        print(f"Error disconnecting from database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting VATSIM pilot data processing script...")
    data = vatsim_api_request()
    processed_data = filter_unique_pilots(data)
    conn, cursor = connect_to_db()
    disconnect_from_db(conn, cursor)
    print("Script finished.")