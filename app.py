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
# НӘТИЖЕЛЕР
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
# CSS
# =========================================================
st.markdown(
    """
    <style>
    .kasym-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #4F46E5;
    }
    .kasym-subtitle {
        font-size: 18px;
        text-align: center;
        color: #6B7280;
        margin-bottom: 20px;
    }
    .card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
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
        if st.button("🚪 Жалпы шығу", key="top_logout"):
            logout()

# =========================================================
# LOGIN
# =========================================================
def login_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🔐 Жүйеге кіру")

    username = st.text_input("Логин", key="login_username")
    password = st.text_input("Құпия сөз", type="password", key="login_password")

    if st.button("Кіру →", use_container_width=True):
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
    st.info("Президенттің негізгі міндеті — жүйедегі аккаунттарды басқару.")

    st.markdown("## 👤 Аккаунт басқару")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Жаңа оқушы/аккаунт жасау", use_container_width=True):
            st.session_state.page = "create_user"
            st.rerun()

    with col2:
        if st.button("👥 Аккаунттар тізімі", use_container_width=True):
            st.session_state.page = "users_list"
            st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ Рөлдер")
    st.write("👑 **Президент** — аккаунттарды басқарады.")
    st.write("👨‍💼 **Премьер министр** — сұрақтар базасын басқарады.")
    st.write("👤 **Оқушы** — тест тапсырады және нәтижесін көреді.")

# =========================================================
# CREATE USER (ЖАҢАРТЫЛДЫ: БАҒЫТ ТАҢДАУ ҚОСЫЛДЫ)
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

    # 🔥 БАҒЫТ (КОМБИНАЦИЯ) ТАҢДАУ
    selected_comb = st.selectbox("Бағыты (Оқушылар үшін):", combinations)

    role_value = "prime_minister" if role == "Премьер министр" else "user"

    if st.button("💾 Оқушыны сақтау", use_container_width=True):
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
            st.info(f"Логин: {new_username}")
            st.info(f"Бағыты: {selected_comb}")

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
    st.markdown('<div class="kasym-subtitle">👨‍💼 ПРЕМЬЕР МИНИСТР</div>', unsafe_allow_html=True)

    st.success(f"Қош келдіңіз, {st.session_state.full_name}!")

    st.markdown("## 📚 Сұрақтар базасын басқару")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Жеке сұрақ қосу", use_container_width=True):
            st.session_state.page = "add_question"
            st.rerun()

    with col2:
        if st.button("📚 Сұрақтар базасы", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()

    st.markdown("---")

    if st.button("👤 Оқушы режиміне өту", use_container_width=True):
        st.session_state.role = "user"
        st.session_state.user_combination = combinations[0]
        st.session_state.page = "home"
        st.rerun()

# =========================================================
# ADD QUESTION
# =========================================================
def add_question_page():
    top_logout_button()
    st.title("➕ Жаңа сұрақ қосу")

    if st.session_state.role != "prime_minister":
        st.error("Бұл бөлімге тек Премьер министр кіре алады.")
        return

    if st.button("← Панельге қайту", use_container_width=True):
        st.session_state.page = "prime_minister"
        st.rerun()

    st.markdown("---")

    selected_subject = st.selectbox("Пәнді таңдаңыз:", all_subjects)
    question_text = st.text_area("Сұрақты жазыңыз:")

    ans1 = st.text_input("А нұсқасы:")
    ans2 = st.text_input("Б нұсқасы:")
    ans3 = st.text_input("В нұсқасы:")
    ans4 = st.text_input("Г нұсқасы:")

    correct_option = st.selectbox("Дұрыс жауап қайсысы?", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"])
    correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(correct_option)

    if st.button("💾 Сұрақты сақтау", use_container_width=True):
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
            st.success("✅ Сұрақ сәтті сақталды!")
        else:
            st.error("Барлық өрістерді толтырыңыз!")

# =========================================================
# QUESTION LIST
# =========================================================
def question_list_page():
    top_logout_button()
    st.title("📚 Сұрақтар базасы")

    if st.session_state.role == "prime_minister":
        if st.button("← Панельге қайту", use_container_width=True):
            st.session_state.page = "prime_minister"
            st.rerun()
    else:
        if st.button("← Артқа", use_container_width=True):
            st.session_state.page = "home"
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

            if st.session_state.role == "prime_minister":
                if st.button(f"🗑️ Өшіру №{idx + 1}", key=f"del_{selected_subject}_{idx}"):
                    questions[selected_subject].pop(idx)
                    save_questions()
                    st.rerun()

# =========================================================
# RESULTS HISTORY (ТЕК ӨЗ НӘТИЖЕЛЕРІ КӨРІНЕДІ)
# =========================================================
def results_history_page():
    top_logout_button()
    st.title("📊 Менің нәтижелерім")

    if st.button("← Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    username = st.session_state.get("username", "Оқушы")
    history = load_results_history()

    # ТЕК ӨЗ ЛОГИНІМЕН СӘЙКЕС КЕЛЕТІН НӘТИЖЕЛЕР ДЕРЕГІ
    my_results = [item for item in history if item.get("username") == username]

    if not my_results:
        st.info("Әзірге тапсырылған тест нәтижесі жоқ.")
        return

    st.markdown("---")

    for number, item in enumerate(reversed(my_results), 1):
        st.markdown(
            f"""
            <div class="card">
                <h3>📝 {number}-тест — {item.get("subject", "Пән")}</h3>
                <p>Нәтиже: <b>{item.get("percent", 0)}%</b></p>
                <p>Балл: <b>{item.get("correct", 0)} / {item.get("total", 0)}</b></p>
                <p>📅 {item.get("date", "")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# PROGRESS
# =========================================================
def progress_page():
    top_logout_button()
    st.title("📈 Менің прогрессім")

    if st.button("← Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    username = st.session_state.get("username", "Оқушы")
    history = load_results_history()

    my_results = [item for item in history if item.get("username") == username]

    if not my_results:
        st.info("Прогресс көрсету үшін алдымен кемінде бір тест тапсырыңыз.")
        return

    st.markdown("---")

    subject_stats = {}
    for item in my_results:
        subject = item.get("subject", "Белгісіз пән")
        percent = int(item.get("percent", 0))

        if subject not in subject_stats:
            subject_stats[subject] = []
        subject_stats[subject].append(percent)

    for subject, scores in subject_stats.items():
        last_score = scores[-1]
        best_score = max(scores)
        test_count = len(scores)

        st.markdown(f"## 📚 {subject}")
        st.write(f"**Соңғы нәтиже:** {last_score}%")
        st.write(f"**Үздік нәтиже:** {best_score}%")
        st.write(f"**Тест саны:** {test_count}")
        st.progress(last_score / 100)
        st.markdown("---")

# =========================================================
# USER HOME (ЖАҢАРТЫЛДЫ: ТЕК БЕКІТІЛГЕН БАҒЫТ КӨРІНЕДІ)
# =========================================================
def home_page():
    top_logout_button()
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    st.markdown(f"### 👋 Сәлем, {st.session_state.full_name}!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Менің нәтижелерім", use_container_width=True):
            st.session_state.page = "results_history"
            st.rerun()

    with col2:
        if st.button("📈 Менің прогрессім", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()

    st.markdown("---")

    # 🎯 ОҚУШЫНЫҢ ЖЕКЕ БАҒЫТЫ
    user_comb = st.session_state.get("user_combination", combinations[0])
    st.session_state.selected_combination = user_comb

    st.markdown(f"## 💻 Таңдалған бағытыңыз: **{user_comb}**")

    # 1. ТОЛЫҚ ҰБТ
    if st.button(f"🚀 {user_comb} бойынша толық ҰБТ тапсыру (5 пән)", type="primary", use_container_width=True):
        st.session_state.selected_subject = f"ҰБТ: {user_comb}"
        st.session_state.is_full_ubt = True
        st.session_state.current_question = 0
        st.session_state.user_answers = {}
        st.session_state.active_questions = []
        st.session_state.result_saved = False
        st.session_state.page = "test"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📘 Жеке пәндер бойынша дайындық")

    main_subjects = user_comb.split(" + ")
    cols = st.columns(2)

    for i, subject in enumerate(main_subjects):
        with cols[i]:
            count = len(questions.get(subject, []))
            if st.button(f"📘 {subject}\n\n{count} сұрақ", use_container_width=True, key=f"main_{subject}"):
                st.session_state.selected_subject = subject
                st.session_state.is_full_ubt = False
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.active_questions = []
                st.session_state.result_saved = False
                st.session_state.page = "test"
                st.rerun()

    st.markdown("#### 📙 Міндетті пәндер")
    cols_com = st.columns(3)
    for i, subject in enumerate(common_subjects):
        with cols_com[i]:
            count = len(questions.get(subject, []))
            if st.button(f"📙 {subject}\n\n{count} сұрақ", use_container_width=True, key=f"com_{subject}"):
                st.session_state.selected_subject = subject
                st.session_state.is_full_ubt = False
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.active_questions = []
                st.session_state.result_saved = False
                st.session_state.page = "test"
                st.rerun()

# =========================================================
# TEST PAGE
# =========================================================
def test_page():
    top_logout_button()
    
    # --- САЙДБАРДАҒЫ КАЛЬКУЛЯТОР ---
    with st.sidebar:
        st.markdown("### 🧮 Калькулятор")
        calc_html = """
        <div style="background: #1F2937; padding: 12px; border-radius: 10px; border: 1px solid #4F46E5;">
            <input type="text" id="calc-display" readonly style="
                width: 100%; height: 38px; background: #111827; color: #10B981; 
                font-size: 18px; text-align: right; padding: 4px 8px; border: 1px solid #4B5563; 
                border-radius: 6px; margin-bottom: 8px; box-sizing: border-box; font-weight: bold;
            " value="0">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
                <button onclick="calcClear()" style="background:#EF4444; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">C</button>
                <button onclick="calcInput('(')" style="background:#4B5563; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">(</button>
                <button onclick="calcInput(')')" style="background:#4B5563; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">)</button>
                <button onclick="calcInput('/')" style="background:#4F46E5; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">÷</button>

                <button onclick="calcInput('7')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">7</button>
                <button onclick="calcInput('8')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">8</button>
                <button onclick="calcInput('9')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">9</button>
                <button onclick="calcInput('*')" style="background:#4F46E5; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">×</button>

                <button onclick="calcInput('4')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">4</button>
                <button onclick="calcInput('5')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">5</button>
                <button onclick="calcInput('6')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">6</button>
                <button onclick="calcInput('-')" style="background:#4F46E5; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">-</button>

                <button onclick="calcInput('1')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">1</button>
                <button onclick="calcInput('2')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">2</button>
                <button onclick="calcInput('3')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">3</button>
                <button onclick="calcInput('+')" style="background:#4F46E5; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">+</button>

                <button onclick="calcInput('0')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">0</button>
                <button onclick="calcInput('.')" style="background:#374151; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">.</button>
                <button onclick="calcBackspace()" style="background:#F59E0B; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer;">⌫</button>
                <button onclick="calcCalculate()" style="background:#10B981; color:white; padding:8px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">=</button>
            </div>
        </div>

        <script>
        let display = document.getElementById('calc-display');
        function calcInput(val) {
            if (display.value === '0' || display.value === 'Қате') display.value = val;
            else display.value += val;
        }
        function calcClear() { display.value = '0'; }
        function calcBackspace() {
            display.value = display.value.slice(0, -1);
            if (display.value === '') display.value = '0';
        }
        function calcCalculate() {
            try { display.value = eval(display.value); } 
            catch (e) { display.value = 'Қате'; }
        }
        </script>
        """
        components.html(calc_html, height=320)

    st.title(f"📝 {st.session_state.selected_subject}")

    if st.button("← Артқа қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("---")

    # Сұрақтарды жүктеу
    if st.session_state.current_question == 0 and not st.session_state.active_questions:
        prepared = []
        
        if st.session_state.is_full_ubt:
            main_subs = st.session_state.selected_combination.split(" + ")
            target_subjects = common_subjects + main_subs
            
            for sub in target_subjects:
                raw_qs = questions.get(sub, [])
                for item in raw_qs:
                    answers_copy = item["answers"].copy()
                    correct_text = answers_copy[item["correct"]]
                    random.shuffle(answers_copy)
                    prepared.append({
                        "subject": sub,
                        "question": item["question"],
                        "answers": answers_copy,
                        "correct": answers_copy.index(correct_text),
                    })
        else:
            sub = st.session_state.selected_subject
            raw_qs = questions.get(sub, [])
            for item in raw_qs:
                answers_copy = item["answers"].copy()
                correct_text = answers_copy[item["correct"]]
                random.shuffle(answers_copy)
                prepared.append({
                    "subject": sub,
                    "question": item["question"],
                    "answers": answers_copy,
                    "correct": answers_copy.index(correct_text),
                })

        st.session_state.active_questions = prepared

    subject_questions = st.session_state.active_questions
    total = len(subject_questions)

    if total == 0:
        st.warning("Бұл режим бойынша сұрақтар әлі қосылмаған.")
        return

    current = st.session_state.current_question

    nav_cols = st.columns(min(total, 20))
    for i in range(min(total, 20)):
        is_current = (i == current)
        btn_type = "primary" if is_current else "secondary"
        with nav_cols[i]:
            if st.button(str(i + 1), key=f"nav_btn_{i}", use_container_width=True, type=btn_type):
                st.session_state.current_question = i
                st.rerun()

    st.markdown("---")

    question = subject_questions[current]

    st.caption(f"Пән: {question.get('subject', '')}")
    st.markdown(f"### Сұрақ {current + 1} / {total}")
    st.markdown(f'<div class="card"><h3>{question["question"]}</h3></div>', unsafe_allow_html=True)

    saved_index = st.session_state.user_answers.get(current, None)

    answer = st.radio(
        "Жауапты таңдаңыз:",
        question["answers"],
        index=saved_index,
        key=f"question_{current}",
    )

    if answer is not None:
        st.session_state.user_answers[current] = question["answers"].index(answer)

    col_back, col_next = st.columns(2)

    with col_back:
        if current > 0 and st.button("← Артқа", use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

    with col_next:
        button_label = "Келесі →" if current + 1 < total else "🎯 Тестті аяқтау"

        if st.button(button_label, use_container_width=True):
            if current + 1 < total:
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.session_state.page = "result"
                st.rerun()

# =========================================================
# RESULT PAGE
# =========================================================
def result_page():
    top_logout_button()
    st.title("🎯 Тест нәтижесі")

    subject_questions = st.session_state.active_questions
    total = len(subject_questions)
    correct_count = 0

    for idx, q in enumerate(subject_questions):
        user_ans = st.session_state.user_answers.get(idx)
        if user_ans is not None and user_ans == q["correct"]:
            correct_count += 1

    percent = int((correct_count / total) * 100) if total > 0 else 0

    if not st.session_state.result_saved:
        add_result_to_history(st.session_state.selected_subject, correct_count, total, percent)
        st.session_state.result_saved = True

    st.markdown(
        f"""
        <div class="card" style="text-align: center;">
            <h2>{st.session_state.selected_subject}</h2>
            <h1 style="color: #10B981; font-size: 48px;">{percent}%</h1>
            <p style="font-size: 20px;">Дұрыс балл: <b>{correct_count} / {total}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🏠 Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

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
        elif page == "test":
            test_page()
        elif page == "result":
            result_page()
        elif page == "results_history":
            results_history_page()
        elif page == "progress":
            progress_page()

if __name__ == "__main__":
    main()
