import streamlit as st

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

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

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}


# =========================================================
# COMBINATIONS
# =========================================================

combinations = [
    "Биология + Химия",
    "Физика + Математика",
    "Информатика + Математика",
    "Дүниежүзі тарихы + Ағылшын тілі",
    "Биология + География",
    "География + Математика",
    "Дүниежүзі тарихы + Құқық"
]


# =========================================================
# COMMON SUBJECTS
# =========================================================

common_subjects = [
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық"
]


# =========================================================
# 20 INFORMATICS QUESTIONS
# =========================================================

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
            "question": "Python тіліндегі бүтін санның типі қайсы?",
            "answers": [
                "float",
                "str",
                "int",
                "bool"
            ],
            "correct": "int"
        },

        {
            "question": "Python тілінде бөлудің нәтижесін нақты сан түрінде беретін оператор қайсы?",
            "answers": [
                "//",
                "%",
                "/",
                "*"
            ],
            "correct": "/"
        },

        {
            "question": "Python тілінде қалдықты табу операторы қайсы?",
            "answers": [
                "/",
                "//",
                "%",
                "**"
            ],
            "correct": "%"
        },

        {
            "question": "Python тілінде бүтін бөлу операторы қайсы?",
            "answers": [
                "/",
                "//",
                "%",
                "**"
            ],
            "correct": "//"
        },

        {
            "question": "Python тілінде дәрежеге шығару операторы қайсы?",
            "answers": [
                "^",
                "**",
                "//",
                "%%"
            ],
            "correct": "**"
        },

        {
            "question": "Тізімдегі элементтер санын анықтайтын функция қайсы?",
            "answers": [
                "sum()",
                "len()",
                "type()",
                "input()"
            ],
            "correct": "len()"
        },

        {
            "question": "Python тілінде екі шарттың екеуі де ақиқат болған жағдайда қолданылатын оператор қайсы?",
            "answers": [
                "or",
                "not",
                "and",
                "in"
            ],
            "correct": "and"
        },

        {
            "question": "Python тілінде кемінде бір шарт ақиқат болған жағдайда қолданылатын оператор қайсы?",
            "answers": [
                "and",
                "or",
                "not",
                "in"
            ],
            "correct": "or"
        },

        {
            "question": "Python тілінде шартты тексеру үшін қай оператор қолданылады?",
            "answers": [
                "for",
                "if",
                "while",
                "def"
            ],
            "correct": "if"
        },

        {
            "question": "Python тіліндегі цикл операторын көрсетіңіз.",
            "answers": [
                "if",
                "else",
                "for",
                "print"
            ],
            "correct": "for"
        },

        {
            "question": "Python тілінде логикалық мәндерді көрсететін тип қайсы?",
            "answers": [
                "int",
                "float",
                "bool",
                "str"
            ],
            "correct": "bool"
        },

        {
            "question": "Python тілінде мәтіндік тип қалай аталады?",
            "answers": [
                "str",
                "int",
                "float",
                "bool"
            ],
            "correct": "str"
        },

        {
            "question": "Python тілінде нақты сандардың типі қайсы?",
            "answers": [
                "int",
                "str",
                "float",
                "bool"
            ],
            "correct": "float"
        },

        {
            "question": "Python тілінде санды бүтін санға айналдыратын функция қайсы?",
            "answers": [
                "str()",
                "float()",
                "int()",
                "bool()"
            ],
            "correct": "int()"
        },

        {
            "question": "Python тілінде санды нақты санға айналдыратын функция қайсы?",
            "answers": [
                "int()",
                "float()",
                "str()",
                "len()"
            ],
            "correct": "float()"
        },

        {
            "question": "Python тілінде мәннің типін анықтайтын функция қайсы?",
            "answers": [
                "type()",
                "len()",
                "sum()",
                "input()"
            ],
            "correct": "type()"
        },

        {
            "question": "Python тілінде тізім қалай жазылады?",
            "answers": [
                "(1, 2, 3)",
                "{1, 2, 3}",
                "[1, 2, 3]",
                "<1, 2, 3>"
            ],
            "correct": "[1, 2, 3]"
        },

        {
            "question": "Python тілінде 10 % 3 өрнегінің нәтижесі қандай?",
            "answers": [
                "0",
                "1",
                "3",
                "10"
            ],
            "correct": "1"
        }

    ]
}


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 20% 10%,
            rgba(37, 99, 235, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 90%,
            rgba(59, 130, 246, 0.12),
            transparent 30%
        ),
        #07111f;

    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 35px;
    padding-bottom: 50px;
}


/* LOGIN */

.login-logo {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 45px;
    margin-bottom: 8px;
    color: white;
}

.login-logo span {
    color: #4f8cff;
}

.login-slogan {
    text-align: center;
    color: #9fb0c7;
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 40px;
}

.login-box {
    max-width: 590px;
    margin: 20px auto 0 auto;
    padding: 42px;
    background: rgba(15, 31, 52, 0.92);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}


/* HEADER */

.header-logo {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: 1px;
}

.header-logo span {
    color: #4f8cff;
}

.header-slogan {
    color: #9fb0c7;
    font-size: 13px;
}


/* HOME */

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-top: 20px;
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


/* SUBJECT */

