import streamlit as st
import sqlite3
from retriever import search
from generator import generate_answer

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
name TEXT,
email TEXT,
college TEXT
)
""")
conn.commit()

def save_user(name,email,college):
    cursor.execute("INSERT INTO users VALUES(?,?,?)",(name,email,college))
    conn.commit()

def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HR Chat Bot", page_icon="🤖", layout="centered")

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color:#add8e6;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🤖 HR Chat Bot")

# ---------------- HEADER ----------------
st.header("Welcome to the Unlox Academy")

# ---------------- SUBHEADER ----------------
st.subheader("Feel free to ask your queries")

st.divider()

# ---------------- USER DETAILS ----------------
st.markdown("### Enter Your Details")

name = st.text_input("Name")
email = st.text_input("Email")
college = st.text_input("College")

if st.button("Submit Details"):
    if name and email and college:
        save_user(name,email,college)

        st.success(f"Hello {name} 👋")
        st.write(f"📧 {email}")
        st.write(f"🎓 {college}")

        st.session_state.user_ready = True
    else:
        st.warning("Please fill all details")

st.divider()

# ---------------- VIEW USERS BUTTON ----------------
if st.button("📊 View Registered Users"):
    users = get_users()

    if users:
        st.markdown("### Stored Users")
        st.table(users)
    else:
        st.info("No users registered yet")

st.divider()

# ---------------- CHATBOT ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.get("user_ready"):

    st.markdown("### 💬 HR Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask HR anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        context = search(prompt)
        answer = generate_answer(prompt, context)

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.info("Please enter your details above to start chatting.")

# ---------------- HIDDEN ADMIN ACCESS ----------------

st.divider()

admin_key = st.text_input("", placeholder="Enter admin access key", type="password")

if admin_key == "unloxadmin":   # ← change this secret key

    st.success("Admin Access Granted")

    users = get_users()

    if users:
        st.markdown("### Registered Users")
        st.table(users)
    else:
        st.info("No users registered yet")

