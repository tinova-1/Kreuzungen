IMPORT_CSV_SEP = ","
COMMENT = "#"

import csv
import sqlite3


content = None
with open("Kreuzungen_zurueck.txt", "r", encoding="utf8") as fh:
    reader = csv.reader(fh, delimiter=",")
    content = [row for row in reader]
    
content = content[1:-6]

con = sqlite3.connect("Kreuzungen.db")
try:
    cur = con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS Kreuzungen (Country TEXT, Location TEXT, latitude NUMERIC, longitude NUMERIC, function TEXT, technique TEXT, rating INTEGER, Link TEXT);")
    
    
    for row in content:
        row = [str(c).strip() for c in row]
        while len(row) < 8:
            row.append(None)
        cur.execute("INSERT INTO Kreuzungen VALUES (?,?,?,?,?,?,?,?);", row)
        
    con.commit()
finally:
    con.close()

    
