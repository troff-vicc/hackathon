import sqlite3

conn = sqlite3.connect('hackathonSQLite.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS login(
            id text,
            name text,
            password text,
            email text
            );
            """)

conn.commit()