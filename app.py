import json
import os
import random
import streamlit as st

# =========================================================
# KASYM EDU
# =========================================================

st.set_page_config(page_title="KASYM EDU", page_icon="🎓", layout="wide")

QUESTIONS_FILE = "questions.json"

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
        },
        {
            "question": "Python тілінде бүтін санның типі қалай аталады?",
            "answers": ["float", "str", "int", "bool"],
            "correct": 2,
        },
    ]
}


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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
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
# CSS (КҮҢГІРТ ДИЗАЙН ЖӘНЕ СТИЛЬДЕР)
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0b1b31 50%, #06101d 100%);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 30px;
}

h1, h2, h3, label { color: white !important; }

.kasym-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    margin-bottom: 5px;
    color: #ffffff;
}

.kasym-subtitle {
    text-align: center;
    font-size: 20px;
    color: #8fb8ff;
    margin-bottom: 40px;
}

.card {
    background: rgba(20, 39, 65, 0.85);
    border: 1px solid rgba(100, 160, 255, 0.18);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
}

.error-box {
    background: rgba(220, 50, 70, 0.12);
    border: 1px solid rgba(255, 80, 100, 0.35);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.st-key-top_logout {
    position: fixed !important;
    top: 12px !important;
    right: 25px !important;
    z-index: 999999 !important;
}

div[data-testid="stHorizontalBlock"] button {
    border-radius: 6px !important;
    height: 38px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 0px !important;
}

div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background-color: #8ccfff !important;
    color: #000000 !important;
    border: none !important;
}

div[data-testid="stHorizontalBlock"] button[data-status="answered"] {
    background-color: #4CAF50 !important;
    color: #ffffff !important;
    border: 1px solid #1b5e20 !important;
}

div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background-color: #2196F3 !important;
    color: #000000 !important;
    border: 2px solid #000000 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "login"
    st.session_state.selected_combination = None
    st.session_state.selected_subject = None
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.active_questions = []
    st.rerun()


def top_logout_button():
    if st.button("🚪 Жалпы шығу", key="top_logout"):
        logout()


def login_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🔐 Кіру")

    username = st.text_input("Логин")
    password = st.text_input("Құпия сөз", type="password")

    if st.button("Кіру →", use_container_width=True):
        if username == "kas01" and password == "kasko100228550357":
            st.session_state.logged_in = True
            st.session_state.role = "president"
            st.session_state.page = "admin"
            st.rerun()
        elif username != "" and password != "":
            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Логин мен құпия сөзді енгіз.")
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# ADMIN PAGES (ПРЕЗИДЕНТ ФУНКЦИЯЛАРЫ)
# =========================================================


