import json
import os
import random
import datetime
import hashlib
import pandas as pd
import streamlit as st

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

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = None
if "username" not in st.session_state: st.session_state.username = ""
if "full_name" not in st.session_state: st.session_state.full_name = ""
if "page" not in st.session_state: st.session_state.page = "login"
if "theme" not in st.session_state: st.session_state.theme = "Қараңғы (Dark)"

# =========================================================
# ДИНАМИКАЛЫҚ CSS (Қатесіз жазылған стильдер)
# =========================================================
if st.session_state.theme == "Ақшыл (Light)":
    bg_color = "#F8FAFC"
    card_bg = "#FFFFFF"
    text_color = "#1E293B"
    sub_text = "#64748B"
    border_color = "rgba(0, 0, 0, 0.08)"
    input_bg = "#F1F5F9"
    sidebar_bg = "#F1F5F9"
else:
    bg_color = "#0B0F19"
    card_bg = "#1E293B"
    text_color = "#F3F4F6"
    sub_text = "#9CA3AF"
    border_color = "rgba(255, 255, 255, 0.08)"
    input_bg = "#1E293B"
    sidebar_bg = "#0F172A"

css_code = f"""
<style>
.stApp {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Inter', sans-serif;
}}
.kasym-title {{
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}}
.kasym-subtitle {{
    font-size: 16px;
    text-align: center;
    color: {sub_text};
    margin-bottom: 30px;
    font-weight: 500;
}}
.card {{
    background-color: {card_bg};
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
}}
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {{
    background-color: {input_bg} !important;
    border-radius: 10px !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
}}
[data-testid="stSidebar"] {{
    background-color: {sidebar_bg};
}}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# =========================================================
# ЖОҒАРҒЫ ПАНЕЛЬ ЖӘНЕ ТЕМА АУЫСТЫРҒЫШ
# =========================================================
def top_bar():
    col1, col2 = st.columns([7, 3])
    with col2:
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
# ПРЕМЬЕР-МИНИСТР ПАНЕЛІ (СҰРАҚ ҚОСУ)
# =========================================================
def prime_minister_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    
    st.markdown('<div class="kasym-title" style="font-size: 32px;">➕ Жаңа сұрақ қосу</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Базаға жаңа сұрақтар мен нұсқаларды енгізу панелі</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_subject = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects)
    question_text = st.text_area("✍️ Сұрақты толық жазыңыз:", placeholder="Мысалы: Фотосинтез процесі қай органоидта жүреді?")

    col_a, col_b = st.columns(2)
    with col_a:
        ans1 = st.text_input("А нұсқасы:")
        ans3 = st.text_input("В нұсқасы:")
    with col_b:
        ans2 = st.text_input("Б нұсқасы:")
        ans4 = st.text_input("Г нұсқасы:")

    correct_option = st.selectbox("✅ Дұрыс жауап қайсысы?", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"])
    correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(correct_option)

    if st.button("💾 Сұрақты базаға сақтау", use_container_width=True, type="primary"):
        if question_text and ans1 and ans2 and ans3 and ans4:
            new_q = {
                "question": question_text,
                "answers": [ans1, ans2, ans3, ans4],
                "correct": correct_index,
            }
            if selected_subject not in questions:
                questions[selected_subject] = []
            questions[selected_subject].append(new_q)
            save_questions()
            st.success("✨ Сұрақ сәтті сақталды!")
        else:
            st.error("⚠️ Барлық өрістерді толық толтырыңыз!")
    st.markdown('</div>', unsafe_allow_html=True)

def admin_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    st.title("👑 Президент панелі")

def home_page():
    top_bar()
    if st.button("🚪 Шығу"): logout()
    st.title("🏠 Басты бет (Оқушы)")

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