.subject-title {
    font-size: 34px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 8px;
}

.subject-subtitle {
    color: #8fa3bd;
    margin-bottom: 35px;
}


/* TEST */

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


/* BUTTONS */

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


/* INPUT */

.stTextInput input {
    background: #0c1b2d;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 13px;
}

.stTextInput label {
    color: #b8c7da;
}


/* RADIO */

.stRadio label {
    color: white !important;
}

.stRadio > div {
    gap: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-logo">KASYM <span>EDU</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-slogan">Бүгінгі дайындық — ертеңгі грант</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Логин",
        key="login_username"
    )

    password = st.text_input(
        "Құпия сөз",
        type="password",
        key="login_password"
    )

    if st.button("Кіру →", key="login_button"):

        if username.strip() and password.strip():

            st.session_state.logged_in = True
            st.session_state.page = "home"

            st.rerun()

        else:

            st.error("Логин мен құпия сөзді енгізіңіз.")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        """
        <div class="header-logo">
            KASYM <span>EDU</span>
        </div>

        <div class="header-slogan">
            Бүгінгі дайындық — ертеңгі грант
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    if st.button("Шығу", key="logout"):

        st.session_state.logged_in = False
        st.session_state.page = "login"

        st.rerun()


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="main-title">
            ҰБТ-ға дайындық
        </div>

        <div class="main-subtitle">
            Өз бағытыңды таңда да, дайындықты баста.
        </div>
        """,
        unsafe_allow_html=True
    )

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

            if st.button(
                "→",
                key=f"combo_{i}"
            ):

                st.session_state.selected_combination = combination
                st.session_state.page = "combination"

                st.rerun()


# =========================================================
# COMBINATION PAGE
# =========================================================

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

    st.markdown(
        '<div class="section-title">🎯 Негізгі пәндер</div>',
        unsafe_allow_html=True
    )

    main_subjects = combination.split(" + ")

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
                key=f"main_{i}_{subject}"
            ):

                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
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
                key=f"common_{i}_{subject}"
            ):

                st.session_state.selected_subject = subject
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.session_state.page = "test"

                st.rerun()


    st.write("")

    if st.button("← Артқа", key="back_home"):

        st.session_state.page = "home"
        st.rerun()


# =========================================================
# TEST PAGE
# =========================================================

elif st.session_state.page == "test":

    subject = st.session_state.selected_subject
    question_index = st.session_state.current_question

    st.markdown(
        f'<div class="subject-title">📚 {subject}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subject-subtitle">ҰБТ тесті</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # SUBJECT HAS QUESTIONS
    # =====================================================

    if subject in questions:

        subject_questions = questions[subject]

        current = subject_questions[question_index]

        st.markdown(
            '<div class="test-card">',
            unsafe_allow_html=True
        )

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


        # CURRENT ANSWER

        saved_answer = st.session_state.user_answers.get(
            question_index,
            None
        )

        answer = st.radio(
            "Жауапты таңдаңыз:",
            current["answers"],
            index=(
                current["answers"].index(saved_answer)
                if saved_answer in current["answers"]
                else None
            ),
            key=f"radio_{question_index}"
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        st.write("")


        # SAVE ANSWER + NEXT

        col1, col2 = st.columns([5, 1])

        with col2:

            if st.button(
                "Келесі →",
                key=f"next_{question_index}"
            ):

                if answer is None:

                    st.warning(
                        "Алдымен жауапты таңда!"
                    )

                else:

                    # Жауапты сақтау
                    st.session_state.user_answers[
                        question_index
                    ] = answer


                    # Келесі сұрақ
                    if question_index < len(subject_questions) - 1:

                        st.session_state.current_question += 1

                        st.rerun()

                    else:

                        # Соңғы сұрақ
                        st.session_state.page = "result"

                        st.rerun()


    # =====================================================
    # SUBJECT WITHOUT QUESTIONS
    # =====================================================

    else:

        st.info(
            f"📚 {subject} пәніне сұрақтар әлі қосылған жоқ."
        )

        st.write("")

        if st.button(
            "← Пәндерге қайту",
            key="back_subjects"
        ):

            st.session_state.page = "combination"

            st.rerun()


# =========================================================
# RESULT PAGE
# =========================================================

elif st.session_state.page == "result":

    subject = st.session_state.selected_subject

    subject_questions = questions[subject]

    correct_count = 0

    for i, question in enumerate(subject_questions):

        user_answer = st.session_state.user_answers.get(
            i,
            None
        )

        if user_answer == question["correct"]:

            correct_count += 1


    total = len(subject_questions)

    percentage = int(
        correct_count / total * 100
    )


    st.markdown(
        """
        <div class="subject-title">
            🎯 Тест аяқталды
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="test-card">

            <div class="question-text">
                Дұрыс жауап: {correct_count} / {total}
            </div>

            <div class="question-text">
                Нәтиже: {percentage}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"✅ Дұрыс: {correct_count}"
        )

    with col2:

        st.error(
            f"❌ Қате: {total - correct_count}"
        )


    st.write("")

    if st.button(
        "← Пәндерге қайту",
        key="result_back"
    ):

        st.session_state.page = "combination"

        st.session_state.current_question = 0

        st.session_state.user_answers = {}

        st.rerun()
