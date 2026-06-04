import sqlite3

conn = sqlite3.connect("confesiones.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS confesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    texto TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()