import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/video-record.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS records")

c.execute("""CREATE TABLE records (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT,
                    description     TEXT,
                    price           REAL
)""")

records = [
  (0, "record 1", "record 1 description", 0),
  (1, "record 2", "record 2 description", 1),
  (2, "record 3", "record 3 description", 2),
  (3, "record 4", "record 4 description", 3),
  (4, "record 5", "record 5 description", 4),
  (5, "record 6", "record 6 description", 5),
  (6, "record 7", "record 7 description", 6),
  (7, "record 8", "record 8 description", 7),
  (8, "record 9", "record 9 description", 8),
  (9, "record 10", "record 10 description", 9),   
]

c.executemany("INSERT INTO records (id, name, description, price) VALUES (?,?,?,?)", records)

conn.commit()
conn.close()

print("Database is created and initialized.")
print("You can see the tables with the show_tables.py script.")