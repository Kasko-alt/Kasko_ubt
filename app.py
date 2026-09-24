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
            rgba(3, 12, 28, 0.72),
            rgba(1, 7, 18, 0.94)
        ),
        radial-gradient(
            circle at 20% 20%,
            rgba(0, 120, 255, 0.22),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 70%,
            rgba(0, 210, 255, 0.14),
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

/* Артқы үлкен мәтін */
.background-title {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    width: 100%;

    text-align: center;

    font-size: clamp(45px, 7vw, 110px);
    font-weight: 800;

    color: rgba(255, 255, 255, 0.045);

    letter-spacing: -3px;
    white-space: nowrap;

    pointer-events: none;
    z-index: 0;
}

/* Login орналасуы */
.login-container {
    min-height: 100vh;

    display: flex;
    justify-content: center;
    align-items: center;

    position: relative;
    z-index: 2;
}

/* Login карточкасы */
.login-card {
    width: 430px;

    padding: 42px;

    border-radius: 28px;

    background: rgba(255, 255, 255, 0.075);

    border: 1px solid rgba(255, 255, 255, 0.16);

    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);

    box-shadow:
        0 30px 80px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

/* Логотип */
.logo {
    text-align: center;

    font-size: 40px;
    font-weight: 800;

    color: white;

    margin-bottom: 8px;
}

.logo span {
    color: #39bfff;
}

/* Слоган */
.subtitle {
    text-align: center;

    color: rgba(255, 255, 255, 0.58);

    font-size: 13px;

    margin-bottom: 28px;
}

/* Input */
.stTextInput {
    margin-bottom: 10px;
}

.stTextInput label {
    color: rgba(255, 255, 255, 0.78) !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.07) !important;

    border: 1px solid rgba(255, 255, 255, 0.15) !important;

    border-radius: 14px !important;

    color: white !important;

    height: 52px !important;

    padding-left: 16px !important;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #39bfff !important;

    box-shadow:
        0 0 0 2px rgba(57, 191, 255, 0.12) !important;
}

/* Кіру батырмасы */
.stButton {
    margin-top: 18px;
}

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
    transform: translateY(-3px);

    box-shadow:
        0 15px 40px rgba(22, 119, 255, 0.45);
}

/* Footer */
.footer {
    text-align: center;

    color: rgba(255, 255, 255, 0.32);

    font-size: 11px;

    margin-top: 22px;
}

</style>
""", unsafe_allow_html=True)


# Артқы жазу
st.markdown(
    """
<div class="background-title">
    Бүгінгі дайындық — ертеңгі грант
</div>
""",
    unsafe_allow_html=True
)


# Login контейнері
st.markdown(
    """
<div class="login-container">
    <div class="login-card">
        <div class="logo">
            KASYM<span>•</span>EDU
        </div>

        <div class="subtitle">
            Бүгінгі дайындық — ертеңгі грант
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True
)


# Input орналасуы
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

    if st.button("Кіру  →"):

        if login and password:
            st.success("Кіру сәтті орындалды!")
        else:
            st.error("Логин мен құпиясөзді енгізіңіз.")

    st.markdown(
        """
<div class="footer">
    © 2026 KASYM EDU
</div>
""",
        unsafe_allow_html=True
    )
