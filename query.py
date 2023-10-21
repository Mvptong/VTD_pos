import sqlite3

# Connect to the database
conn = sqlite3.connect('D:\Coding\VTDprogram\gold_stock.db')
cursor = conn.cursor()

# Execute a query
#cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' ")
cursor.execute("SELECT * FROM users ")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
