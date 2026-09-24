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


# ==========================================
# ПӘН КОМБИНАЦИЯЛАРЫ
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
   COMBINATION PAGE
========================================== */

.combo-title {
    color: white;
    font-size: 48px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
    margin-top: 80px;
}

.combo-title span {
    color: #39bfff;
}

.common-box {
    margin-top: 35px;
    padding: 25px;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}

.common-title {
    color: white;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 18px;
}

.common-item {
    color: rgba(255,255,255,0.70);
    font-size: 14px;
    padding: 8px 0;
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
    # HOME PAGE
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


        # ==================================
        # ПӘНДЕР
        # ==================================

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
            <div class="home-description">
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
                    key=f"subject_{i}_{subject}",
                    use_container_width=True
                ):

                    st.info(
                        f"{subject} тесттері келесі қадамда қосылады."
                    )

            st.divider()


        # ==================================
        # ОРТАҚ МІНДЕТТІ ПӘНДЕР
        # ==================================

        st.markdown(
            """
            <div class="common-box">

                <div class="common-title">
                    📌 Барлық пәндерге ортақ міндетті бөлім
                </div>

                <div class="common-item">
                    🧠 Математикалық сауаттылық
                </div>

                <div class="common-item">
                    📖 Оқу сауаттылығы
                </div>

                <div class="common-item">
                    🇰🇿 Қазақстан тарихы
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")


        # ==================================
        # BACK
        # ==================================

        if st.button("← Пәндерге қайту"):

            st.session_state.page = "home"
            st.session_state.selected_combination = None

            st.rerun()


        st.markdown(
            '<div class="footer">© 2026 KASYM EDU</div>',
            unsafe_allow_html=True
        )
