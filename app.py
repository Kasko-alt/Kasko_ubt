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
# ҚАУІПСІЗДІК: ПАРОЛЬДІ ХЭШТЕУ ФУНКЦИЯСЫ
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

# =========================================================
# БАСТАПҚЫ СҰРАҚТАР
# =========================================================
default_questions = {
    "Информатика": [
        {
            "question": "Python тілінде экранға мәтін шығару үшін қай функция қолданылады?",
            "answers": ["input()", "print()", "output()", "write()"],
            "correct": 1,
        },
        {
            "question": "Python тілінде бүтін санның типі қалай аталады?",
            "answers": ["float", "str", "int", "bool"],
            "correct": 2,
        },
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
    hashed_input_password = hash_password(password)
    for user in users:
        stored_password = user.get("password")
        if user.get("username") == username and (stored_password == hashed_input_password or stored_password == password):
            return user
    return None

def username_exists(username):
    for user in users:
        if user.get("username") == username:
            return True
    return False

def role_name(role):
    if role == "president":
        return "Президент"
    elif role == "prime_minister":
        return "Премьер министр"
    elif role == "user":
        return "Оқушы"
    return "Белгісіз"

# =========================================================
# QUESTIONS
# =========================================================
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                for subject in all_subjects:
                    if subject not in data:
                        data[subject] = []
                return data
        except Exception:
            return default_questions.copy()

    return default_questions.copy()

def save_questions():
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

questions = load_questions()

# =========================================================
# НӘТИЖЕЛЕР ЖҮЙЕСІ
# =========================================================
def load_results_history():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def save_results_history(history):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

def add_result_to_history(subject, correct, total, percent):
    username = st.session_state.get("username", "Оқушы")
    history = load_results_history()

    history.append(
        {
            "username": username,
            "subject": subject,
            "correct": correct,
            "total": total,
            "percent": percent,
            "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
    )
    save_results_history(history)

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "full_name" not in st.session_state:
    st.session_state.full_name = ""
if "user_combination" not in st.session_state:
    st.session_state.user_combination = None
if "result_saved" not in st.session_state:
    st.session_state.result_saved = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "selected_combination" not in st.session_state:
    st.session_state.selected_combination = None
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "active_questions" not in st.session_state:
    st.session_state.active_questions = []
if "is_full_ubt" not in st.session_state:
    st.session_state.is_full_ubt = False

# =========================================================
# PREMIUM CSS STYLES (ЖАҢАРТЫЛҒАН ДИЗАЙН)
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
        font-family: 'Inter', sans-serif;
    }

    .kasym-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .kasym-subtitle {
        font-size: 16px;
        text-align: center;
        color: #9CA3AF;
        margin-bottom: 30px;
        font-weight: 500;
    }

    .card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
        border-color: #6366F1;
    }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #1E293B !important;
        border-radius: 10px !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# LOGOUT
# =========================================================
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""
    st.session_state.full_name = ""
    st.session_state.user_combination = None
    st.session_state.result_saved = False
    st.session_state.page = "login"
    st.session_state.selected_combination = None
    st.session_state.selected_subject = None
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.active_questions = []
    st.session_state.is_full_ubt = False
    st.rerun()

def top_logout_button():
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🚪 Шығу", key="top_logout"):
            logout()

# =========================================================
# LOGIN
# =========================================================
def login_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🔐 Жүйеге кіру</h3>", unsafe_allow_html=True)

        username = st.text_input("Логин", key="login_username")
        password = st.text_input("Құпия сөз", type="password", key="login_password")

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        if st.button("Кіру →", use_container_width=True, type="primary"):
            username = username.strip()

            if username == "" or password == "":
                st.error("Логин мен құпия сөзді толық енгізіңіз.")
            else:
                user = find_user(username, password)

                if user is None:
                    st.error("❌ Логин немесе құпия сөз қате.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.full_name = user.get("name", user["username"])
                    st.session_state.role = user.get("role", "user")
                    st.session_state.user_combination = user.get("combination", combinations[0])
                    st.session_state.result_saved = False

                    if user.get("role") == "president":
                        st.session_state.page = "admin"
                    elif user.get("role") == "prime_minister":
                        st.session_state.page = "prime_minister"
                    else:
                        st.session_state.page = "home"

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PRESIDENT PANEL
# =========================================================
def admin_page():
    top_logout_button()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">👑 PRESIDENT PANEL</div>', unsafe_allow_html=True)

    st.success(f"Қош келдіңіз, {st.session_state.full_name}!")
    st.markdown("## 👤 Аккаунт басқару")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Жаңа оқушы/аккаунт жасау", use_container_width=True, type="primary"):
            st.session_state.page = "create_user"
            st.rerun()

    with col2:
        if st.button("👥 Аккаунттар тізімі", use_container_width=True):
            st.session_state.page = "users_list"
            st.rerun()

# =========================================================
# CREATE USER
# =========================================================
def create_user_page():
    top_logout_button()
    st.title("➕ Жаңа аккаунт жасау")

    if st.button("← Президент панеліне қайту", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

    st.markdown("---")

    name = st.text_input("Аты-жөні")
    new_username = st.text_input("Жаңа логин")
    new_password = st.text_input("Жаңа құпия сөз", type="password")
    role = st.selectbox("Рөлді таңдаңыз", ["Оқушы", "Премьер министр"])
    selected_comb = st.selectbox("Бағыты (Оқушылар үшін):", combinations)

    role_value = "prime_minister" if role == "Премьер министр" else "user"

    if st.button("💾 Оқушыны сақтау", use_container_width=True, type="primary"):
        name = name.strip()
        new_username = new_username.strip()
        new_password = new_password.strip()

        if name == "" or new_username == "" or new_password == "":
            st.error("Барлық өрісті толтырыңыз.")
        elif username_exists(new_username):
            st.error("❌ Бұл логин бұрыннан бар.")
        else:
            users.append({
                "username": new_username,
                "password": hash_password(new_password),
                "name": name,
                "role": role_value,
                "combination": selected_comb if role_value == "user" else None,
            })
            save_users(users)
            st.success(f"✅ {name} үшін аккаунт жасалды.")

# =========================================================
# USERS LIST
# =========================================================
def users_list_page():
    top_logout_button()
    st.title("👥 Аккаунттар тізімі")

    if st.button("← Президент панеліне қайту", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

    st.markdown("---")

    for index, user in enumerate(users):
        r_name = role_name(user.get("role"))
        comb_info = f"<p>💻 Бағыты: <b>{user.get('combination', 'Белгіленбеген')}</b></p>" if user.get("role") == "user" else ""

        st.markdown(
            f"""
            <div class="card">
                <h3>👤 {user.get("name", "Аты жоқ")}</h3>
                <p>🔑 Логин: <b>{user.get("username", "")}</b></p>
                <p>🎖️ Рөл: <b>{r_name}</b></p>
                {comb_info}
            </div>
            """,
            unsafe_allow_html=True
        )

        if user.get("role") != "president":
            if st.button(f"🗑️ Өшіру: {user.get('username')}", key=f"delete_user_{index}", use_container_width=True):
                users.pop(index)
                save_users(users)
                st.success("Аккаунт өшірілді.")
                st.rerun()

# =========================================================
# PRIME MINISTER PANEL
# =========================================================
def prime_minister_page():
    top_logout_button()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">👨‍💼 ПРЕМЬЕР МИНИСТР ПАНЕКІ</div>', unsafe_allow_html=True)

    st.success(f"Қош келдіңіз, {st.session_state.full_name}!")

    st.markdown("## 📚 Сұрақтар базасын басқару")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Жеке сұрақ қосу", use_container_width=True, type="primary"):
            st.session_state.page = "add_question"
            st.rerun()

    with col2:
        if st.button("📚 Сұрақтар базасы", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()

# =========================================================
# ADD QUESTION (ЖАҢАРТЫЛҒАН ДИЗАЙН - КАРТОЧКА ФОРМАТЫ)
# =========================================================
def add_question_page():
    top_logout_button()
    
    if st.session_state.role != "prime_minister":
        st.error("Бұл бөлімге тек Премьер министр кіре алады.")
        return

    st.markdown('<div class="kasym-title" style="font-size: 32px;">➕ Жаңа сұрақ қосу</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Базаға жаңа сұрақтар мен нұсқаларды енгізу панелі</div>', unsafe_allow_html=True)

    if st.button("← Панельге қайту", use_container_width=False):
        st.session_state.page = "prime_minister"
        st.rerun()

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Карточка контейнерінің ішіне форманы саламыз
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    selected_subject = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    question_text = st.text_area("✍️ Сұрақты толық жазыңыз:", placeholder="Мысалы: Фотосинтез процесі қай органоидта жүреді?")

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Желке нұсқаларын толтырыңыз:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        ans1 = st.text_input("А нұсқасы:", placeholder="Ядро")
        ans3 = st.text_input("В нұсқасы:", placeholder="Рибосома")
    with col_b:
        ans2 = st.text_input("Б нұсқасы:", placeholder="Хлоропласт")
        ans4 = st.text_input("Г нұсқасы:", placeholder="Митохондрия")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    correct_option = st.selectbox("✅ Дұрыс жауап қайсысы?", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"])
    correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(correct_option)

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
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
            st.success("✨ Сұрақ сәтті сақталды және базаға қосылды!")
        else:
            st.error("⚠️ Барлық өрістерді толық толтырыңыз!")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# QUESTION LIST
# =========================================================
def question_list_page():
    top_logout_button()
    st.title("📚 Сұрақтар базасы")

    if st.button("← Панельге қайту", use_container_width=True):
        st.session_state.page = "prime_minister"
        st.rerun()

    st.markdown("---")

    selected_subject = st.selectbox("Пәнді таңдаңыз:", all_subjects)
    subject_q = questions.get(selected_subject, [])

    st.write(f"Жалпы сұрақ саны: **{len(subject_q)}**")

    for idx, q in enumerate(subject_q):
        with st.expander(f"Сұрақ {idx + 1}: {q['question'][:50]}..."):
            st.write(f"**Толық сұрақ:** {q['question']}")

            for a_idx, ans in enumerate(q["answers"]):
                is_corr = " (✅ Дұрыс)" if a_idx == q["correct"] else ""
                st.write(f"- {ans}{is_corr}")

            if st.button(f"🗑️ Өшіру №{idx + 1}", key=f"del_{selected_subject}_{idx}"):
                questions[selected_subject].pop(idx)
                save_questions()
                st.rerun()

# =========================================================
# RESULTS HISTORY & PROGRESS (Қалған беттер)
# =========================================================
def results_history_page():
    top_logout_button()
    st.title("📊 Менің нәтижелерім")
    if st.button("← Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

def progress_page():
    top_logout_button()
    st.title("📈 Менің прогрессім")
    if st.button("← Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

def home_page():
    top_logout_button()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)
    
    if st.button("➕ Сұрақ қосу панеліне өту", type="primary", use_container_width=True):
        st.session_state.page = "add_question"
        st.rerun()

def test_page():
    pass

def result_page():
    pass

# =========================================================
# MAIN ROUTER
# =========================================================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        page = st.session_state.page
        if page == "admin":
            admin_page()
        elif page == "create_user":
            create_user_page()
        elif page == "users_list":
            users_list_page()
        elif page == "prime_minister":
            prime_minister_page()
        elif page == "add_question":
            add_question_page()
        elif page == "question_list":
            question_list_page()
        elif page == "home":
            home_page()

if __name__ == "__main__":
    main()
