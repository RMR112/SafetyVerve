import sqlite3
from typing import List, Tuple, Optional

DB_PATH = 'incident_db.sqlite'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def fetch_all(query: str, params: Optional[Tuple] = ()) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()
    return results

def fetch_one(query: str, params: Optional[Tuple] = ()) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    conn.close()
    return result

def execute_query(query: str, params: Optional[Tuple] = ()) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

def execute_many(query: str, data: List[Tuple]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(query, data)
    conn.commit()
    conn.close()
