import streamlit as st

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    min-height: 100vh;

    background:
        linear-gradient(
            rgba(2, 10, 25, 0.78),
            rgba(1, 6, 18, 0.96)
        ),
        radial-gradient(
            circle at 20% 20%,
            rgba(0, 120, 255, 0.25),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 75%,
            rgba(0, 200, 255, 0.15),
            transparent 35%
        ),
        #020817;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

/* =========================
   АРТҚЫ ЖАЗУ
========================= */

.background-title {
    position: fixed;

    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);

    width: 100%;

    text-align: center;

    font-size: clamp(40px, 7vw, 105px);

    font-weight: 800;

    letter-spacing: -3px;

    color: rgba(255, 255, 255, 0.045);

    white-space: nowrap;

    pointer-events: none;

    z-index: 0;
}

/* =========================
   НЕГІЗГІ ОРТАЛЫҚ
========================= */

.login-page {

    min-height: 100vh;

    display: flex;

    justify-content: center;

    align-items: center;

    position: relative;

    z-index: 2;
}

/* =========================
   GLASS CARD
========================= */

.login-card {

    width: 430px;

    padding: 42px 40px 34px 40px;

    border-radius: 28px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.11),
            rgba(255,255,255,0.045)
        );

    border: 1px solid rgba(255,255,255,0.16);

    backdrop-filter: blur(25px);

    -webkit-backdrop-filter: blur(25px);

    box-shadow:

        0 30px 90px rgba(0,0,0,0.55),

        inset 0 1px 0 rgba(255,255,255,0.12);

}

/* =========================
   ЛОГО
========================= */

.logo {

    text-align: center;

    font-size: 38px;

    font-weight: 800;

    color: white;

    letter-spacing: -1px;

    margin-bottom: 7px;
}

.logo span {

    color: #39bfff;

}

/* =========================
   СЛОГАН
========================= */

.subtitle {

    text-align: center;

    color: rgba(255,255,255,0.55);

    font-size: 12px;

    margin-bottom: 28px;

}

/* =========================
   INPUT LABEL
========================= */

.stTextInput label {

    color: rgba(255,255,255,0.78) !important;

    font-size: 13px !important;

    font-weight: 600 !important;

}

/* =========================
   INPUT
========================= */

.stTextInput > div > div > input {

    height: 52px !important;

    background: rgba(255,255,255,0.055) !important;

    border: 1px solid rgba(255,255,255,0.14) !important;

    border-radius: 14px !important;

    color: white !important;

    padding-left: 16px !important;

    font-size: 14px !important;

}

.stTextInput > div > div > input::placeholder {

    color: rgba(255,255,255,0.30) !important;

}

.stTextInput > div > div > input:focus {

    border: 1px solid #39bfff !important;

    box-shadow:
        0 0 0 2px rgba(57,191,255,0.12) !important;

}

/* =========================
   КІРУ БАТЫРМАСЫ
========================= */

.stButton {

    margin-top: 18px;

}

.stButton > button {

    width: 100%;

    height: 54px;

    border-radius: 15px;

    border: none;

    background:
        linear-gradient(
            135deg,
            #39bfff,
            #1677ff
        );

    color: white;

    font-size: 15px;

    font-weight: 700;

    transition: 0.25s;

    box-shadow:
        0 10px 30px rgba(22,119,255,0.28);

}

.stButton > button:hover {

    transform: translateY(-3px);

    box-shadow:
        0 15px 40px rgba(22,119,255,0.45);

}

/* =========================
   FOOTER
========================= */

.footer {

    text-align: center;

    color: rgba(255,255,255,0.25);

    font-size: 10px;

    margin-top: 25px;

}

/* =========================
   SUCCESS / ERROR
========================= */

.stAlert {

    border-radius: 12px !important;

    margin-top: 15px !important;

}

</style>
""", unsafe_allow_html=True)


# =========================
# АРТҚЫ ЖАЗУ
# =========================

st.markdown("""
<div class="background-title">
    Бүгінгі дайындық — ертеңгі грант
</div>
""", unsafe_allow_html=True)


# =========================
# LOGIN БЕТІНІҢ ЖОҒАРҒЫ БӨЛІГІ
# =========================

st.markdown("""
<div class="login-page">

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


# =========================
# INPUT-ТАРДЫ КАРТОЧКАҒА
# ЖАҚЫН ОРНАЛАСТЫРУ
# =========================

left, center, right = st.columns([1, 1.1, 1])

with center:

    login = st.text_input(
        "Логин",
        placeholder="Логиніңізді енгізіңіз",
        key="login"
    )

    password = st.text_input(
        "Құпиясөз",
        type="password",
        placeholder="Құпиясөзіңізді енгізіңіз",
        key="password"
    )

    if st.button("Кіру  →", use_container_width=True):

        if login and password:

            st.success("Кіру сәтті орындалды! 🎉")

        else:

            st.error(
                "Логин мен құпиясөзді енгізіңіз."
            )

    st.markdown("""
    <div class="footer">
        © 2026 KASYM EDU
    </div>
    """, unsafe_allow_html=True)
