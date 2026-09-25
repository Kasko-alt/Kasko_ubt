import streamlit as st

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "selected_combination" not in st.session_state:
    st.session_state.selected_combination = ""

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = ""

if "current_question" not in st.session_state:
    st.session_state.current_question = 0


# =========================
# DATA
# =========================

combinations = [
    "Биология + Химия",
    "Физика + Математика",
    "Информатика + Математика",
    "Дүниежүзі тарихы + Ағылшын тілі",
    "Биология + География",
    "География + Математика",
    "Дүниежүзі тарихы + Құқық"
]

common_subjects = [
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық"
]


# =========================
# QUESTIONS
# =========================

questions = {

    "Информатика": [
        {
            "question": "Python тілінде экранға мәтін шығару үшін қай функция қолданылады?",
            "answers": [
                "input()",
                "print()",
                "len()",
                "type()"
            ],
            "correct": "print()"
        },

        {
            "question": "Python тілінде пайдаланушыдан мәлімет енгізу үшін қай функция қолданылады?",
            "answers": [
                "print()",
                "input()",
                "int()",
                "str()"
            ],
            "correct": "input()"
        },

        {
            "question": "Python тілінде бүтін санның типі қалай аталады?",
            "answers": [
                "float",
                "str",
                "int",
                "bool"
            ],
            "correct": "int"
        },

        {
            "question": "Тізімдегі элементтердің санын анықтау үшін қай функция қолданылады?",
            "answers": [
                "sum()",
                "type()",
                "len()",
                "print()"
            ],
            "correct": "len()"
        },

        {
            "question": "Python тілінде қалдықты табу операторы қайсы?",
            "answers": [
                "/",
                "//",
                "%",
                "*"
            ],
            "correct": "%"
        }
    ]
}


# =========================
# CSS
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(37, 99, 235, 0.18), transparent 30%),
        radial-gradient(circle at 80% 90%, rgba(59, 130, 246, 0.12), transparent 30%),
        #07111f;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 35px;
    padding-bottom: 50px;
}


/* =========================
   LOGIN
   ========================= */

