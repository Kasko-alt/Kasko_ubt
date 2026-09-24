import streamlit as st

# ==========================================
# БАПТАУЛАР
# ==========================================

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Montserrat', sans-serif;
}

.stApp {

    min-height: 100vh;

    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(0, 120, 255, 0.20),
            transparent 30%
        ),

        radial-gradient(
            circle at 85% 80%,
            rgba(0, 210, 255, 0.13),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #020817,
            #06142b,
            #020817
        );

}

header {
    background: transparent !important;
}

.block-container {
    max-width: 1200px !important;
    padding-top: 30px !important;
}


/* ==========================================
   LOGIN
========================================== */

.login-wrapper {

    min-height: 90vh;

    display: flex;

    justify-content: center;

    align-items: center;

}

.login-card {

    width: 430px;

    padding: 45px 40px;

    border-radius: 28px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.11),
            rgba(255,255,255,0.045)
        );

    border: 1px solid rgba(255,255,255,0.15);

    backdrop-filter: blur(25px);

    box-shadow:
        0 30px 90px rgba(0,0,0,0.55);

}

.logo {

    text-align: center;

    font-size: 38px;

    font-weight: 800;

    color: white;

}

.logo span {

    color: #39bfff;

}

.subtitle {

    text-align: center;

    color: rgba(255,255,255,0.50);

    font-size: 12px;

    margin-top: 8px;

    margin-bottom: 25px;

}


/* ==========================================
   INPUT
========================================== */

.stTextInput label {

    color: rgba(255,255,255,0.75) !important;

    font-weight: 600 !important;

}

.stTextInput input {

    background: rgba(255,255,255,0.06) !important;

    border: 1px solid rgba(255,255,255,0.14) !important;

    border-radius: 14px !important;

    color: white !important;

    height: 52px !important;

}


/* ==========================================
   BUTTON
========================================== */

.stButton button {

    border-radius: 14px !important;

    height: 50px !important;

    font-weight: 700 !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #39bfff,
            #1677ff
        ) !important;

    color: white !important;

    transition: 0.25s !important;

}

.stButton button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 10px 30px rgba(22,119,255,0.35);

}


/* ==========================================
   HOME HEADER
========================================== */

.home-header {

    padding: 25px 0 35px 0;

}

.home-logo {

    font-size: 30px;

    font-weight: 800;

    color: white;

}

.home-logo span {

    color: #39bfff;

}

.home-title {

    font-size: 42px;

    font-weight: 800;

    color: white;

    margin-top: 45px;

}

.home-description {

    color: rgba(255,255,255,0.55);

    font-size: 15px;

    margin-top: 8px;

}


/* ==========================================
   SUBJECT CARDS
========================================== */

.subject-card {

    min-height: 190px;

    padding: 28px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.035)
        );

    border: 1px solid rgba(255,255,255,0.12);

    backdrop-filter: blur(20px);

    transition: 0.25s;

}

.subject-card:hover {

    transform: translateY(-5px);

    border-color:
        rgba(57,191,255,0.45);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.30);

}

.subject-icon {

    font-size: 38px;

}

.subject-name {

    color: white;

    font-size: 20px;

    font-weight: 700;

    margin-top: 15px;

}

.subject-info {

    color: rgba(255,255,255,0.45);

    font-size: 12px;

    margin-top: 7px;

}


/* ==========================================
   SECTION
========================================== */

.section-title {

    color: white;

    font-size: 22px;

    font-weight: 700;

    margin-top: 30px;

    margin-bottom: 15px;

}


/* ==========================================
   FOOTER
========================================== */

.footer {

    text-align: center;

    color: rgba(255,255,255,0.25);

    font-size: 11px;

    margin-top: 60px;

}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-wrapper">

        <div class="login-card">

            <div class="logo">
                KASYM<span>•</span>EDU
            </div>

            <div class="subtitle">
                Бүгінгі дайындық — ертеңгі грант
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    left, center, right = st.columns([1, 1.1, 1])

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
    # HEADER
    # --------------------------------------

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown("""
        <div class="home-header">

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
    # TITLE
    # --------------------------------------

    st.markdown("""
    <div class="home-title">
        ҰБТ-ға дайындық
    </div>

    <div class="home-description">
        Біліміңді тексер. Қателеріңді талда.
        Нәтижеңді жақсарт.
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # SECTION
    # --------------------------------------

    st.markdown("""
    <div class="section-title">
        📚 Пәндер
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # SUBJECTS
    # --------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                📐
            </div>

            <div class="subject-name">
                Математика
            </div>

            <div class="subject-info">
                ҰБТ есептері • Тесттер • Талдау
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Математикаға өту →",
            key="math",
            use_container_width=True
        )


    with col2:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                💻
            </div>

            <div class="subject-name">
                Информатика
            </div>

            <div class="subject-info">
                Python • Теория • ҰБТ тесттері
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Информатикаға өту →",
            key="info",
            use_container_width=True
        )


    with col3:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                🇰🇿
            </div>

            <div class="subject-name">
                Қазақстан тарихы
            </div>

            <div class="subject-info">
                Даталар • Оқиғалар • Тесттер
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Тарихқа өту →",
            key="history",
            use_container_width=True
        )


    # --------------------------------------
    # SECOND ROW
    # --------------------------------------

    st.write("")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                📖
            </div>

            <div class="subject-name">
                Оқу сауаттылығы
            </div>

            <div class="subject-info">
                Мәтіндер • Талдау • Тесттер
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Оқу сауаттылығына өту →",
            key="reading",
            use_container_width=True
        )


    with col2:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                🧠
            </div>

            <div class="subject-name">
                Математикалық сауаттылық
            </div>

            <div class="subject-info">
                Логика • Формулалар • Есептер
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Мат. сауатқа өту →",
            key="math_lit",
            use_container_width=True
        )


    with col3:

        st.markdown("""
        <div class="subject-card">

            <div class="subject-icon">
                🎯
            </div>

            <div class="subject-name">
                Менің нәтижелерім
            </div>

            <div class="subject-info">
                Дұрыс жауаптар • Қателер • Прогресс
            </div>

        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Нәтижелерді көру →",
            key="results",
            use_container_width=True
        )


    # --------------------------------------
    # FOOTER
    # --------------------------------------

    st.markdown("""
    <div class="footer">
        © 2026 KASYM EDU • Бүгінгі дайындық — ертеңгі грант
    </div>
    """, unsafe_allow_html=True)
