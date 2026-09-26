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
# CSS (СУРЕТТЕГІДЕЙ БАТЫРМА СТИЛЬДЕРІ)
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background: #ffffff;
    color: #000000;
}

.block-container {
    max-width: 1200px;
    padding-top: 20px;
}

/* Навигация батырмаларының ортақ стилі */
div[data-testid="stHorizontalBlock"] button {
    border-radius: 6px !important;
    height: 38px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 0px !important;
    margin: 2px !important;
}

/* 1. Белгіленбеген (әлі жауап берілмеген) сұрақтар - Ашық көк */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background-color: #8ccfff !important;
    color: #000000 !important;
    border: none !important;
}

/* 2. Жауап берілген сұрақтар - Жасыл */
div[data-testid="stHorizontalBlock"] button[data-status="answered"] {
    background-color: #4CAF50 !important;
    color: #ffffff !important;
    border: 1px solid #1b5e20 !important;
}

/* 3. Ағымдағы белсенді сұрақ - Қанық көк + Қара жиек */
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
    if st.button("🚪 Шығу", key="top_logout"):
        logout()


def login_page():
    st.title("🎓 KASYM EDU")
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
            st.error("Логин мен құпия сөзді енгізіңіз.")


def home_page():
    st.title("📚 Пәндер комбинациясы")
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
                f"📘 {subject} ({count} сұрақ)",
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

    # =========================================================
    # СУРЕТТЕГІДЕЙ СҰРАҚТАР НЕНАВИГАЦИЯСЫ
    # =========================================================
    nav_cols = st.columns(20)

    for i in range(total):
        col_idx = i % 20
        is_current = i == current
        is_answered = (
            i in st.session_state.user_answers
            and st.session_state.user_answers[i] is not None
        )

        label = f"{i + 1}"

        if is_current:
            btn_type = "primary"
        else:
            btn_type = "secondary"

        with nav_cols[col_idx]:
            # Жауап берілген сұрақты жасыл түске бояу
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

    st.subheader(question["question"])

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
    st.title("🎯 Тест аяқталды")


if st.session_state.logged_in:
    top_logout_button()

if not st.session_state.logged_in:
    login_page()
else:
    pg = st.session_state.page
    if pg == "home":
        home_page()
    elif pg == "combination":
        combination_page()
    elif pg == "test":
        test_page()
    elif pg == "result":
        result_page()
