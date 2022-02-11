
  
import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/video-record.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

def show_items():
    try:
        items = c.execute("""SELECT
                                r.id, r.name, r.description, r.price
                             FROM
                                records AS r
        """)

        print("RECORDS")
        print("#############")
        for row in items:
            print("ID:             ", row[0]),
            print("Name:           ", row[1]),
            print("Description:    ", row[2]),
            print("Price:          ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()

show_items()

conn.close()