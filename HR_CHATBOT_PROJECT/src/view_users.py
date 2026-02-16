import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

print("\nStored Users:\n")
print("Name | Email | College")
print("-"*40)

for row in cursor.execute("SELECT * FROM users"):
    print(f"{row[0]} | {row[1]} | {row[2]}")
