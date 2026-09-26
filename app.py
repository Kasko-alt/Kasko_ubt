import json
import os
import random
import datetime
import hashlib
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
# ҚАУІПСІЗДІК: ПАРОЛЬДІ ХЭШТЕУ ФУНКЦИЯСЫ
# =========================================================
def hash_password(password: str) -> str:
    """Парольді SHA-256 алгоритмі арқылы шифрлайды"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# ПӘНДЕР
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
# АККАУНТ ЖҮЙЕСІ (ШИФРЛАНҒАН)
# =========================================================
def default_users():
    return [
        {
            "username": "kas01",
            "password": hash_password("kasko100228550357"),  # Пароль хэш түрінде сақталады
            "name": "KASYM",
            "role": "president",
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
        # Ескі жүйеден қалған ашық парольдер болса, оларды да тексеруге мүмкіндік береді
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
        json.dump(
            questions,
            file,
            ensure_ascii=False,
            indent=4
        )

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
        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=4
        )

def add_result_to_history(subject, correct, total, percent):
    username = st.session_state.get(
        "username",
        "Оқушы"
    )
    history = load_results_history()

    history.append(
        {
            "username": username,
            "subject": subject,
            "correct": correct,
            "total": total,
            "percent": percent,
            "date": datetime.datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
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
    .error-box {
        background-color: #374151;
        padding: 15px;
        border-left: 5px solid #EF4444;
        border-radius: 8px;
        margin-bottom: 10px;
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
    st.session_state.result_saved = False
    st.session_state.page = "login"
    st.session_state.selected_combination = None
    st.session_state.selected_subject = None
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.active_questions = []
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
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">👑 PRESIDENT PANEL</div>', unsafe_allow_html=True)

    st.success(f"Қош келдіңіз, {st.session_state.full_name}!")
    st.info("Президенттің негізгі міндеті — жүйедегі аккаунттарды басқару.")

    st.markdown("## 👤 Аккаунт басқару")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Жаңа аккаунт жасау", use_container_width=True):
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
# CREATE USER
# =========================================================
def create_user_page():
    st.title("➕ Жаңа аккаунт жасау")

    if st.button("← Президент панеліне қайту", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

    st.markdown("---")

    name = st.text_input("Аты-жөні")
    new_username = st.text_input("Жаңа логин")
    new_password = st.text_input("Жаңа құпия сөз", type="password")
    role = st.selectbox("Рөлді таңдаңыз", ["Оқушы", "Премьер министр"])

    role_value = "prime_minister" if role == "Премьер министр" else "user"

    if st.button("💾 Аккаунтты сақтау", use_container_width=True):
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
                "password": hash_password(new_password),  # Жаңа қолданушының паролі де хэштеледі
                "name": name,
                "role": role_value,
            })
            save_users(users)
            st.success(f"✅ {name} үшін аккаунт жасалды.")
            st.info(f"Логин: {new_username}")
            st.info(f"Рөл: {role}")

# =========================================================
# USERS LIST
# =========================================================
def users_list_page():
    st.title("👥 Аккаунттар тізімі")

    if st.button("← Президент панеліне қайту", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

    st.markdown("---")

    for index, user in enumerate(users):
        r_name = role_name(user.get("role"))

        st.markdown(
            f"""
            <div class="card">
                <h3>👤 {user.get("name", "Аты жоқ")}</h3>
                <p>🔑 Логин: <b>{user.get("username", "")}</b></p>
                <p>🎖️ Рөл: <b>{r_name}</b></p>
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
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">👨‍💼 ПРЕМЬЕР МИНИСТР</div>', unsafe_allow_html=True)

    st.success(f"Қош келдіңіз, {st.session_state.full_name}!")

    st.markdown("## 📚 Сұрақтар базасы")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Сұрақ қосу", use_container_width=True):
            st.session_state.page = "add_question"
            st.rerun()

    with col2:
        if st.button("📚 Сұрақтар базасы", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()

    st.markdown("---")

    if st.button("👤 Оқушы режиміне өту", use_container_width=True):
        st.session_state.role = "user"
        st.session_state.page = "home"
        st.rerun()

# =========================================================
# ADD QUESTION
# =========================================================
def add_question_page():
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
# RESULTS HISTORY
# =========================================================
def results_history_page():
    st.title("📊 Менің нәтижелерім")

    if st.button("← Басты бетке қайту", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    username = st.session_state.get("username", "Оқушы")
    history = load_results_history()

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
                <p>Дұрыс жауап: <b>{item.get("correct", 0)} / {item.get("total", 0)}</b></p>
                <p>📅 {item.get("date", "")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# PROGRESS
# =========================================================
def progress_page():
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

        if last_score > 0:
            st.caption(f"Қазіргі прогресс: {last_score}%")
        else:
            st.caption("Қазіргі прогресс: 0%")

        st.markdown("---")

# =========================================================
# USER HOME
# =========================================================
def home_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    st.markdown(f"### 👋 Сәлем, {st.session_state.full_name}!")
    st.markdown("## 📚 Пәндер комбинациясы")

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

    for combination in combinations:
        if st.button(combination, use_container_width=True):
            st.session_state.selected_combination = combination
            st.session_state.page = "combination"
            st.rerun()

# =========================================================
# COMBINATION
# =========================================================
def combination_page():
    combination = st.session_state.selected_combination

    st.title(f"📚 {combination}")

    if st.button("← Артқа", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("---")

    main_subjects = combination.split(" + ")
    cols = st.columns(2)

    for i, subject in enumerate(main_subjects):
        with cols[i]:
            count = len(questions.get(subject, []))

            if st.button(f"📘 {subject}\n\n{count} сұрақ", use_container_width=True, key=f"main_{subject}"):
                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.active_questions = []
                st.session_state.result_saved = False
                st.session_state.page = "test"
                st.rerun()

# =========================================================
# TEST
# =========================================================
def test_page():
    subject = st.session_state.selected_subject
    raw_questions = questions.get(subject, [])

    st.title(f"📝 {subject}")

    if st.button("← Пәндерге қайту", use_container_width=True):
        st.session_state.page = "combination"
        st.rerun()

    st.markdown("---")

    if len(raw_questions) == 0:
        st.warning(f"«{subject}» пәнінде әзірге сұрақ жоқ.")
        return

    if st.session_state.current_question == 0 and not st.session_state.active_questions:
        prepared = []
        shuffled_list = random.sample(raw_questions, len(raw_questions))

        for item in shuffled_list:
            answers_copy = item["answers"].copy()
            correct_text = answers_copy[item["correct"]]
            random.shuffle(answers_copy)

            prepared.append({
                "question": item["question"],
                "answers": answers_copy,
                "correct": answers_copy.index(correct_text),
            })

        st.session_state.active_questions = prepared

    subject_questions = st.session_state.active_questions
    current = st.session_state.current_question
    total = len(subject_questions)

    nav_cols = st.columns(min(total, 20))

    for i in range(total):
        col_idx = i % min(total, 20)
        is_current = (i == current)
        is_answered = (i in st.session_state.user_answers and st.session_state.user_answers[i] is not None)

        btn_type = "primary" if is_current else "secondary"

        with nav_cols[col_idx]:
            if st.button(str(i + 1), key=f"nav_btn_{i}", use_container_width=True, type=btn_type):
                st.session_state.current_question = i
                st.rerun()

    st.markdown("---")

    question = subject_questions[current]

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
# RESULT
# =========================================================
def result_page():
    subject = st.session_state.selected_subject
    subject_questions = st.session_state.active_questions
    total = len(subject_questions)

    correct_count = 0
    wrong_questions = []

    for i, question in enumerate(subject_questions):
        user_answer = st.session_state.user_answers.get(i)
        if user_answer == question["correct"]:
            correct_count += 1
        else:
            wrong_questions.append(i)

    wrong_count = total - correct_count
    percent = int(correct_count / total * 100) if total > 0 else 0

    if not st.session_state.get("result_saved", False):
        add_result_to_history(subject, correct_count, total, percent)
        st.session_state.result_saved = True

    st.markdown('<div class="kasym-title">🎯 Тест аяқталды</div>', unsafe_allow_html=True)
    st.markdown(f"## {subject}")
    st.markdown("---")

    st.markdown(
        f"""
        <div class="card">
            <h2>Дұрыс жауап: {correct_count} / {total}</h2>
            <h2>Нәтиже: {percent}%</h2>
            <p>✅ Дұрыс: {correct_count}</p>
            <p>❌ Қате: {wrong_count}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Қайта тапсыру", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.active_questions = []
            st.session_state.result_saved = False
            st.session_state.page = "test"
            st.rerun()

    with col2:
        if st.button("📚 Пәндерге қайту (Артқа)", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.active_questions = []
            st.session_state.page = "combination"
            st.rerun()

    st.markdown("---")
    st.markdown("## ❌ Қате кеткен сұрақтар")

    if len(wrong_questions) == 0:
        st.success("🎉 Барлық сұраққа дұрыс жауап бердіңіз!")
    else:
        for index in wrong_questions:
            question = subject_questions[index]
            user_index = st.session_state.user_answers.get(index)
            correct_index = question["correct"]

            user_text = question["answers"][user_index] if user_index is not None else "Жауап берілмеді"
            correct_text = question["answers"][correct_index]

            st.markdown(
                f"""
                <div class="error-box">
                    <h3>❌ Сұрақ {index + 1}</h3>
                    <p><b>{question["question"]}</b></p>
                    <p>🔴 Сенің жауабың: {user_text}</p>
                    <p>🟢 Дұрыс жауап: {correct_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# ROUTING
# =========================================================
if st.session_state.logged_in:
    top_logout_button()

if not st.session_state.logged_in:
    login_page()
else:
    pg = st.session_state.page

    if pg == "admin":
        if st.session_state.role == "president":
            admin_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "create_user":
        if st.session_state.role == "president":
            create_user_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "users_list":
        if st.session_state.role == "president":
            users_list_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "prime_minister":
        if st.session_state.role == "prime_minister":
            prime_minister_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "add_question":
        if st.session_state.role == "prime_minister":
            add_question_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "question_list":
        question_list_page()

    elif pg == "home":
        home_page()

    elif pg == "combination":
        combination_page()

    elif pg == "test":
        test_page()

    elif pg == "result":
        result_page()

    elif pg == "results_history":
        results_history_page()

    elif pg == "progress":
        progress_page()

    else:
        st.session_state.page = "home"
        st.rerun()
