# =========================================
# IMPORTS
# =========================================
import sqlite3
from retriever import search
from generator import generate_answer


# =========================================
# DATABASE SETUP
# =========================================
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    email TEXT,
    college TEXT
)
""")


# =========================================
# SAVE USER FUNCTION
# =========================================
def save_user(name, email, college):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone():
        print("\nUser already registered.\n")
        return

    cursor.execute(
        "INSERT INTO users VALUES (?,?,?)",
        (name, email, college)
    )
    conn.commit()
    print("\nDetails saved successfully!\n")


# =========================================
# SHOW USERS FUNCTION
# =========================================
def show_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("\nStored Users:\n")
    print("Name | Email | College")
    print("-"*40)

    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")
    print()


# =========================================
# USER REGISTRATION
# =========================================
print("\n===== HR CHATBOT REGISTRATION =====\n")

name = input("Enter your name: ")
email = input("Enter your email: ")
college = input("Enter your college: ")

save_user(name, email, college)

print(f"Welcome {name}! 🎉")


# =========================================
# CHATBOT LOOP
# =========================================
print("\nHR Chatbot Ready!")
print("Type 'exit' to stop")
print("Type 'show users' to view stored users\n")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        print("\nBot: Goodbye! Have a great day 😊\n")
        break

    elif query.lower() == "show users":
        show_users()
        continue

    context = search(query)
    answer = generate_answer(query, context)

    print("Bot:", answer, "\n")
