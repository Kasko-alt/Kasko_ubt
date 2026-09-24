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
    border: none !important;

    background: linear-gradient(
        135deg,
        #39bfff,
        #1677ff
    ) !important;

    color: white !important;

    font-weight: 700 !important;

    transition: 0.2s;
}

.stButton button:hover {
    transform: translateY(-2px);
}


/* ==========================================
   HOME
========================================== */

.home-logo {
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.home-logo span {
    color: #39bfff;
}

.home-title {
    color: white;
    font-size: 58px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -3px;
    margin-top: 100px;
}

.home-description {
    color: rgba(255,255,255,0.48);
    font-size: 15px;
    margin-top: 20px;
    line-height: 1.6;
}


/* ==========================================
   SECTION TITLE
========================================== */

.section-title {
    color: white;
    font-size: 26px;
    font-weight: 700;
    margin-top: 70px;
    margin-bottom: 25px;
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
   COMMON SECTION
========================================== */

.common-title {
    color: rgba(255,255,255,0.60);
    font-size: 14px;
    font-weight: 600;
    margin-top: 55px;
    margin-bottom: 20px;
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


# ==========================================
# HOME
# ==========================================

else:

    # --------------------------------------
    # HEADER
    # --------------------------------------

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
    # HOME PAGE
    # ======================================

    if st.session_state.page == "home":

        st.markdown(
            """
            <div class="home-title">
                Бүгінгі дайындық —<br>
                ертеңгі грант.
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


        # ==================================
        # НЕГІЗГІ ПӘНДЕР
        # ==================================

        st.markdown(
            '<div class="section-title">Негізгі пәндер</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------
        # ИНФОРМАТИКА + МАТЕМАТИКА
        # ----------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write("01")

            st.subheader(
                "💻 Информатика  +  📐 Математика"
            )

            st.caption(
                "Информатика • Математика • ҰБТ тесттері"
            )

        with col2:

            if st.button(
                "→",
                key="main_subjects",
                use_container_width=True
            ):

                st.session_state.page = "main_subjects"

        st.divider()


        # ==================================
        # ОРТАҚ МІНДЕТТІ ПӘНДЕР
        # ==================================

        st.markdown(
            '<div class="common-title">Барлық негізгі пәндерге ортақ</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------
        # МАТЕМАТИКАЛЫҚ САУАТТЫЛЫҚ
        # ----------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write("02")

            st.subheader(
                "🧠 Математикалық сауаттылық"
            )

            st.caption(
                "Логика • Формулалар • Есептер"
            )

        with col2:

            st.button(
                "→",
                key="math_lit"
            )

        st.divider()


        # ----------------------------------
        # ОҚУ САУАТТЫЛЫҒЫ
        # ----------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write("03")

            st.subheader(
                "📖 Оқу сауаттылығы"
            )

            st.caption(
                "Мәтіндер • Талдау • Тесттер"
            )

        with col2:

            st.button(
                "→",
                key="reading"
            )

        st.divider()


        # ----------------------------------
        # ҚАЗАҚСТАН ТАРИХЫ
        # ----------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write("04")

            st.subheader(
                "🇰🇿 Қазақстан тарихы"
            )

            st.caption(
                "Даталар • Оқиғалар • Тесттер"
            )

        with col2:

            st.button(
                "→",
                key="history"
            )


        # ==================================
        # НӘТИЖЕЛЕР
        # ==================================

        st.markdown(
            '<div class="section-title">Нәтижелер</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write("05")

            st.subheader(
                "🎯 Менің нәтижелерім"
            )

            st.caption(
                "Дұрыс жауаптар • Қате сұрақтар • Прогресс"
            )

        with col2:

            st.button(
                "→",
                key="results"
            )


        st.markdown(
            '<div class="footer">© 2026 KASYM EDU</div>',
            unsafe_allow_html=True
        )


    # ======================================
    # MAIN SUBJECTS PAGE
    # ======================================

    elif st.session_state.page == "main_subjects":

        st.markdown(
            """
            <div class="home-title">
                Информатика<br>
                <span>+ Математика</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="home-description">
                Негізгі пәндер бойынша ҰБТ дайындығы.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("💻 Информатика")

            st.caption(
                "Python • Алгоритмдер • Ақпараттық технологиялар"
            )

            if st.button(
                "Информатиканы бастау →",
                key="start_info",
                use_container_width=True
            ):
                st.info("Информатика тесттері келесі қадамда қосылады.")


        with col2:

            st.subheader("📐 Математика")

            st.caption(
                "Алгебра • Геометрия • ҰБТ есептері"
            )

            if st.button(
                "Математиканы бастау →",
                key="start_math",
                use_container_width=True
            ):
                st.info("Математика тесттері келесі қадамда қосылады.")


        st.write("")

        if st.button("← Артқа"):

            st.session_state.page = "home"

            st.rerun()
