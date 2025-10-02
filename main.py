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
    """
    Requests pilot data from the VATSIM API.
    Returns:
        list: List of pilot dictionaries from the API response.
    Exits the program if the request fails.
    """
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
    """
    Filters out pilots with duplicate names from the provided list.
    Args:
        pilots (list): List of pilot dictionaries.
    Returns:
        list: List of unique pilot dictionaries (by name).
    """
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
    """
    Connects to the PostgreSQL database using pyodbc.
    Returns:
        tuple: (connection, cursor) to the database.
    Exits the program if the connection fails.
    """
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

def create_table_if_not_exists(current_cursor):
    """
    Creates the 'pilots' table in the database if it does not already exist.
    Args:
        current_cursor: The database cursor object.
    """
    print("Creating table 'pilots' if it does not exist...")
    current_cursor.execute("""
        CREATE TABLE IF NOT EXISTS pilots (
            id SERIAL PRIMARY KEY,
            cid INTEGER NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL
        );
    """)
    print("Table checked/created.")

def upsert_pilot(current_cursor, cid, name):
    """
    Inserts or updates a pilot in the 'pilots' table based on cid.
    Args:
        current_cursor: The database cursor object.
        cid (int): The pilot's CID.
        name (str): The pilot's name.
    """
    print(f"Upserting pilot: {name} (cid: {cid})")
    current_cursor.execute("""
        INSERT INTO pilots (cid, name)
        VALUES (?, ?)
        ON CONFLICT (cid) DO UPDATE SET name = EXCLUDED.name;
    """, (cid, name))

def disconnect_from_db(connection, cursor_db):
    """
    Closes the database cursor and connection, handling exceptions.
    Args:
        connection: The database connection object.
        cursor_db: The database cursor object.
    """
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
    create_table_if_not_exists(cursor)
    for pilot in processed_data:
        upsert_pilot(cursor, pilot['cid'], pilot['name'])
    disconnect_from_db(conn, cursor)
    print("Script finished.")