def admin_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kasym-subtitle">👑 PRESIDENT PANEL</div>', unsafe_allow_html=True
    )
    st.success("Сен Президент режиміндесің.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Сұрақ қосу", use_container_width=True):
            st.session_state.page = "add_question"
            st.rerun()
    with col2:
        if st.button("📚 Пәндер базасы", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()
    with col3:
        if st.button("👤 Оқушы режимі", use_container_width=True):
            st.session_state.role = "user"
            st.session_state.page = "home"
            st.rerun()


def add_question_page():
    st.title("➕ Жас сұрақ қосу")

    if st.button("← Панельге қайту", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

    st.markdown("---")

    selected_subject = st.selectbox("Пәнді таңдаңыз:", all_subjects)
    question_text = st.text_area("Сұрақты жазыңыз:")

    ans1 = st.text_input("А нұсқасы:")
    ans2 = st.text_input("Б нұсқасы:")
    ans3 = st.text_input("В нұсқасы:")
    ans4 = st.text_input("Г нұсқасы:")

    correct_option = st.selectbox(
        "Дұрыс жауап қайсысы?",
        ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"],
    )

    correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(
        correct_option
    )

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
            st.success("Сұрақ сәтті сақталды!")
        else:
            st.error("Барлық өрістерді толтырыңыз!")


def question_list_page():
    st.title("📚 Сұрақтар базасы")

    if st.button("← Панельге қайту", use_container_width=True):
        st.session_state.page = "admin"
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
# USER PAGES (ОҚУШЫ ФУНКЦИЯЛАРЫ)
# =========================================================


def home_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## 📚 Пәндер комбинациясы")

    for combination in combinations:
        if st.button(combination, use_container_width=True):
            st.session_state.selected_combination = combination
            st.session_state.page = "combination"
            st.rerun()


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
            if st.button(
                f"📘 {subject}\n\n{count} сұрақ",
                use_container_width=True,
                key=f"main_{subject}",
            ):
                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.active_questions = []
                st.session_state.page = "test"
                st.rerun()


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

    if (
        st.session_state.current_question == 0
        and not st.session_state.active_questions
    ):
        prepared = []
        shuffled_list = random.sample(raw_questions, len(raw_questions))
        for item in shuffled_list:
            answers_copy = item["answers"].copy()
            correct_text = answers_copy[item["correct"]]
            random.shuffle(answers_copy)
            prepared.append(
                {
                    "question": item["question"],
                    "answers": answers_copy,
                    "correct": answers_copy.index(correct_text),
                }
            )
        st.session_state.active_questions = prepared

    subject_questions = st.session_state.active_questions
    current = st.session_state.current_question
    total = len(subject_questions)

    nav_cols = st.columns(20 if total >= 20 else total)

    for i in range(total):
        col_idx = i % (20 if total >= 20 else total)
        is_current = i == current
        is_answered = (
            i in st.session_state.user_answers
            and st.session_state.user_answers[i] is not None
        )

        label = f"{i + 1}"
        btn_type = "primary" if is_current else "secondary"

        with nav_cols[col_idx]:
            if is_answered and not is_current:
                st.markdown(
                    f"""
                    <script>
                    var elements = window.parent.document.querySelectorAll('button');
                    for (var j = 0; j < elements.length; j++) {{
                        if (elements[j].innerText.trim() === '{i + 1}') {{
                            elements[j].setAttribute('data-status', 'answered');
                        }}
                    }}
                    </script>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button(
                label,
                key=f"nav_btn_{i}",
                use_container_width=True,
                type=btn_type,
            ):
                st.session_state.current_question = i
                st.rerun()

    st.markdown("---")

    question = subject_questions[current]
    st.markdown(f"### Сұрақ {current + 1} / {total}")

    st.markdown(
        f'<div class="card"><h3>{question["question"]}</h3></div>',
        unsafe_allow_html=True,
    )

    saved_index = st.session_state.user_answers.get(current, None)
    answer = st.radio(
        "Жауапты таңдаңыз:",
        question["answers"],
        index=saved_index,
        key=f"question_{current}",
    )

    if answer is not None:
        st.session_state.user_answers[current] = question["answers"].index(
            answer
        )

    col_back, col_next = st.columns(2)
    with col_back:
        if current > 0 and st.button("← Артқа", use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

    with col_next:
        button_label = (
            "Келесі →" if current + 1 < total else "🎯 Тестті аяқтау"
        )
        if st.button(button_label, use_container_width=True):
            if current + 1 < total:
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.session_state.page = "result"
                st.rerun()


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

    st.markdown(
        '<div class="kasym-title">🎯 Тест аяқталды</div>', unsafe_allow_html=True
    )
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
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Қайта тапсыру", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.active_questions = []
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

            user_text = (
                question["answers"][user_index]
                if user_index is not None
                else "Жауап берілмеді"
            )
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
                unsafe_allow_html=True,
            )


# =========================================================
# ROUTING (БЕТТЕРДІ БАСҚАРУ)
# =========================================================

if st.session_state.logged_in:
    top_logout_button()

if not st.session_state.logged_in:
    login_page()
else:
    pg = st.session_state.page
    if pg == "admin":
        admin_page()
    elif pg == "add_question":
        add_question_page()
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
