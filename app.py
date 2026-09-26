import json
import os
import random
import datetime
import hashlib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# KASYM EDU CONFIG
# =========================================================
st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide"
)

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"

# =========================================================
# ПАРОЛЬДІ ХЭШТЕУ
# =========================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# ПӘНДЕР МЕН КОМБИНАЦИЯЛАР
# =========================================================
combinations = [
    "Биология + Химия",
    "Физика + Математика",
    "Информатика + Математика",
    "Дүниежүзі тарихы + Ағылшын тілі",
    "Биология + География",
    "География + Математика",
    "Дүниежүзі тарихы + Құқық",
]

common_subjects = [
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық",
]

all_subjects = [
    "Биология",
    "Химия",
    "Физика",
    "Математика",
    "Информатика",
    "Дүниежүзі тарихы",
    "Ағылшын тілі",
    "География",
    "Құқық",
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық",
]

default_questions = {
    "Информатика": [
        {
            "question": "Python тілінде экранға мәтін шығару үшін қай функция қолданылады?",
            "answers": ["input()", "print()", "output()", "write()"],
            "correct": 1,
        }
    ]
}

# =========================================================
# АККАУНТ ЖҮЙЕСІ
# =========================================================
def default_users():
    return [
        {
            "username": "kas01",
            "password": hash_password("kasko100228550357"),
            "name": "KASYM",
            "role": "president",
            "combination": None,
        }
    ]

def save_users(users_list):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users_list, file, ensure_ascii=False, indent=4)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    users_list = default_users()
    save_users(users_list)
    return users_list

users = load_users()

def find_user(username, password):
    hashed_input = hash_password(password)
    for user in users:
        stored = user.get("password")
        if user.get("username") == username and (stored == hashed_input or stored == password):
            return user
    return None

def username_exists(username):
    return any(u.get("username") == username for u in users)

def role_name(role):
    if role == "president": return "Президент"
    elif role == "prime_minister": return "Премьер министр"
    elif role == "user": return "Оқушы"
    return "Белгісіз"

# =========================================================
# СҰРАҚТАР МЕН НӘТИЖЕЛЕР
# =========================================================
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                for sub in all_subjects:
                    if sub not in data: data[sub] = []
                return data
        except Exception:
            return default_questions.copy()
    return default_questions.copy()

def save_questions():
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

questions = load_questions()

def load_results_history():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list): return data
        except Exception:
            pass
    return []

def save_results_history(history):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

def add_result_to_history(subject, correct, total, percent):
    username = st.session_state.get("username", "Оқушы")
    history = load_results_history()
    history.append({
        "username": username,
        "subject": subject,
        "correct": correct,
        "total": total,
        "percent": percent,
        "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    })
    save_results_history(history)

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = None
if "username" not in st.session_state: st.session_state.username = ""
if "full_name" not in st.session_state: st.session_state.full_name = ""
if "user_combination" not in st.session_state: st.session_state.user_combination = None
if "result_saved" not in st.session_state: st.session_state.result_saved = False
if "page" not in st.session_state: st.session_state.page = "login"
if "selected_subject" not in st.session_state: st.session_state.selected_subject = None
if "current_question" not in st.session_state: st.session_state.current_question = 0
if "user_answers" not in st.session_state: st.session_state.user_answers = {}
if "active_questions" not in st.session_state: st.session_state.active_questions = []
if "is_full_ubt" not in st.session_state: st.session_state.is_full_ubt = False
if "theme" not in st.session_state: st.session_state.theme = "Қараңғы (Dark)"

# =========================================================
# ДИНАМИКАЛЫҚ CSS (Қараңғы & Көзге жайлы Ақшыл режим)
# =========================================================
if st.session_state.theme == "Ақшыл (Light)":
    # Көзді ауыртпайтын жұмсақ палитра (Soft Light Theme)
    bg_color = "#F8FAFC"
    card_bg = "#FFFFFF"
    text_color = "#1E293B"
    sub_text = "#64748B"
    border_color = "rgba(0, 0, 0, 0.08)"
    input_bg = "#F1F5F9"
    sidebar_bg = "#F1F5F9"
else:
    # Премиум қараңғы режим (Dark Theme)
    bg_color = "#0B0F19"
    card_bg = "linear-gradient(145deg, #1E293B 0%, #0F172A 100%)"
    text_color = "#F3F4F6"
    sub_text = "#9CA3AF"
    border_color = "rgba(255, 255, 255, 0.08)"
    input_bg = "#1E293B"
    sidebar_bg = "#0F172A"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }

    .kasym-title {{
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }}
    
    .kasym-subtitle {{
        font-size: 16px;
        text-align: center;
        color: {sub_text};
        margin-bottom: 30px;
        font-weight: 500;
    }}

    .card {{
        background: {card_bg};
        padding: 24px;
        border-radius: 16px;
        border: 1px solid {border_color};
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }}

    .stButton>button {{
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid {border_color};
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.2);
        border-color: #6366F1;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {{
        background-color: {input_bg} !important;
        border-radius: 10px !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# ЖОҒАРҒЫ ПАНЕЛЬ ЖӘНЕ ТЕМА АУЫСТЫРҒЫШ
# =========================================================
def top_bar():
    col1, col2 = st.columns([7, 3])
    with col2:
        # Режимді ауыстыру батырмасы
        current_theme_icon = "🌙 Қараңғы" if st.session_state.theme == "Ақшыл (Light)" else "☀️ Ақшыл"
        if st.button(f"🎨 Режим: {current_theme_icon}", use_container_width=True):
            if st.session_state.theme == "Ақшыл (Light)":
                st.session_state.theme = "Қараңғы (Dark)"
            else:
                st.session_state.theme = "Ақшыл (Light)"
            st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "login"
    st.rerun()

# =========================================================
# LOGIN
# =========================================================
def login_page():
    top_bar()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🔐 Жүйеге кіру</h3>", unsafe_allow_html=True)
        username = st.text_input("Логин", key="login_username")
        password = st.text_input("Құпия сөз", type="password", key="login_password")

        if st.button("Кіру →", use_container_width=True, type="primary"):
            user = find_user(username.strip(), password.strip())
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.full_name = user.get("name", "")
                st.session_state.role = user.get("role", "user")
                st.session_state.page = "admin" if user["role"] == "president" else ("prime_minister" if user["role"] == "prime_minister" else "home")
                st.rerun()
            else:
                st.error("❌ Логин немесе құпия сөз қате.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# БАСТЫ БЕТ (HOME) ЖӘНЕ БАСҚА БӨЛІМДЕР
# =========================================================
def home_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Қош келдіңіз, оқушы!</div>', unsafe_allow_html=True)

def admin_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    st.title("👑 Президент панелі")

def prime_minister_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    st.title("👨‍💼 Премьер министр панелі")

# =========================================================
# РОУТЕР
# =========================================================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        p = st.session_state.page
        if p == "admin": admin_page()
        elif p == "prime_minister": prime_minister_page()
        else: home_page()

if __name__ == "__main__":
    main()
