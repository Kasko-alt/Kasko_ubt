```python
import streamlit as st

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_combination" not in st.session_state:
    st.session_state.selected_combination = None

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "current_question" not in st.session_state:
    st.session_state.current_question = 0


# ==========================================
# НЕГІЗГІ ПӘН КОМБИНАЦИЯЛАРЫ
# ==========================================

combinations = [

    ("🧬⚗️", "Биология + Химия",
     "Биология • Химия"),

    ("⚡📐", "Физика + Математика",
     "Физика • Математика"),

    ("💻📐", "Информатика + Математика",
     "Информатика • Математика"),

    ("🌍🇬🇧", "Дүниежүзі тарихы + Ағылшын тілі",
     "Дүниежүзі тарихы • Ағылшын тілі"),

    ("🧬🌍", "Биология + География",
     "Биология • География"),

    ("🌍📐", "География + Математика",
     "География • Математика"),

    ("🌍⚖️", "Дүниежүзі тарихы + Құқық",
     "Дүниежүзі тарихы • Құқық"),

]


# ==========================================
# ОРТАҚ МІНДЕТТІ ПӘНДЕР
# ==========================================

common_subjects = [
    ("🇰🇿", "Қазақстан тарихы"),
    ("📖", "Оқу сауаттылығы"),
    ("🧠", "Математикалық сауаттылық"),
]


# ==========================================
# ТЕСТ СҰРАҚТАРЫ
# ==========================================

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
            "correct": 1
        },

        {
            "question": "Python-да пайдаланушыдан мәлімет енгізу үшін қай функция қолданылады?",
            "answers": [
                "print()",
                "input()",
                "len()",
                "str()"
            ],
            "correct": 1
        },

        {
            "question": "Python-да бүтін санның типі қалай жазылады?",
            "answers": [
                "float",
                "str",
                "int",
                "bool"
            ],
            "correct": 2
        },

        {
            "question": "Тізімнің элементтер санын анықтайтын функция:",
            "answers": [
                "sum()",
                "type()",
                "len()",
                "input()"
            ],
            "correct": 2
        },

        {
            "question": "Python-да қалдықты табу операторы:",
            "answers": [
                "/",
                "//",
                "%",
                "**"
            ],
            "correct": 2
        },

    ]
}


# ==========================================
# DESIGN
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(0, 130, 255, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 75%,
            rgba(0, 200, 255, 0.10),
            transparent 30%
        ),
        #020817;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 1150px !important;
    padding-top: 35px !important;
}


/* ==========================================
   LOGIN
========================================== */

.login-title {
    text-align: center;
    color: white;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-top: 130px;
}

.login-title span {
    color: #39bfff;
}

.login-text {
    text-align: center;
    color: rgba(255,255,255,0.50);
    font-size: 14px;
    margin-bottom: 35px;
}


/* ==========================================
   INPUT
========================================== */

.stTextInput label {
    color: rgba(255,255,255,0.75) !important;
    font-weight: 600 !important;
}

.stTextInput input {
    height: 50px !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: white !important;
}


/* ==========================================
   BUTTON
========================================== */

.stButton button {
    height: 50px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    font-weight: 700 !important;
    transition: 0.2s;
}

.stButton button:hover {
    background: rgba(57,191,255,0.12) !important;
    border-color: rgba(57,191,255,0.35) !important;
    transform: translateY(-2px);
}


/* ==========================================
   LOGIN BUTTON
========================================== */

.login-button button {
    background: linear-gradient(
        135deg,
        #39bfff,
        #1677ff
    ) !important;

    border: none !important;
}


/* ==========================================
   LOGO
========================================== */

.home-logo {
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.home-logo span {
    color: #39bfff;
}


/* ==========================================
   HOME TITLE
========================================== */

.home-title {
    color: white;
    font-size: 58px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -3px;
    margin-top: 100px;
}

.home-title span {
    color: #39bfff;
}

.home-description {
    color: rgba(255,255,255,0.48);
    font-size: 15px;
    margin-top: 20px;
    line-height: 1.6;
}


/* ==========================================
   SECTION
========================================== */

.section-title {
    color: white;
    font-size: 28px;
    font-weight: 700;
    margin-top: 70px;
    margin-bottom: 30px;
}


/* ==========================================
   SUBJECT
========================================== */

.subject-number {
    color: #39bfff;
    font-size: 13px;
    font-weight: 700;
}

.subject-name {
    color: white;
    font-size: 21px;
    font-weight: 700;
    margin-top: 5px;
}

.subject-info {
    color: rgba(255,255,255,0.38);
    font-size: 12px;
    margin-top: 5px;
}


/* ==========================================
   COMBINATION TITLE
========================================== */

.combo-title {
    color: white;
    font-size: 48px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
    margin-top: 80px;
}

.combo-description {
    color: rgba(255,255,255,0.48);
    font-size: 15px;
    margin-top: 18px;
}


/* ==========================================
   COMMON SUBJECT
========================================== */

.common-heading {
    color: rgba(255,255,255,0.55);
    font-size: 15px;
    font-weight: 700;
    margin-top: 45px;
    margin-bottom: 20px;
}


/* ==========================================
   TEST
========================================== */

.test-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-top: 60px;
}

.test-progress {
    color: #39bfff;
    font-size: 15px;
    font-weight: 700;
    margin-top: 12px;
}

.question-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 35px;
    margin-top: 30px;
    margin-bottom: 25px;
}

.question-text {
    color: white;
    font-size: 23px;
    font-weight: 700;
    line-height: 1.5;
}

.answer-label {
    color: rgba(255,255,255,0.55);
    font-size: 14px;
    font-weight: 600;
    margin-top: 25px;
}

.test-back {
    margin-top: 25px;
}


/* ==========================================
   FOOTER
========================================== */

.footer {
    color: rgba(255,255,255,0.22);
    text-align: center;
    font-size: 10px;
    margin-top: 80px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOGIN
# ==========================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="login-title">KASYM<span>•</span>EDU</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-text">Бүгінгі дайындық — ертеңгі грант</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1.2, 1, 1.2])

    with center:

        login = st.text_input(
            "Логин",
            placeholder="Логиніңізді енгізіңіз"
        )

        password = st.text_input(
            "Құпиясөз",
            type="password",
            placeholder="Құпиясөзіңізді енгізіңіз"
        )

        st.markdown(
            '<div class="login-button">',
            unsafe_allow_html=True
        )

        if st.button(
            "Кіру →",
            use_container_width=True
        ):

            if login and password:

                st.session_state.logged_in = True
                st.session_state.page = "home"

                st.rerun()

            else:

                st.error(
                    "Логин мен құпиясөзді енгізіңіз."
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ==========================================
# MAIN SITE
# ==========================================

else:

    # ======================================
    # HEADER
    # ======================================

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown(
            '<div class="home-logo">KASYM<span>•</span>EDU</div>',
            unsafe_allow_html=True
        )

    with col2:

        if st.button(
            "Шығу",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.page = "home"

            st.rerun()


    # ======================================
    # HOME
    # ======================================

    if st.session_state.page == "home":

        st.markdown(
            """
            <div class="home-title">
                Бүгінгі дайындық —<br>
                <span>ертеңгі грант.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="home-description">
                ҰБТ-ға дайындал. Біліміңді тексер.
                Қателеріңді талда. Нәтижеңді жақсарт.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">📚 Пәндер</div>',
            unsafe_allow_html=True
        )


        # ==================================
        # 7 КОМБИНАЦИЯ
        # ==================================

        for i, (icon, name, info) in enumerate(combinations):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="subject-number">
                        {i + 1:02d}
                    </div>

                    <div class="subject-name">
                        {icon} {name}
                    </div>

                    <div class="subject-info">
                        {info}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "→",
                    key=f"combo_{i}",
                    use_container_width=True
                ):

                    st.session_state.selected_combination = name
                    st.session_state.page = "combination"

                    st.rerun()

            st.divider()


        st.markdown(
            '<div class="footer">© 2026 KASYM EDU</div>',
            unsafe_allow_html=True
        )


    # ======================================
    # COMBINATION PAGE
    # ======================================

    elif st.session_state.page == "combination":

        selected = st.session_state.selected_combination

        st.markdown(
            f"""
            <div class="combo-title">
                {selected}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="combo-description">
                Осы бағыт бойынша ҰБТ дайындығы
            </div>
            """,
            unsafe_allow_html=True
        )


        # ==================================
        # НЕГІЗГІ ПӘНДЕР
        # ==================================

        st.markdown(
            '<div class="section-title">Негізгі пәндер</div>',
            unsafe_allow_html=True
        )

        selected_parts = selected.split(" + ")


        for i, subject in enumerate(selected_parts):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="subject-number">
                        {i + 1:02d}
                    </div>

                    <div class="subject-name">
                        📚 {subject}
                    </div>

                    <div class="subject-info">
                        ҰБТ тесттері • Тақырыптар • Қателерді талдау
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "→",
                    key=f"main_subject_{i}_{subject}",
                    use_container_width=True
                ):

                    st.session_state.selected_subject = subject
                    st.session_state.current_question = 0

                    st.session_state.page = "test"

                    st.rerun()

            st.divider()


        # ==================================
        # ОРТАҚ ПӘНДЕР
        # ==================================

        st.markdown(
            '<div class="common-heading">Барлық комбинацияға ортақ міндетті пәндер</div>',
            unsafe_allow_html=True
        )


        for i, (icon, subject) in enumerate(common_subjects):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"""
                    <div class="subject-number">
                        {i + 3:02d}
                    </div>

                    <div class="subject-name">
                        {icon} {subject}
                    </div>

                    <div class="subject-info">
                        ҰБТ тесттері • Тақырыптар • Қателерді талдау
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "→",
                    key=f"common_subject_{i}",
                    use_container_width=True
                ):

                    st.session_state.selected_subject = subject
                    st.session_state.current_question = 0

                    st.session_state.page = "test"

                    st.rerun()

            st.divider()


        # ==================================
        # BACK
        # ==================================

        if st.button(
            "← Пәндерге қайту",
            use_container_width=False
        ):

            st.session_state.page = "home"
            st.session_state.selected_combination = None

            st.rerun()


        st.markdown(
            '<div class="footer">© 2026 KASYM EDU</div>',
            unsafe_allow_html=True
        )


    # ======================================
    # TEST PAGE
    # ======================================

    elif st.session_state.page == "test":

        subject = st.session_state.selected_subject

        # ----------------------------------
        # BACK
        # ----------------------------------

        if st.button("← Пәнге қайту"):

            st.session_state.page = "combination"

            st.rerun()


        # ----------------------------------
        # ТЕК ҚАЗІР ИНФОРМАТИКА ТЕСТІ
        # ----------------------------------

        if subject not in questions:

            st.markdown(
                f"""
                <div class="test-title">
                    {subject}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "Бұл пәннің тесттері келесі кезеңде қосылады."
            )

        else:

            test_questions = questions[subject]

            question_number = st.session_state.current_question

            # ----------------------------------
            # TEST HEADER
            # ----------------------------------

            st.markdown(
                f"""
                <div class="test-title">
                    💻 {subject}
                </div>

                <div class="test-progress">
                    ҰБТ тесті • Сұрақ {question_number + 1} / 20
                </div>
                """,
                unsafe_allow_html=True
            )


            # ----------------------------------
            # QUESTION
            # ----------------------------------

            q = test_questions[
                question_number % len(test_questions)
            ]

            st.markdown(
                f"""
                <div class="que
```
