import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'movies.db')
DB_PATH = os.path.abspath(DB_PATH)
print('Using DB at:', DB_PATH)
if not os.path.exists(DB_PATH):
    print('Database file not found.')
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("PRAGMA table_info('user')")
cols = [r[1] for r in cur.fetchall()]
print('Columns on user table:', cols)
if 'is_admin' not in cols:
    print('Adding is_admin column...')
    cur.execute("ALTER TABLE user ADD COLUMN is_admin INTEGER DEFAULT 0")
    conn.commit()
    print('is_admin added.')
else:
    print('is_admin already exists.')
cur.close()
conn.close()
