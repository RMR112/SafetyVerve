import sqlite3

def initialize_database(sql_file,db_path='incident_db.sqlite'):
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the SQL script
    with open(sql_file, 'r') as f:
        sql_script = f.read()

    # Execute the script
    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Database initialized successfully at '{db_path}'.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database(sql_file='data/seed_incidents.sql')
    print("Database initialized successfully.")