.login-container {
    max-width: 520px;
    margin: 90px auto 0 auto;
    padding: 45px;
    background: rgba(15, 31, 52, 0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.login-logo {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.login-slogan {
    text-align: center;
    color: #9fb0c7;
    font-size: 15px;
    margin-bottom: 35px;
}


/* =========================
   HEADER
   ========================= */

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 45px;
}

.logo {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 1px;
}

.logo span {
    color: #4f8cff;
}

.slogan {
    color: #9fb0c7;
    font-size: 13px;
}


/* =========================
   HOME
   ========================= */

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.main-subtitle {
    color: #8fa3bd;
    font-size: 16px;
    margin-bottom: 40px;
}

.section-title {
    font-size: 23px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 20px;
}

.combo-title {
    background: rgba(20, 40, 65, 0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 20px 24px;
    margin-top: 12px;
    margin-bottom: 4px;
    font-size: 18px;
    font-weight: 700;
}


/* =========================
   SUBJECT
   ========================= */

.subject-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.subject-subtitle {
    color: #8fa3bd;
    margin-bottom: 35px;
}

.test-card {
    background: rgba(15, 31, 52, 0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 25px;
    padding: 30px;
    margin-top: 20px;
}

.question-number {
    color: #5d9bff;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 15px;
}

.question-text {
    font-size: 23px;
    font-weight: 700;
    line-height: 1.45;
    margin-bottom: 25px;
}


/* =========================
   BUTTONS
   ========================= */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: #12243b;
    color: white;
    font-weight: 600;
    min-height: 48px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #1b3556;
    border-color: #4f8cff;
}

.login-button .stButton > button {
    background: #2563eb;
}

.login-button .stButton > button:hover {
    background: #3474f2;
}


/* =========================
   INPUT
   ========================= */

.stTextInput input {
    background: #0c1b2d;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 13px;
}

.stTextInput label {
    color: #b8c7da;
}


/* =========================
   RADIO
   ========================= */

.stRadio label {
    color: white !important;
}

.stRadio > div {
    gap: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-container">

        <div class="login-logo">
            KASYM <span style="color:#4f8cff;">EDU</span>
        </div>

        <div class="login-slogan">
            Бүгінгі дайындық — ертеңгі грант
        </div>

    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Логин")
    password = st.text_input("Құпия сөз", type="password")

    st.markdown('<div class="login-button">', unsafe_allow_html=True)

    if st.button("Кіру →"):
        if username.strip() and password.strip():
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Логин мен құпия сөзді енгізіңіз.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# =========================
# HEADER
# =========================

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("""
    <div class="header">
        <div>
            <div class="logo">
                KASYM <span>EDU</span>
            </div>
            <div class="slogan">
                Бүгінгі дайындық — ертеңгі грант
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Шығу"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()


# =========================
# HOME PAGE
# =========================

if st.session_state.page == "home":

    st.markdown("""
    <div class="main-title">
        ҰБТ-ға дайындық
    </div>

    <div class="main-subtitle">
        Өз бағытыңды таңда да, дайындықты баста.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📚 Пәндік комбинациялар</div>',
        unsafe_allow_html=True
    )

    for i, combination in enumerate(combinations):

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(
                f'<div class="combo-title">{combination}</div>',
                unsafe_allow_html=True
            )

        with col2:
            if st.button("→", key=f"combo_{i}"):

                st.session_state.selected_combination = combination
                st.session_state.page = "combination"

                st.rerun()


# =========================
# COMBINATION PAGE
# =========================

elif st.session_state.page == "combination":

    combination = st.session_state.selected_combination

    st.markdown(
        f'<div class="subject-title">{combination}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subject-subtitle">Пәнді таңдаңыз</div>',
        unsafe_allow_html=True
    )

    # MAIN SUBJECTS

    main_subjects = combination.split(" + ")

    st.markdown(
        '<div class="section-title">🎯 Негізгі пәндер</div>',
        unsafe_allow_html=True
    )

    for i, subject in enumerate(main_subjects):

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(
                f'<div class="combo-title">{subject}</div>',
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                "→",
                key=f"main_subject_{i}_{subject}"
            ):

                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.page = "test"

                st.rerun()


    # COMMON SUBJECTS

    st.markdown(
        '<div class="section-title">📖 Міндетті пәндер</div>',
        unsafe_allow_html=True
    )

    for i, subject in enumerate(common_subjects):

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(
                f'<div class="combo-title">{subject}</div>',
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                "→",
                key=f"common_subject_{i}_{subject}"
            ):

                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.page = "test"

                st.rerun()


    st.write("")

    if st.button("← Артқа"):

        st.session_state.page = "home"
        st.rerun()


# =========================
# TEST PAGE
# =========================

elif st.session_state.page == "test":

    subject = st.session_state.selected_subject
    question_index = st.session_state.current_question

    st.markdown(
        f'<div class="subject-title">💻 {subject}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subject-subtitle">ҰБТ тесті</div>',
        unsafe_allow_html=True
    )


    # IF QUESTIONS EXIST

    if subject in questions:

        subject_questions = questions[subject]

        # prevent index error
        if question_index >= len(subject_questions):
            question_index = 0
            st.session_state.current_question = 0

        current = subject_questions[question_index]

        st.markdown('<div class="test-card">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="question-number">
                Сұрақ {question_index + 1} / {len(subject_questions)}
            </div>

            <div class="question-text">
                {current["question"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        answer = st.radio(
            "Жауапты таңдаңыз:",
            current["answers"],
            key=f"answer_{subject}_{question_index}"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns([5, 1])

        with col2:

            if st.button("Келесі →"):

                if question_index < len(subject_questions) - 1:

                    st.session_state.current_question += 1
                    st.rerun()

                else:

                    st.success("🎯 Тест аяқталды!")

                    st.info(
                        "Нәтиже шығару жүйесін келесі кезеңде қосамыз."
                    )


    else:

        st.info(
            f"📚 {subject} пәніне сұрақтар әлі қосылған жоқ."
        )

        st.write("")

        if st.button("← Пәндерге қайту"):

            st.session_state.page = "combination"
            st.rerun()
