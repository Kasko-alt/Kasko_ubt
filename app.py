import streamlit as st

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Бүгінгі дайындық — ертеңгі грант",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Montserrat', sans-serif;
}

html, body, [class*="css"] {
    margin: 0;
    padding: 0;
}

.stApp {
    min-height: 100vh;

    background:
        linear-gradient(
            rgba(4, 13, 30, 0.72),
            rgba(2, 8, 20, 0.88)
        ),
        radial-gradient(
            circle at 20% 20%,
            rgba(0, 120, 255, 0.25),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 70%,
            rgba(0, 210, 255, 0.15),
            transparent 35%
        ),
        #020817;
}

/* Streamlit header */
header {
    background: transparent !important;
}

/* Main container */
.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

/* Background slogan */
.background-title {
    position: fixed;
    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);

    width: 100%;

    text-align: center;

    font-size: clamp(45px, 7vw, 110px);
    font-weight: 800;

    color: rgba(255, 255, 255, 0.055);

    letter-spacing: -3px;

    pointer-events: none;

    white-space: nowrap;

    z-index: 0;
}

/* Login wrapper */
.login-wrapper {
    min-height: 100vh;

    display: flex;
    justify-content: center;
    align-items: center;

    position: relative;

    z-index: 2;
}

/* Login card */
.login-card {
    width: 430px;

    padding: 45px 42px;

    border-radius: 28px;

    background: rgba(255, 255, 255, 0.08);

    border: 1px solid rgba(255, 255, 255, 0.16);

    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    box-shadow:
        0 30px 80px rgba(0, 0, 0, 0.45),
        inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

/* Logo */
.logo {
    text-align: center;

    font-size: 42px;
    font-weight: 800;

    color: white;

    margin-bottom: 8px;
}

.logo span {
    color: #39bfff;
}

/* Subtitle */
.subtitle {
    text-align: center;

    color: rgba(255, 255, 255, 0.62);

    font-size: 14px;

    margin-bottom: 32px;
}

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.07) !important;

    border: 1px solid rgba(255, 255, 255, 0.15) !important;

    border-radius: 14px !important;

    color: white !important;

    height: 52px !important;

    padding-left: 16px !important;
}

.stTextInput > div > div > input:focus {
    border: 1px solid rgba(57, 191, 255, 0.8) !important;

    box-shadow:
        0 0 0 2px rgba(57, 191, 255, 0.12) !important;
}

/* Input labels */
.stTextInput label {
    color: rgba(255, 255, 255, 0.75) !important;

    font-weight: 500 !important;
}

/* Login button */
.stButton > button {
    width: 100%;

    height: 54px;

    border-radius: 15px;

    border: none;

    background: linear-gradient(
        135deg,
        #39bfff,
        #1677ff
    );

    color: white;

    font-size: 16px;

    font-weight: 700;

    transition: all 0.25s ease;

    box-shadow:
        0 10px 30px rgba(22, 119, 255, 0.28);
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 15px 35px rgba(22, 119, 255, 0.45);
}

/* Footer */
.footer {
    text-align: center;

    color: rgba(255, 255, 255, 0.35);

    font-size: 11px;

    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# LOGIN PAGE
# =========================

st.markdown("""
<div class="background-title">
    Бүгінгі дайындық — ертеңгі грант
</div>
""", unsafe_allow_html=True)


# Center columns
left, center, right = st.columns([1, 1.1, 1])


with center:

    st.markdown("""
    <div class="login-card">

        <div class="logo">
            KASYM<span>•</span>EDU
        </div>

        <div class="subtitle">
            Бүгінгі дайындық — ертеңгі грант
        </div>

    </div>
    """, unsafe_allow_html=True)

    login = st.text_input(
        "Логин",
        placeholder="Логиніңізді енгізіңіз"
    )

    password = st.text_input(
        "Құпиясөз",
        type="password",
        placeholder="Құпиясөзіңізді енгізіңіз"
    )

    st.write("")

    if st.button("Кіру  →"):

        if login and password:
            st.success("Кіру сәтті орындалды!")
        else:
            st.error("Логин мен құпиясөзді енгізіңіз.")

    st.markdown("""
    <div class="footer">
        © 2026 KASYM EDU
    </div>
    """, unsafe_allow_html=True)
