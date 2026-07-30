import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Domain Specific AI Agent",
    layout='wide'
)

# -------------------
# CUSTOM THEME
# -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 40%, #fef3c7 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 60%, #4c1d95 100%) !important;
    border-right: 2px solid #7c3aed;
}

[data-testid="stSidebar"] * {
    color: #ede9fe !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] header {
    color: #fbbf24 !important;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.85rem;
}

[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(167,139,250,0.4) !important;
    color: #fff !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
}

[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6);
}

/* ── Page Title Banner ── */
h1 {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    padding-bottom: 0.2rem;
}

/* ── Section Headers ── */
h2, h3 {
    color: #1e1b4b !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* ── Cards / Containers ── */
[data-testid="stVerticalBlock"] > div:has(.stMarkdown),
.element-container {
    border-radius: 12px;
}

/* ── Alerts ── */
.stSuccess {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0) !important;
    border-left: 4px solid #10b981 !important;
    border-radius: 10px !important;
    color: #065f46 !important;
}

.stWarning {
    background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
    border-left: 4px solid #f59e0b !important;
    border-radius: 10px !important;
    color: #78350f !important;
}

.stError {
    background: linear-gradient(135deg, #fee2e2, #fecaca) !important;
    border-left: 4px solid #ef4444 !important;
    border-radius: 10px !important;
    color: #7f1d1d !important;
}

/* ── Main Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
    animation: pulse-glow 2.5s ease-in-out infinite;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.55) !important;
    animation: none;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35); }
    50%       { box-shadow: 0 4px 22px rgba(168, 85, 247, 0.65); }
}

/* ── Text Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid #c4b5fd !important;
    border-radius: 10px !important;
    background: #fff !important;
    color: #1e1b4b !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #a78bfa !important;
    border-radius: 12px !important;
    background: rgba(237, 233, 254, 0.5) !important;
    padding: 1rem;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #a78bfa, #f59e0b, transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ── Chat History Cards ── */
.chat-card {
    background: #ffffff;
    border: 1px solid #e0d7ff;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(124, 58, 237, 0.08);
    transition: box-shadow 0.2s ease;
}

.chat-card:hover {
    box-shadow: 0 6px 24px rgba(124, 58, 237, 0.18);
}

.chat-q {
    color: #5b21b6;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.4rem;
}

.chat-a {
    color: #1e1b4b;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 0.4rem;
}

.chat-ts {
    color: #9ca3af;
    font-size: 0.78rem;
    font-style: italic;
}

/* ── Answer Box ── */
.answer-box {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    border: 1.5px solid #a78bfa;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    color: #1e1b4b;
    font-size: 1rem;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.12);
}

/* ── Source Pills ── */
.source-pill {
    display: inline-block;
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border: 1px solid #f59e0b;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: #78350f;
    margin: 0.25rem 0.3rem 0.25rem 0;
}

/* ── Caption ── */
.stCaption {
    color: #9ca3af !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Domain Specific AI Agent")

# -------------------
# AUTH SECTION
# -------------------

st.sidebar.header("Authentication")

auth_mode = st.sidebar.radio(
    "Select Mode",
    ["Login", "Register"]
)

if auth_mode == "Register":
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type="password")

# -------------------
# REGISTER
# -------------------
if auth_mode == "Register":

    if st.sidebar.button("Register"):

        response = requests.post(
            f"{BACKEND_URL}/users",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        if response.status_code in [200, 201]:

            st.sidebar.success(
                "Registration successful! Please login."
            )
            st.balloons()
        else:

            st.sidebar.error(
                response.text
            )
# -------------------
# LOGIN SECTION
# -------------------
else:

    email = st.sidebar.text_input("Email", key="email_input")
    password = st.sidebar.text_input("Password", type="password", key="password_input")



    if st.sidebar.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/users/login",
            data={"username": email, "password": password}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token

            user_response = requests.get(
                f"{BACKEND_URL}/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if user_response.status_code == 200:
                user = user_response.json()
                st.session_state["role"] = user["role"]
                st.session_state["email"] = user["email"]

            st.sidebar.success("Login successful")

            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")

if "token" in st.session_state:
    st.sidebar.divider()
        
    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()

# -------------------
# AUTH CHECK
# -------------------
if "token" not in st.session_state:
    st.warning("Please login to continue.")
    st.stop()

# -------------------
# PROTECTED CONTENT
# -------------------
st.success(f"✅ Welcome back, **{st.session_state.get('email', 'User')}**!")

if st.session_state.get("role") == "admin":
    st.header("📤 Upload Documents")

    uploaded_file = st.file_uploader(
        "Choose a file (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=False
    )

    if uploaded_file:
        if st.button("Upload Document"):
            response = requests.post(
                f"{BACKEND_URL}/documents/upload",
                headers={"Authorization": f"Bearer {st.session_state['token']}"},
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            )

            if response.status_code == 200:
                st.success("✅ Document uploaded successfully!")
            else:
                st.error(response.text)
    
    st.header("📚 Uploaded Documents")

    response = requests.get(
        f"{BACKEND_URL}/documents",
        headers={
            "Authorization":
            f"Bearer {st.session_state['token']}"
        }
    )

    if response.status_code == 200:

        documents = response.json()

        if documents:

            for doc in documents:
                col1, col2 = st.columns([5, 1])

                with col1:
                    st.write(f"📄 {doc['filename']}")
                
                with col2:
                    if st.button(
                        "🗑",
                        key=f"delete_{doc['id']}"
                    ):
                        delete_response = requests.delete(
                            f"{BACKEND_URL}/documents/{doc['id']}",
                            headers={
                                "Authorization":
                                f"Bearer {st.session_state['token']}"
                        }
                        )

                        if delete_response.status_code == 200:
                            st.success("Document deleted successfully")
                            st.rerun()
                        else:
                            st.error(delete_response.text)
        else:
            st.info("No documents uploaded yet.")

st.header("💬 Ask a Question")

question = st.text_input("What would you like to know?", placeholder="e.g. What is our refund policy?")

if st.button("Ask ✨") and question:
    response = requests.post(
        f"{BACKEND_URL}/ask",
        headers={"Authorization": f"Bearer {st.session_state['token']}"},
        json={"query": question}
    )

    if response.status_code == 200:
        result = response.json()

        st.subheader("Answer")
        st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

        if result.get("sources"):
            st.subheader("Sources")
            pills_html = "".join(
                f'<span class="source-pill">📄 {src}</span>' for src in result["sources"]
            )
            st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.error(response.text)

st.divider()

st.header("🕓 Chat History")

history_response = requests.get(
    f"{BACKEND_URL}/chat/history",
    headers={"Authorization": f"Bearer {st.session_state['token']}"}
)

if history_response.status_code == 200:
    chats = history_response.json()

    for chat in chats:
        card_html = f"""
        <div class="chat-card">
            <div class="chat-q">🙋 {chat['question']}</div>
            <div class="chat-a">🤖 {chat['answer']}</div>
            <div class="chat-ts">Asked at: {chat['created_at']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)