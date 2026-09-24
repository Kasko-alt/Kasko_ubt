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


# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Manrope', sans-serif;
}

.stApp {

    min-height: 100vh;

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


/* ==========================================
   STREAMLIT
========================================== */

header {
    background: transparent !important;
}

.block-container {
    max-width: 1200px !important;
    padding-top: 25px !important;
}


/* ==========================================
   LOGIN
========================================== */

.login-page {

    min-height: 90vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

}


/* ==========================================
   LOGO
========================================== */

.login-logo {

    font-size: 46px;

    font-weight: 800;

    letter-spacing: -2px;

    color: white;

    margin-bottom: 8px;

}

.login-logo span {

    color: #39bfff;

}


/* ==========================================
   SLOGAN
========================================== */

.login-slogan {

    color: rgba(255,255,255,0.48);

    font-size: 14px;

    font-weight: 500;

    margin-bottom: 35px;

}


/* ==========================================
   INPUTS
========================================== */

.stTextInput {

    margin-bottom: 5px;

}

.stTextInput label {

    color: rgba(255,255,255,0.70) !important;

    font-size: 13px !important;

    font-weight: 600 !important;

}

.stTextInput > div > div > input {

    height: 52px !important;

    background: rgba(255,255,255,0.045) !important;

    border: 1px solid rgba(255,255,255,0.13) !important;

    border-radius: 13px !important;

    color: white !important;

    font-family: 'Manrope', sans-serif !important;

    font-size: 14px !important;

}

.stTextInput > div > div > input:focus {

    border-color: #39bfff !important;

    box-shadow:
        0 0 0 2px rgba(57,191,255,0.10) !important;

}


/* ==========================================
   LOGIN BUTTON
========================================== */

.stButton {

    margin-top: 17px;

}

.stButton > button {

    height: 52px !important;

    border-radius: 13px !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #39bfff,
            #1677ff
        ) !important;

    color: white !important;

    font-family: 'Manrope', sans-serif !important;

    font-size: 14px !important;

    font-weight: 700 !important;

    transition: 0.25s;

}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(22,119,255,0.30);

}


/* ==========================================
   HOME
========================================== */

.home-top {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding-top: 10px;

}


.home-logo {

    font-size: 27px;

    font-weight: 800;

    letter-spacing: -1px;

    color: white;

}

.home-logo span {

    color: #39bfff;

}


/* ==========================================
   HOME TITLE
========================================== */

.home-title {

    margin-top: 100px;

    font-size: clamp(45px, 6vw, 76px);

    line-height: 1.05;

    font-weight: 800;

    letter-spacing: -3px;

    color: white;

}

.home-title span {

    color: #39bfff;

}


.home-description {

    margin-top: 20px;

    color: rgba(255,255,255,0.48);

    font-size: 15px;

    max-width: 600px;

    line-height: 1.7;

}


/* ==========================================
   SUBJECTS
========================================== */

.subject-section {

    margin-top: 75px;

}


.subject-heading {

    color: white;

    font-size: 24px;

    font-weight: 700;

    margin-bottom: 25px;

}


.subject {

    padding: 20px 0;

    border-bottom:
        1px solid rgba(255,255,255,0.09);

    cursor: pointer;

    transition: 0.25s;

}


.subject:hover {

    padding-left: 12px;

}


.subject-number {

    color: #39bfff;

    font-size: 13px;

    font-weight: 700;

}


.subject-name {

    color: white;

    font-size: 20px;

    font-weight: 600;

    margin-top: 4px;

}


.subject-info {

    color: rgba(255,255,255,0.35);

    font-size: 12px;

    margin-top: 4px;

}


/* ==========================================
   FOOTER
========================================== */

.footer {

    margin-top: 100px;

    padding-bottom: 30px;

    color: rgba(255,255,255,0.22);

    font-size: 10px;

}


/* ==========================================
   ALERT
========================================== */

.stAlert {

    border-radius: 10px !important;

}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-page">

        <div class="login-logo">
            KASYM<span>•</span>EDU
        </div>

        <div class="login-slogan">
            Бүгінгі дайындық — ертеңгі грант
        </div>

    </div>
    """, unsafe_allow_html=True)


    # Input ортасында
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

        if st.button(
            "Кіру  →",
            use_container_width=True
        ):

            if login and password:

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error(
                    "Логин мен құпиясөзді енгізіңіз."
                )


# ==========================================
# HOME PAGE
# ==========================================

else:

    # --------------------------------------
    # TOP
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="home-top">

            <div class="home-logo">
                KASYM<span>•</span>EDU
            </div>

        </div>
        """, unsafe_allow_html=True)


    with col2:

        if st.button(
            "Шығу",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.rerun()


    # --------------------------------------
    # MAIN TITLE
    # --------------------------------------

    st.markdown("""
    <div class="home-title">
        Бүгінгі дайындық —<br>
        <span>ертеңгі грант.</span>
    </div>

    <div class="home-description">
        ҰБТ-ға дайындал. Біліміңді тексер.
        Қателеріңді талда. Нәтижеңді жақсарт.
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # SUBJECTS
    # --------------------------------------

    st.markdown("""
    <div class="subject-section">

        <div class="subject-heading">
            Пәндер
        </div>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # SUBJECT 1
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                01
            </div>

            <div class="subject-name">
                📐 Математика
            </div>

            <div class="subject-info">
                ҰБТ есептері • Тесттер • Қателерді талдау
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="math",
            use_container_width=True
        )


    # --------------------------------------
    # SUBJECT 2
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                02
            </div>

            <div class="subject-name">
                💻 Информатика
            </div>

            <div class="subject-info">
                Python • Теория • ҰБТ тесттері
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="informatics",
            use_container_width=True
        )


    # --------------------------------------
    # SUBJECT 3
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                03
            </div>

            <div class="subject-name">
                🇰🇿 Қазақстан тарихы
            </div>

            <div class="subject-info">
                Даталар • Оқиғалар • Тесттер
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="history",
            use_container_width=True
        )


    # --------------------------------------
    # SUBJECT 4
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                04
            </div>

            <div class="subject-name">
                📖 Оқу сауаттылығы
            </div>

            <div class="subject-info">
                Мәтіндер • Талдау • Тесттер
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="reading",
            use_container_width=True
        )


    # --------------------------------------
    # SUBJECT 5
    # --------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                05
            </div>

            <div class="subject-name">
                🧠 Математикалық сауаттылық
            </div>

            <div class="subject-info">
                Логика • Формулалар • Есептер
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="math_literacy",
            use_container_width=True
        )


    # --------------------------------------
    # RESULTS
    # --------------------------------------

    st.markdown("""
    <div class="subject-section">

        <div class="subject-heading">
            Менің нәтижелерім
        </div>

    </div>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown("""
        <div class="subject">

            <div class="subject-number">
                06
            </div>

            <div class="subject-name">
                🎯 Нәтижелер мен қателер
            </div>

            <div class="subject-info">
                Дұрыс жауаптар • Қате сұрақтар • Прогресс
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.button(
            "→",
            key="results",
            use_container_width=True
        )


    # --------------------------------------
    # FOOTER
    # --------------------------------------

    st.markdown("""
    <div class="footer">
        © 2026 KASYM EDU
    </div>
    """, unsafe_allow_html=True)
