# =========================================
# IMPORTS
# =========================================
import streamlit as st
import sqlite3
import os
from retriever import search
from generator import generate_answer


# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="HR Chat Bot", page_icon="🤖", layout="centered")


# =========================================
# BLUE BACKGROUND
# =========================================
st.markdown("""
<style>
.stApp {
    background-color:#0a1f44;
    color:white;
}
</style>
""", unsafe_allow_html=True)


# =========================================
# DATABASE SETUP
# =========================================
BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, "users.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
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
        return False

    cursor.execute(
        "INSERT INTO users VALUES (?,?,?)",
        (name, email, college)
    )
    conn.commit()

    print("Saved:", name, email, college)
    return True


# =========================================
# TITLE
# =========================================
st.title("🤖 HR Chat Bot")
st.header("Welcome to the Unlox Academy")
st.subheader("Feel free to ask your queries")

st.divider()


# =========================================
# USER FORM
# =========================================
st.markdown("### Enter Your Details")

name = st.text_input("Name")
email = st.text_input("Email")
college = st.text_input("College")

if st.button("Submit Details"):

    if name and email and college:

        status = save_user(name, email, college)

        if status:
            st.success(f"Hello {name} 👋")
        else:
            st.warning("User already registered")

        st.session_state.user_ready = True

    else:
        st.warning("Please fill all fields")


st.divider()


# =========================================
# CHATBOT SECTION
# =========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.get("user_ready"):

    st.markdown("### 💬 HR Assistant")

    # show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # user input
    prompt = st.chat_input("Ask HR anything...")

    if prompt:

        # store user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # generate response
        context = search(prompt)
        answer = generate_answer(prompt, context)

        # show bot reply
        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    st.info("Please enter your details above to start chatting.")
