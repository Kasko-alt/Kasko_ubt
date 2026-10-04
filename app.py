import datetime
import hashlib
import json
import os
import random
import re

import pandas as pd
import streamlit as st


# =========================================================
# KASYM EDU
# =========================================================

st.set_page_config(
    page_title="KASYM EDU - Білім беру платформасы",
    page_icon="🎓",
    layout="wide",
)


# =========================================================
# FILES
# =========================================================

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"
TEST_PROGRESS_FILE = "test_progress.json"

ADMIN_USERNAME = "kas01"
ADMIN_PASSWORD = os.environ.get(
    "KASYM_ADMIN_PASSWORD",
    "CHANGE_ME"
)


# =========================================================
# SUBJECTS
# =========================================================

all_subjects = [
    "Биология",
    "Химия",
    "Физика",
    "Математика",
    "Информатика",
    "Дүниежүзі тарихы",
    "Ағылшын тілі",
    "География",
    "Құқық",
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық",
]


# =========================================================
# QUESTION LIMITS
# =========================================================

QUESTION_LIMITS = {
    "Қазақстан тарихы": 20,
    "Оқу сауаттылығы": 10,
    "Математикалық сауаттылық": 10,

    "Биология": 40,
    "Химия": 40,
    "Физика": 40,
    "Математика": 40,
    "Информатика": 40,
    "Дүниежүзі тарихы": 40,
    "Ағылшын тілі": 40,
    "География": 40,
    "Құқық": 40,
}


# =========================================================
# POINT LIMITS
# =========================================================

POINT_LIMITS = {
    "Қазақстан тарихы": 20,
    "Оқу сауаттылығы": 10,
    "Математикалық сауаттылығы": 10,

    "Биология": 50,
    "Химия": 50,
    "Физика": 50,
    "Математика": 50,
    "Информатика": 50,
    "Дүниежүзі тарихы": 50,
    "Ағылшын тілі": 50,
    "География": 50,
    "Құқық": 50,
}

# Correct key for math literacy
POINT_LIMITS["Математикалық сауаттылығы"] = 10
POINT_LIMITS["Математикалық сауаттылық"] = 10


# =========================================================
# COMBINATIONS
# =========================================================

combinations = {
    "Математика - Физика (Инженерлік)": {
        "pair": ["Математика", "Физика"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },

    "Биология - Химия (Медицина)": {
        "pair": ["Биология", "Химия"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },

    "География - Математика (Геодезия/Экономика)": {
        "pair": ["География", "Математика"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },

    "Дүниежүзі тарихы - Ағылшын (Халықаралық)": {
        "pair": ["Дүниежүзі тарихы", "Ағылшын тілі"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },

    "Математика - Информатика (IT / Бағдарламалау)": {
        "pair": ["Математика", "Информатика"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },

    "Құқық - Дүниежүзі тарихы (Юриспруденция)": {
        "pair": ["Құқық", "Дүниежүзі тарихы"],
        "common": [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ],
    },
}


# =========================================================
# DEFAULT QUESTIONS
# =========================================================

default_questions = {
    "Қазақстан тарихы": [
        {
            "question": "Қазақстан Республикасының тәуелсіздігі қашан жарияланды?",
            "options": [
                "1990 жылғы 25 қазан",
                "1991 жылғы 16 желтоқсан",
                "1991 жылғы 1 желтоқсан",
                "1992 жылғы 4 маусым",
            ],
            "answer": 1,
        },
        {
            "question": "Қазақстан Республикасының мемлекеттік рәміздері қашан бекітілді?",
            "options": [
                "1991 жылы",
                "1992 жылы",
                "1993 жылы",
                "1995 жылы",
            ],
            "answer": 1,
        },
    ],

    "Биология": [
        {
            "question": "Жасушаның тұқым қуалайтын ақпаратын сақтайтын негізгі құрылым?",
            "options": [
                "Рибосома",
                "Ядро",
                "Лизосома",
                "Митохондрия",
            ],
            "answer": 1,
        }
    ],
}


# =========================================================
# PASSWORD
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# USERS
# =========================================================

def default_users():
    return [
        {
            "username": ADMIN_USERNAME,
            "password": hash_password(ADMIN_PASSWORD),
            "name": "KASYM",
            "role": "admin",
            "combination": None,
        }
    ]


def save_users(users_list):
    try:
        with open(
            USERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                users_list,
                file,
                ensure_ascii=False,
                indent=4
            )
    except Exception as error:
        st.error(
            f"Қолданушыларды сақтау кезінде қате: {error}"
        )


def load_users():

    if os.path.exists(USERS_FILE):

        try:

            with open(
                USERS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list) and data:

                admin_found = False

                for user in data:

                    if user.get("username") == ADMIN_USERNAME:

                        user["role"] = "admin"

                        admin_found = True

                if admin_found:
                    return data

                data.append(
                    {
                        "username": ADMIN_USERNAME,
                        "password": hash_password(
                            ADMIN_PASSWORD
                        ),
                        "name": "KASYM",
                        "role": "admin",
                        "combination": None,
                    }
                )

                save_users(data)

                return data

        except Exception:
            pass

    data = default_users()

    save_users(data)

    return data


users = load_users()


def find_user(username, password):

    username = (username or "").strip()
    password = password or ""

    if not username or not password:
        return None

    hashed_input = hash_password(password)

    for user in users:

        if user.get("username") != username:
            continue

        stored_password = str(
            user.get("password", "")
        ).strip()

        if stored_password == hashed_input:
            return user

        # Compatibility with old plain-text users
        if stored_password == password:
            return user

    return None


# =========================================================
# QUESTIONS
# =========================================================

def save_questions(data):

    try:

        with open(
            QUESTIONS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as error:

        st.error(
            f"Сұрақтарды сақтау кезінде қате: {error}"
        )


def load_questions():

    if os.path.exists(QUESTIONS_FILE):

        try:

            with open(
                QUESTIONS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

    data = default_questions.copy()

    save_questions(data)

    return data


questions = load_questions()


# =========================================================
# RESULTS
# =========================================================

def load_results():

    if os.path.exists(RESULTS_FILE):

        try:

            with open(
                RESULTS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):
                return data

        except Exception:
            pass

    return []


def save_results(data):

    try:

        with open(
            RESULTS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as error:

        st.error(
            f"Нәтижені сақтау кезінде қате: {error}"
        )


results_history = load_results()


# =========================================================
# TEST PROGRESS
# =========================================================

def load_test_progress():

    if os.path.exists(TEST_PROGRESS_FILE):

        try:

            with open(
                TEST_PROGRESS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

    return {}


def save_test_progress():

    try:

        if not st.session_state.get("test_started"):
            return

        data = {
            "username": st.session_state.get(
                "username"
            ),

            "full_name": st.session_state.get(
                "full_name"
            ),

            "active_combination": st.session_state.get(
                "active_combination"
            ),

            "current_subject_idx": st.session_state.get(
                "current_subject_idx",
                0
            ),

            "current_question_idx": st.session_state.get(
                "current_question_idx",
                0
            ),

            "test_answers": st.session_state.get(
                "test_answers",
                {}
            ),

            "test_data": st.session_state.get(
                "test_data",
                {}
            ),

            "started_at": st.session_state.get(
                "started_at"
            ),
        }

        with open(
            TEST_PROGRESS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception:
        pass


def clear_test_progress():

    try:

        if os.path.exists(TEST_PROGRESS_FILE):
            os.remove(TEST_PROGRESS_FILE)

    except Exception:
        pass


# =========================================================
# SESSION DEFAULTS
# =========================================================

session_defaults = {

    "logged_in": False,

    "role": None,

    "username": None,

    "full_name": None,

    "page": "home",

    "test_started": False,

    "active_combination": None,

    "current_subject_idx": 0,

    "current_question_idx": 0,

    "test_answers": {},

    "test_data": {},

    "started_at": None,

    "saved_result_id": None,

    "pending_delete_question": None,

    "pending_user_delete": None,

    "retry_mode": False,

    "retry_questions": {},

    "retry_answers": {},

    "retry_subject_idx": 0,

    "retry_question_idx": 0,
}


for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# PREMIUM DARK BLUE CSS
# =========================================================

st.markdown(
    """
<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(37, 99, 235, 0.16),
            transparent 28%
        ),

        radial-gradient(
            circle at 90% 10%,
            rgba(124, 58, 237, 0.12),
            transparent 25%
        ),

        #070A12;

    color: #F8FAFC;
}


.block-container {

    max-width: 1450px;

    padding-top: 2rem;

    padding-bottom: 4rem;
}


/* ===================================================== */
/* TEXT */
/* ===================================================== */

h1,
h2,
h3,
h4,
h5,
h6 {

    color: #F8FAFC !important;
}


p,
span,
label {

    color: #CBD5E1;
}


.kasym-title {

    font-size: 46px;

    font-weight: 900;

    letter-spacing: -1.5px;

    color: #F8FAFC;
}


.kasym-subtitle {

    font-size: 16px;

    color: #94A3B8;

    margin-top: -5px;
}


/* ===================================================== */
/* HERO */
/* ===================================================== */

.hero {

    position: relative;

    overflow: hidden;

    padding: 34px;

    border-radius: 26px;

    background:

        radial-gradient(
            circle at 85% 20%,
            rgba(56,189,248,0.18),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            rgba(37,99,235,0.28),
            rgba(15,23,42,0.94)
        );

    border: 1px solid rgba(
        96,
        165,
        250,
        0.20
    );

    box-shadow:

        0 25px 80px rgba(0,0,0,0.35),

        inset 0 1px 0 rgba(
            255,
            255,
            255,
            0.04
        );

    margin: 20px 0 25px 0;
}


.hero::after {

    content: "";

    position: absolute;

    width: 220px;

    height: 220px;

    right: -80px;

    top: -100px;

    background: rgba(
        37,
        99,
        235,
        0.20
    );

    filter: blur(60px);

    border-radius: 50%;
}


.hero h2 {

    font-size: 28px;

    font-weight: 850;

    margin-bottom: 10px;
}


.hero p {

    color: #A8B4C7;
}


/* ===================================================== */
/* CARDS */
/* ===================================================== */

.card {

    background:

        linear-gradient(
            145deg,
            rgba(17,24,39,0.92),
            rgba(10,15,27,0.92)
        );

    border: 1px solid rgba(
        148,
        163,
        184,
        0.10
    );

    border-radius: 20px;

    padding: 23px;

    margin-bottom: 18px;

    box-shadow:

        0 12px 40px rgba(
            0,
            0,
            0,
            0.22
        ),

        inset 0 1px 0 rgba(
            255,
            255,
            255,
            0.025
        );

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}


.card:hover {

    transform: translateY(-3px);

    border-color:
        rgba(59,130,246,0.30);

    box-shadow:

        0 18px 45px rgba(
            0,
            0,
            0,
            0.32
        ),

        0 0 25px rgba(
            37,
            99,
            235,
            0.07
        );
}


/* ===================================================== */
/* METRIC */
/* ===================================================== */

.metric-box {

    position: relative;

    background:

        linear-gradient(
            145deg,
            rgba(17,24,39,0.95),
            rgba(11,16,28,0.95)
        );

    border: 1px solid rgba(
        148,
        163,
        184,
        0.10
    );

    border-radius: 20px;

    padding: 24px;

    text-align: center;

    min-height: 120px;

    box-shadow:
        0 10px 35px rgba(
            0,
            0,
            0,
            0.20
        );
}


.metric-number {

    font-size: 32px;

    font-weight: 900;

    color: #F8FAFC;
}


.metric-label {

    margin-top: 6px;

    color: #64748B;

    font-size: 13px;

    font-weight: 600;
}


/* ===================================================== */
/* QUESTION */
/* ===================================================== */

.question-box {

    background:

        linear-gradient(
            145deg,
            rgba(17,24,39,0.97),
            rgba(9,14,25,0.97)
        );

    border: 1px solid rgba(
        96,
        165,
        250,
        0.14
    );

    border-radius: 24px;

    padding: 30px;

    margin: 20px 0;

    box-shadow:
        0 20px 60px rgba(
            0,
            0,
            0,
            0.30
        );
}


.question-text {

    font-size: 21px;

    font-weight: 750;

    line-height: 1.6;

    color: #F8FAFC;
}


/* ===================================================== */
/* ANSWER STATES */
/* ===================================================== */

.correct-box {

    background:

        linear-gradient(
            135deg,
            rgba(34,197,94,0.12),
            rgba(15,23,42,0.80)
        );

    border: 1px solid rgba(
        34,
        197,
        94,
        0.30
    );

    border-radius: 16px;

    padding: 17px;

    margin-top: 12px;
}


.wrong-box {

    background:

        linear-gradient(
            135deg,
            rgba(239,68,68,0.12),
            rgba(15,23,42,0.80)
        );

    border: 1px solid rgba(
        239,
        68,
        68,
        0.30
    );

    border-radius: 16px;

    padding: 17px;

    margin-top: 12px;
}


.unanswered-box {

    background:

        linear-gradient(
            135deg,
            rgba(100,116,139,0.10),
            rgba(15,23,42,0.80)
        );

    border: 1px solid rgba(
        148,
        163,
        184,
        0.18
    );

    border-radius: 16px;

    padding: 17px;

    margin-top: 12px;
}


/* ===================================================== */
/* RESUME */
/* ===================================================== */

.resume-card {

    background:

        radial-gradient(
            circle at 100% 0%,
            rgba(34,197,94,0.13),
            transparent 35%
        ),

        linear-gradient(
            145deg,
            rgba(17,24,39,0.96),
            rgba(8,15,25,0.96)
        );

    border: 1px solid rgba(
        34,
        197,
        94,
        0.25
    );

    border-radius: 22px;

    padding: 25px;

    margin: 22px 0;
}


/* ===================================================== */
/* INFO */
/* ===================================================== */

.info-box {

    padding: 18px;

    border-radius: 16px;

    background:
        rgba(37,99,235,0.10);

    border: 1px solid rgba(
        59,
        130,
        246,
        0.22
    );

    margin-bottom: 15px;
}


.warning-box {

    padding: 18px;

    border-radius: 16px;

    background:
        rgba(245,158,11,0.10);

    border: 1px solid rgba(
        245,
        158,
        11,
        0.25
    );

    margin-bottom: 15px;
}


/* ===================================================== */
/* BUTTONS */
/* ===================================================== */

[data-testid="stButton"] button {

    min-height: 46px;

    border-radius: 13px;

    font-weight: 750;

    border: 1px solid rgba(
        148,
        163,
        184,
        0.12
    );

    background:

        linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );

    color: #E2E8F0;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}


[data-testid="stButton"] button:hover {

    transform: translateY(-2px);

    border-color:
        rgba(59,130,246,0.40);

    box-shadow:
        0 8px 25px rgba(
            37,
            99,
            235,
            0.15
        );
}


/* PRIMARY */

[data-testid="stButton"] button[kind="primary"] {

    background:

        linear-gradient(
            135deg,
            #2563EB,
            #1D4ED8
        );

    color: white;

    border: none;

    box-shadow:
        0 8px 28px rgba(
            37,
            99,
            235,
            0.28
        );
}


[data-testid="stButton"] button[kind="primary"]:hover {

    background:

        linear-gradient(
            135deg,
            #3B82F6,
            #2563EB
        );

    box-shadow:
        0 10px 35px rgba(
            37,
            99,
            235,
            0.40
        );
}


/* ===================================================== */
/* INPUTS */
/* ===================================================== */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {

    background: #0F172A !important;

    border: 1px solid #1E293B !important;

    color: #F8FAFC !important;

    border-radius: 13px !important;
}


[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {

    border-color: #3B82F6 !important;

    box-shadow:
        0 0 0 1px #3B82F6,
        0 0 18px rgba(
            37,
            99,
            235,
            0.14
        ) !important;
}


/* ===================================================== */
/* RADIO */
/* ===================================================== */

.stRadio > div {

    gap: 10px;
}


.stRadio label {

    padding: 12px 15px;

    border-radius: 13px;

    background:
        rgba(15,23,42,0.70);

    border: 1px solid rgba(
        148,
        163,
        184,
        0.08
    );

    transition: all 0.18s ease;
}


.stRadio label:hover {

    background:
        rgba(30,41,59,0.90);

    border-color:
        rgba(59,130,246,0.30);
}


/* ===================================================== */
/* TABS */
/* ===================================================== */

.stTabs [data-baseweb="tab-list"] {

    gap: 8px;

    background: transparent;
}


.stTabs [data-baseweb="tab"] {

    background:
        rgba(15,23,42,0.70);

    border-radius: 12px;

    padding: 10px 18px;

    color: #94A3B8;
}


.stTabs [aria-selected="true"] {

    background:
        rgba(37,99,235,0.16);

    color: #60A5FA !important;

    border-bottom:
        2px solid #3B82F6;
}


/* ===================================================== */
/* EXPANDER */
/* ===================================================== */

[data-testid="stExpander"] {

    background:
        rgba(15,23,42,0.65);

    border: 1px solid rgba(
        148,
        163,
        184,
        0.10
    );

    border-radius: 16px;
}


/* ===================================================== */
/* LOGIN */
/* ===================================================== */

.login-container {

    max-width: 470px;

    margin: 7vh auto 0 auto;
}


.login-card {

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(37,99,235,0.14),
            transparent 40%
        ),

        linear-gradient(
            145deg,
            rgba(17,24,39,0.98),
            rgba(7,11,20,0.98)
        );

    border: 1px solid rgba(
        96,
        165,
        250,
        0.16
    );

    border-radius: 28px;

    padding: 38px;

    box-shadow:

        0 30px 100px rgba(
            0,
            0,
            0,
            0.55
        ),

        0 0 50px rgba(
            37,
            99,
            235,
            0.05
        );
}


/* ===================================================== */
/* SCORE */
/* ===================================================== */

.score-big {

    font-size: 68px;

    font-weight: 950;

    line-height: 1;

    letter-spacing: -3px;

    background:

        linear-gradient(
            135deg,
            #FFFFFF,
            #60A5FA
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* ===================================================== */
/* DIVIDER */
/* ===================================================== */

hr {

    border-color:
        rgba(
            148,
            163,
            184,
            0.10
        ) !important;
}


/* ===================================================== */
/* MOBILE */
/* ===================================================== */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem;
    }

    .kasym-title {
        font-size: 32px;
    }

    .kasym-subtitle {
        font-size: 14px;
    }

    .hero {
        padding: 22px;
        border-radius: 20px;
    }

    .card {
        padding: 18px;
        border-radius: 17px;
    }

    .question-box {
        padding: 20px;
        border-radius: 18px;
    }

    .question-text {
        font-size: 18px;
    }

    .metric-box {
        padding: 17px;
        min-height: 95px;
    }

    .metric-number {
        font-size: 25px;
    }

    .score-big {
        font-size: 48px;
    }

    .login-container {
        margin-top: 3vh;
    }

    .login-card {
        padding: 24px;
        border-radius: 22px;
    }
}


@media (max-width: 480px) {

    .kasym-title {
        font-size: 27px;
    }

    .metric-number {
        font-size: 22px;
    }

    .score-big {
        font-size: 42px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# LOGOUT
# =========================================================

def logout():

    if st.session_state.get("test_started"):
        save_test_progress()

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.page = "home"

    st.session_state.test_started = False
    st.session_state.active_combination = None
    st.session_state.test_answers = {}
    st.session_state.test_data = {}
    st.session_state.current_subject_idx = 0
    st.session_state.current_question_idx = 0

    st.session_state.pending_delete_question = None
    st.session_state.pending_user_delete = None

    st.session_state.retry_mode = False
    st.session_state.retry_questions = {}
    st.session_state.retry_answers = {}

    st.session_state.saved_result_id = None

    st.rerun()


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="login-container">

            <div class="login-card">

                <div style="
                    text-align:center;
                    margin-bottom:25px;
                ">

                    <div style="
                        width:80px;
                        height:80px;
                        margin:auto;
                        border-radius:24px;

                        display:flex;
                        align-items:center;
                        justify-content:center;

                        background:
                            linear-gradient(
                                135deg,
                                #2563EB,
                                #7C3AED
                            );

                        box-shadow:
                            0 15px 40px
                            rgba(
                                37,
                                99,
                                235,
                                0.30
                            );

                        font-size:40px;
                    ">
                        🎓
                    </div>

                    <div class="kasym-title"
                         style="
                            font-size:38px;
                            margin-top:18px;
                         ">
                        KASYM EDU
                    </div>

                    <div class="kasym-subtitle">
                        Бүгінгі дайындық — ертеңгі грант
                    </div>

                </div>
        """,
        unsafe_allow_html=True,
    )

    username = st.text_input(
        "Логин",
        placeholder="Логиніңізді енгізіңіз",
        key="login_username",
    )

    password = st.text_input(
        "Құпиясөз",
        type="password",
        placeholder="Құпиясөзіңізді енгізіңіз",
        key="login_password",
    )

    if st.button(
        "🚀 Кіру",
        use_container_width=True,
        type="primary",
    ):

        user = find_user(
            username,
            password,
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.username = user.get(
                "username"
            )

            st.session_state.full_name = user.get(
                "name",
                user.get("username")
            )

            st.session_state.role = user.get(
                "role",
                "user"
            )

            st.session_state.page = "home"

            st.session_state.login_username = ""
            st.session_state.login_password = ""

            st.rerun()

        else:

            st.error(
                "❌ Логин немесе құпиясөз дұрыс емес."
            )

    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# STATISTICS
# =========================================================

def user_results(username):

    return [
        result
        for result in results_history
        if result.get("username") == username
    ]


def calculate_user_statistics(username):

    history = user_results(username)

    if not history:

        return {
            "attempts": 0,
            "best": 0,
            "average": 0,
        }

    scores = [
        float(
            result.get(
                "total_score",
                0
            )
        )
        for result in history
    ]

    return {
        "attempts": len(scores),
        "best": max(scores),
        "average": round(
            sum(scores) / len(scores),
            1
        ),
    }


# =========================================================
# ANALYTICS
# =========================================================

def analytics_page(username):

    history = user_results(username)

    st.markdown(
        "## 📊 Менің аналитикам"
    )

    if not history:

        st.markdown(
            """
            <div class="card"
                 style="text-align:center;padding:40px;">

                <div style="
                    font-size:45px;
                    margin-bottom:10px;
                ">
                    📊
                </div>

                <h3>
                    Әзірге нәтиже жоқ
                </h3>

                <p>
                    Бірінші тестіңді орындағаннан кейін
                    аналитика осы жерде пайда болады.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    scores = [
        float(
            item.get(
                "total_score",
                0
            )
        )
        for item in history
    ]

    best = max(scores)

    average = round(
        sum(scores) / len(scores),
        1
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-number">
                    {len(scores)}
                </div>

                <div class="metric-label">
                    Тест саны
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-number">
                    {best:.0f}
                    <span style="
                        font-size:14px;
                        color:#64748B;
                    ">
                        / 140
                    </span>
                </div>

                <div class="metric-label">
                    Ең жоғары балл
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-number">
                    {average:.1f}
                </div>

                <div class="metric-label">
                    Орташа балл
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "### 📈 Тест тарихы"
    )

    rows = []

    for index, result in enumerate(
        reversed(history),
        start=1
    ):

        rows.append(
            {
                "№": index,
                "Күні": result.get(
                    "date",
                    "-"
                ),
                "Бағыт": result.get(
                    "combination",
                    "-"
                ),
                "Балл": result.get(
                    "total_score",
                    0
                ),
                "Пайыз": result.get(
                    "percentage",
                    0
                ),
            }
        )

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# BULK QUESTION PARSER
# =========================================================

def parse_bulk_questions(text):

    questions_result = []

    if not text or not text.strip():
        return questions_result

    blocks = re.split(
        r"\n\s*\n",
        text.strip()
    )

    for block in blocks:

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if len(lines) < 5:
            continue

        question_text = lines[0]

        options = []

        correct_index = None

        for line in lines[1:]:

            match = re.match(
                r"^[A-DА-Г]\s*[\.\)\:\-]?\s*(.*)$",
                line,
                re.IGNORECASE,
            )

            if not match:
                continue

            option_text = match.group(1).strip()

            is_correct = False

            if option_text.startswith("*"):

                is_correct = True

                option_text = (
                    option_text[1:].strip()
                )

            if option_text.startswith("(+)"):

                is_correct = True

                option_text = (
                    option_text[3:].strip()
                )

            if "Дұрыс" in option_text:

                is_correct = True

                option_text = (
                    option_text
                    .replace(
                        "Дұрыс",
                        ""
                    )
                    .strip()
                )

            options.append(
                option_text
            )

            if is_correct:

                correct_index = (
                    len(options) - 1
                )

        if len(options) == 4:

            if correct_index is None:
                correct_index = 0

            questions_result.append(
                {
                    "question": question_text,
                    "options": options,
                    "answer": correct_index,
                }
            )

    return questions_result


# =========================================================
# EXCEL QUESTION PARSER
# =========================================================

def parse_excel_questions(uploaded_file):

    try:

        df = pd.read_excel(
            uploaded_file
        )

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        possible_question_columns = [
            "question",
            "Question",
            "Сұрақ",
            "сұрақ",
            "Вопрос",
            "вопрос",
        ]

        question_column = None

        for column in possible_question_columns:

            if column in df.columns:

                question_column = column

                break

        if question_column is None:

            question_column = df.columns[0]

        option_columns = []

        for name in [
            "A",
            "B",
            "C",
            "D",
            "А",
            "Б",
            "В",
            "Г",
        ]:

            if name in df.columns:

                option_columns.append(name)

        if len(option_columns) < 4:

            if len(df.columns) >= 5:

                option_columns = list(
                    df.columns[1:5]
                )

        if len(option_columns) < 4:

            return []

        result = []

        for _, row in df.iterrows():

            question_text = str(
                row[question_column]
            ).strip()

            if (
                not question_text
                or question_text == "nan"
            ):
                continue

            options = []

            for column in option_columns[:4]:

                value = row[column]

                if pd.isna(value):
                    value = ""

                options.append(
                    str(value).strip()
                )

            correct_index = 0

            if "Дұрыс жауап" in df.columns:

                correct = str(
                    row["Дұрыс жауап"]
                ).strip()

                if correct.upper() in [
                    "A",
                    "А",
                ]:

                    correct_index = 0

                elif correct.upper() in [
                    "B",
                    "Б",
                ]:

                    correct_index = 1

                elif correct.upper() in [
                    "C",
                    "В",
                ]:

                    correct_index = 2

                elif correct.upper() in [
                    "D",
                    "Г",
                ]:

                    correct_index = 3

                elif correct.isdigit():

                    number = int(correct)

                    if 1 <= number <= 4:

                        correct_index = (
                            number - 1
                        )

            result.append(
                {
                    "question": question_text,
                    "options": options,
                    "answer": correct_index,
                }
            )

        return result

    except Exception as error:

        st.error(
            f"Excel оқу кезінде қате: {error}"
        )

        return []


# =========================================================
# MODERATOR PAGE
# =========================================================

def moderator_page():

    if (
        not st.session_state.logged_in
        or st.session_state.role != "moderator"
    ):

        st.error(
            "Бұл бөлімге кіруге рұқсат жоқ."
        )

        return

    top1, top2 = st.columns([7, 1])

    with top1:

        st.markdown(
            """
            <div class="kasym-title"
                 style="font-size:36px;">
                KASYM EDU
            </div>

            <div class="kasym-subtitle">
                🧑‍💼 Модератор жұмыс кеңістігі
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top2:

        if st.button(
            "↪ Шығу",
            use_container_width=True,
        ):

            logout()

    tabs = st.tabs(
        [
            "➕ Сұрақ қосу",
            "📥 Excel",
            "🗑️ Сұрақтарды басқару",
        ]
    )

    # =====================================================
    # ADD
    # =====================================================

    with tabs[0]:

        st.markdown(
            "### ➕ Сұрақтар қосу"
        )

        subject = st.selectbox(
            "Пән",
            all_subjects,
            key="moderator_subject_add",
        )

        st.markdown(
            """
            <div class="info-box">

            <b>Формат:</b><br><br>

            1. Сұрақ мәтіні<br>
            A. Жауап<br>
            B. Жауап<br>
            C. *Дұрыс жауап<br>
            D. Жауап<br><br>

            Әр сұрақтың арасында бос жол қалдырыңыз.

            </div>
            """,
            unsafe_allow_html=True,
        )

        bulk_text = st.text_area(
            "Сұрақтарды енгізіңіз",
            height=350,
            key="bulk_questions",
        )

        if st.button(
            "➕ Сұрақтарды қосу",
            type="primary",
        ):

            parsed = parse_bulk_questions(
                bulk_text
            )

            if not parsed:

                st.warning(
                    "Сұрақтар табылмады. Форматты тексеріңіз."
                )

            else:

                if subject not in questions:
                    questions[subject] = []

                questions[subject].extend(
                    parsed
                )

                save_questions(
                    questions
                )

                st.success(
                    f"✅ {len(parsed)} сұрақ қосылды!"
                )

                st.rerun()

    # =====================================================
    # EXCEL
    # =====================================================

    with tabs[1]:

        st.markdown(
            "### 📥 Excel арқылы сұрақ импорттау"
        )

        subject = st.selectbox(
            "Пән",
            all_subjects,
            key="excel_subject",
        )

        uploaded_file = st.file_uploader(
            "Excel файлды таңдаңыз",
            type=[
                "xlsx",
                "xls",
            ],
        )

        if uploaded_file:

            parsed = parse_excel_questions(
                uploaded_file
            )

            st.info(
                f"Табылған сұрақ саны: {len(parsed)}"
            )

            if parsed:

                preview_rows = []

                for index, item in enumerate(
                    parsed[:10],
                    start=1
                ):

                    preview_rows.append(
                        {
                            "№": index,
                            "Сұрақ": item[
                                "question"
                            ],
                            "Дұрыс жауап": (
                                item["answer"] + 1
                            ),
                        }
                    )

                st.dataframe(
                    pd.DataFrame(preview_rows),
                    use_container_width=True,
                    hide_index=True,
                )

                if st.button(
                    "📥 Excel сұрақтарын сақтау",
                    type="primary",
                ):

                    if subject not in questions:
                        questions[subject] = []

                    questions[subject].extend(
                        parsed
                    )

                    save_questions(
                        questions
                    )

                    st.success(
                        f"✅ {len(parsed)} сұрақ сақталды!"
                    )

                    st.rerun()

    # =====================================================
    # DELETE
    # =====================================================

    with tabs[2]:

        st.markdown(
            "### 🗑️ Сұрақтарды басқару"
        )

        subject = st.selectbox(
            "Пәнді таңдаңыз",
            all_subjects,
            key="delete_subject",
        )

        subject_questions = questions.get(
            subject,
            []
        )

        if not subject_questions:

            st.markdown(
                """
                <div class="card"
                     style="text-align:center;">
                    Бұл пәнде сұрақ жоқ.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            question_options = [
                f"{index + 1}. "
                f"{item.get('question', '')[:100]}"
                for index, item in enumerate(
                    subject_questions
                )
            ]

            selected_question = st.selectbox(
                "Сұрақ",
                question_options,
                key="question_to_delete",
            )

            selected_index = (
                question_options.index(
                    selected_question
                )
            )

            question = subject_questions[
                selected_index
            ]

            st.markdown(
                f"""
                <div class="question-box">

                    <div style="
                        color:#60A5FA;
                        font-size:12px;
                        font-weight:800;
                        margin-bottom:10px;
                    ">
                        СҰРАҚ
                    </div>

                    <div class="question-text">
                        {question.get('question', '')}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            pending = st.session_state.get(
                "pending_delete_question"
            )

            pending_key = (
                f"{subject}:{selected_index}"
            )

            if pending == pending_key:

                st.warning(
                    "⚠️ Бұл сұрақты шынымен өшіргіңіз келе ме?"
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "✅ Иә, өшіру",
                        key="confirm_question_delete",
                        use_container_width=True,
                        type="primary",
                    ):

                        del questions[
                            subject
                        ][selected_index]

                        save_questions(
                            questions
                        )

                        st.session_state.pending_delete_question = None

                        st.success(
                            "Сұрақ өшірілді."
                        )

                        st.rerun()

                with c2:

                    if st.button(
                        "❌ Болдырмау",
                        key="cancel_question_delete",
                        use_container_width=True,
                    ):

                        st.session_state.pending_delete_question = None

                        st.rerun()

            else:

                if st.button(
                    "🗑️ Жою",
                    key="delete_question_button",
                ):

                    st.session_state.pending_delete_question = pending_key

                    st.rerun()


# =========================================================
# ADMIN PAGE
# =========================================================

def admin_page():

    if (
        not st.session_state.logged_in
        or st.session_state.role != "admin"
    ):

        st.error(
            "Бұл бөлімге кіруге рұқсат жоқ."
        )

        return

    top1, top2 = st.columns([7, 1])

    with top1:

        st.markdown(
            """
            <div class="kasym-title"
                 style="font-size:36px;">
                KASYM EDU
            </div>

            <div class="kasym-subtitle">
                👑 Әкімшілік басқару панелі
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top2:

        if st.button(
            "↪ Шығу",
            use_container_width=True,
        ):

            logout()

    tabs = st.tabs(
        [
            "👥 Қолданушылар",
            "➕ Жаңа қолданушы",
            "📊 Статистика",
        ]
    )

    # =====================================================
    # USERS
    # =====================================================

    with tabs[0]:

        st.markdown(
            "### 👥 Қолданушылар"
        )

        current_users = users

        if not current_users:

            st.info(
                "Қолданушылар жоқ."
            )

        else:

            pending_user_delete = (
                st.session_state.get(
                    "pending_user_delete"
                )
            )

            for index, user in enumerate(
                current_users
            ):

                u_username = user.get(
                    "username",
                    ""
                )

                u_name = user.get(
                    "name",
                    ""
                )

                u_role = user.get(
                    "role",
                    "user"
                )

                u_combination = user.get(
                    "combination"
                )

                role_label = {

                    "admin": "👑 Админ",

                    "moderator": "🧑‍💼 Модератор",

                    "user": "👨‍🎓 Оқушы",

                }.get(
                    u_role,
                    u_role
                )

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True,
                )

                col1, col2, col3, col4 = st.columns(
                    [2, 2, 2, 1]
                )

                with col1:

                    st.markdown(
                        f"**{u_name}**"
                    )

                    st.caption(
                        f"Логин: `{u_username}`"
                    )

                with col2:

                    st.markdown(
                        f"**Рөл:** {role_label}"
                    )

                with col3:

                    if u_combination:

                        st.markdown(
                            f"**Бағыт:** {u_combination}"
                        )

                    else:

                        st.markdown(
                            "**Бағыт:** —"
                        )

                with col4:

                    if u_username == ADMIN_USERNAME:

                        st.caption(
                            "🔒 Негізгі админ"
                        )

                    else:

                        delete_key = (
                            f"delete_user_{u_username}"
                        )

                        if (
                            pending_user_delete
                            == u_username
                        ):

                            st.warning(
                                "Өшіру?"
                            )

                            c1, c2 = st.columns(2)

                            with c1:

                                if st.button(
                                    "✅ Иә",
                                    key=f"confirm_{u_username}",
                                    use_container_width=True,
                                    type="primary",
                                ):

                                    users[:] = [
                                        x
                                        for x in users
                                        if x.get(
                                            "username"
                                        ) != u_username
                                    ]

                                    save_users(
                                        users
                                    )

                                    st.session_state.pending_user_delete = None

                                    st.success(
                                        "Қолданушы өшірілді."
                                    )

                                    st.rerun()

                            with c2:

                                if st.button(
                                    "❌ Жоқ",
                                    key=f"cancel_{u_username}",
                                    use_container_width=True,
                                ):

                                    st.session_state.pending_user_delete = None

                                    st.rerun()

                        else:

                            if st.button(
                                "🗑️ Жою",
                                key=delete_key,
                                use_container_width=True,
                            ):

                                st.session_state.pending_user_delete = u_username

                                st.rerun()

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

    # =====================================================
    # NEW USER
    # =====================================================

    with tabs[1]:

        st.markdown(
            "### ➕ Жаңа қолданушы"
        )

        new_name = st.text_input(
            "Аты-жөні",
            placeholder="Мысалы: Алишер",
        )

        new_username = st.text_input(
            "Логин",
            placeholder="Мысалы: alisher01",
        )

        new_password = st.text_input(
            "Құпиясөз",
            type="password",
        )

        new_role = st.selectbox(
            "Рөл",
            [
                "user",
                "moderator",
            ],
            format_func=lambda x: {
                "user": "👨‍🎓 Оқушы",
                "moderator": "🧑‍💼 Модератор",
            }.get(
                x,
                x
            ),
        )

        if new_role == "user":

            new_combination = st.selectbox(
                "ҰБТ бағыты",
                list(combinations.keys()),
            )

        else:

            new_combination = None

        if st.button(
            "➕ Қолданушыны жасау",
            type="primary",
        ):

            username_clean = (
                new_username.strip()
            )

            if not new_name.strip():

                st.warning(
                    "Аты-жөнін енгізіңіз."
                )

            elif not username_clean:

                st.warning(
                    "Логин енгізіңіз."
                )

            elif not new_password:

                st.warning(
                    "Құпиясөз енгізіңіз."
                )

            elif any(
                user.get("username")
                == username_clean
                for user in users
            ):

                st.error(
                    "Бұл логин бұрыннан бар."
                )

            else:

                users.append(
                    {
                        "username": username_clean,

                        "password": hash_password(
                            new_password
                        ),

                        "name": new_name.strip(),

                        "role": new_role,

                        "combination": new_combination,
                    }
                )

                save_users(
                    users
                )

                st.success(
                    f"✅ {username_clean} қолданушысы жасалды."
                )

                st.rerun()

    # =====================================================
    # STATISTICS
    # =====================================================

    with tabs[2]:

        st.markdown(
            "### 📊 Жалпы статистика"
        )

        total_users = len(users)

        total_students = len(
            [
                user
                for user in users
                if user.get("role") == "user"
            ]
        )

        total_moderators = len(
            [
                user
                for user in users
                if user.get("role") == "moderator"
            ]
        )

        total_tests = len(
            results_history
        )

        col1, col2, col3, col4 = st.columns(4)

        stats_data = [
            (
                total_users,
                "👥",
                "Қолданушы"
            ),
            (
                total_students,
                "🎓",
                "Оқушы"
            ),
            (
                total_moderators,
                "🧑‍💼",
                "Модератор"
            ),
            (
                total_tests,
                "📝",
                "Тест саны"
            ),
        ]

        for column, data in zip(
            [col1, col2, col3, col4],
            stats_data
        ):

            with column:

                number, icon, label = data

                st.markdown(
                    f"""
                    <div class="metric-box">

                        <div style="
                            font-size:23px;
                            margin-bottom:6px;
                        ">
                            {icon}
                        </div>

                        <div class="metric-number">
                            {number}
                        </div>

                        <div class="metric-label">
                            {label}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            "### 👥 Қолданушылар"
        )

        user_rows = []

        for user in users:

            user_stats = (
                calculate_user_statistics(
                    user.get("username")
                )
            )

            user_rows.append(
                {
                    "Аты": user.get(
                        "name",
                        "-"
                    ),

                    "Логин": user.get(
                        "username",
                        "-"
                    ),

                    "Рөл": user.get(
                        "role",
                        "-"
                    ),

                    "Тест саны": user_stats[
                        "attempts"
                    ],

                    "Үздік балл": user_stats[
                        "best"
                    ],

                    "Орташа": user_stats[
                        "average"
                    ],
                }
            )

        if user_rows:

            st.dataframe(
                pd.DataFrame(user_rows),
                use_container_width=True,
                hide_index=True,
            )


# =========================================================
# PREPARE TEST
# =========================================================

def prepare_test_data(combination_name):

    combination = combinations.get(
        combination_name
    )

    if not combination:
        return {}

    subjects = (
        combination["common"]
        + combination["pair"]
    )

    test_data = {}

    for subject in subjects:

        source_questions = questions.get(
            subject,
            []
        )

        if not source_questions:

            test_data[subject] = []

            continue

        limit = QUESTION_LIMITS.get(
            subject,
            40
        )

        selected = source_questions.copy()

        random.shuffle(selected)

        selected = selected[:limit]

        prepared = []

        for item in selected:

            options = item.get(
                "options",
                []
            )

            correct = item.get(
                "answer",
                0
            )

            option_pairs = list(
                enumerate(options)
            )

            random.shuffle(option_pairs)

            new_options = [
                pair[1]
                for pair in option_pairs
            ]

            new_correct = 0

            for new_index, pair in enumerate(
                option_pairs
            ):

                old_index = pair[0]

                if old_index == correct:

                    new_correct = new_index

                    break

            prepared.append(
                {
                    "question": item.get(
                        "question",
                        ""
                    ),

                    "options": new_options,

                    "answer": new_correct,
                }
            )

        test_data[subject] = prepared

    return test_data


# =========================================================
# START TEST
# =========================================================

def start_test(combination_name):

    st.session_state.test_started = True

    st.session_state.active_combination = (
        combination_name
    )

    st.session_state.current_subject_idx = 0

    st.session_state.current_question_idx = 0

    st.session_state.test_answers = {}

    st.session_state.test_data = (
        prepare_test_data(
            combination_name
        )
    )

    st.session_state.started_at = (
        datetime.datetime.now().isoformat()
    )

    st.session_state.retry_mode = False

    st.session_state.saved_result_id = None

    save_test_progress()


# =========================================================
# GET TEST SUBJECTS
# =========================================================

def get_test_subjects():

    combination_name = (
        st.session_state.active_combination
    )

    if not combination_name:
        return []

    combination = combinations.get(
        combination_name
    )

    if not combination:
        return []

    return (
        combination["common"]
        + combination["pair"]
    )


# =========================================================
# USER PAGE
# =========================================================

def user_page():

    username = st.session_state.username

    # =====================================================
    # TEST
    # =====================================================

    if st.session_state.test_started:

        render_test()

        return

    # =====================================================
    # RESULT
    # =====================================================

    if st.session_state.page == "result":

        render_result()

        return

    # =====================================================
    # RETRY RESULT
    # =====================================================

    if st.session_state.page == "retry_result":

        render_retry_result()

        return

    # =====================================================
    # ANALYTICS
    # =====================================================

    if st.session_state.page == "analytics":

        analytics_page(username)

        if st.button(
            "⬅️ Басты бетке",
            use_container_width=True,
        ):

            st.session_state.page = "home"

            st.rerun()

        return

    # =====================================================
    # FIND USER
    # =====================================================

    current_user = None

    for user in users:

        if user.get("username") == username:

            current_user = user

            break

    if not current_user:

        st.error(
            "Қолданушы табылмады."
        )

        return

    assigned_combination = current_user.get(
        "combination"
    )

    # =====================================================
    # TOP BAR
    # =====================================================

    top1, top2 = st.columns([7, 1])

    with top1:

        st.markdown(
            """
            <div class="kasym-title">
                KASYM EDU
                <span style="
                    font-size:34px;
                    color:#3B82F6;
                ">
                    ✦
                </span>
            </div>

            <div class="kasym-subtitle">
                Бүгінгі дайындық — ертеңгі грант
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top2:

        if st.button(
            "↪ Шығу",
            use_container_width=True,
        ):

            logout()

    # =====================================================
    # GREETING
    # =====================================================

    st.markdown(
        f"""
        <div class="hero">

            <div style="
                color:#60A5FA;
                font-size:13px;
                font-weight:800;
                margin-bottom:8px;
            ">
                ОҚУШЫ КАБИНЕТІ
            </div>

            <h2 style="
                font-size:34px;
                margin-bottom:8px;
            ">
                Сәлем, {st.session_state.full_name}! 👋
            </h2>

            <p style="
                font-size:16px;
                max-width:700px;
            ">
                Бүгінгі тестіңді орындап,
                өз нәтижеңді жақсарта бер.
                Әрбір дұрыс жауап — грантқа тағы бір қадам.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # RESUME
    # =====================================================

    progress = load_test_progress()

    if (
        progress
        and progress.get("username") == username
        and progress.get("active_combination")
    ):

        st.markdown(
            f"""
            <div class="resume-card">

                <div style="
                    color:#4ADE80;
                    font-size:12px;
                    font-weight:850;
                    margin-bottom:7px;
                ">
                    ● САҚТАЛҒАН ТЕСТ
                </div>

                <h3 style="margin:0;">
                    🔄 Аяқталмаған тест бар
                </h3>

                <p>
                    <b>
                        {progress.get("active_combination")}
                    </b>
                    бағыты бойынша тест сақталған.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "▶️ Тестті жалғастыру",
                use_container_width=True,
                type="primary",
            ):

                st.session_state.test_started = True

                st.session_state.active_combination = (
                    progress.get(
                        "active_combination"
                    )
                )

                st.session_state.current_subject_idx = (
                    progress.get(
                        "current_subject_idx",
                        0
                    )
                )

                st.session_state.current_question_idx = (
                    progress.get(
                        "current_question_idx",
                        0
                    )
                )

                st.session_state.test_answers = (
                    progress.get(
                        "test_answers",
                        {}
                    )
                )

                st.session_state.test_data = (
                    progress.get(
                        "test_data",
                        {}
                    )
                )

                st.session_state.started_at = (
                    progress.get(
                        "started_at"
                    )
                )

                st.session_state.saved_result_id = None

                st.rerun()

        with c2:

            if st.button(
                "🗑️ Тестті өшіру",
                use_container_width=True,
            ):

                clear_test_progress()

                st.success(
                    "Сақталған тест өшірілді."
                )

                st.rerun()

    # =====================================================
    # STATISTICS
    # =====================================================

    stats = calculate_user_statistics(
        username
    )

    st.markdown(
        "### 📊 Сенің көрсеткіштерің"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:22px;
                    margin-bottom:8px;
                ">
                    📝
                </div>

                <div class="metric-number">
                    {stats["attempts"]}
                </div>

                <div class="metric-label">
                    Орындалған тест
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:22px;
                    margin-bottom:8px;
                ">
                    🏆
                </div>

                <div class="metric-number">
                    {stats["best"]:.0f}
                    <span style="
                        font-size:15px;
                        color:#64748B;
                    ">
                        / 140
                    </span>
                </div>

                <div class="metric-label">
                    Ең жоғары нәтиже
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:22px;
                    margin-bottom:8px;
                ">
                    📈
                </div>

                <div class="metric-number">
                    {stats["average"]:.1f}
                </div>

                <div class="metric-label">
                    Орташа балл
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button(
        "📊 Толық аналитиканы ашу",
        use_container_width=True,
    ):

        st.session_state.page = "analytics"

        st.rerun()

    # =====================================================
    # DIRECTION
    # =====================================================

    st.markdown(
        "### 🎯 Менің ҰБТ бағытым"
    )

    if not assigned_combination:

        st.warning(
            "Сізге ҰБТ бағыты әлі тағайындалмаған."
        )

        return

    combination_info = combinations.get(
        assigned_combination
    )

    st.markdown(
        f"""
        <div class="hero">

            <div style="
                color:#60A5FA;
                font-size:12px;
                font-weight:850;
                margin-bottom:10px;
            ">
                СІЗГЕ БЕКІТІЛГЕН БАҒЫТ
            </div>

            <h2>
                🎯 {assigned_combination}
            </h2>

            <p>
                Бұл бағыт бойынша барлық негізгі және
                бейіндік пәндер бір тесттің ішінде беріледі.
            </p>

            <div style="
                display:inline-block;
                margin-top:8px;
                padding:9px 15px;
                border-radius:12px;
                background:rgba(37,99,235,0.16);
                border:1px solid rgba(59,130,246,0.20);
                color:#93C5FD;
                font-weight:800;
            ">
                Максимум — 140 балл
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # SUBJECTS
    # =====================================================

    if combination_info:

        subjects = (
            combination_info["common"]
            + combination_info["pair"]
        )

        st.markdown(
            "### 📚 Тест пәндері"
        )

        cols = st.columns(3)

        for index, subject in enumerate(
            subjects
        ):

            with cols[
                index % 3
            ]:

                is_common = (
                    subject
                    in combination_info["common"]
                )

                badge = (
                    "ЖАЛПЫ ПӘН"
                    if is_common
                    else "БЕЙІНДІК ПӘН"
                )

                badge_color = (
                    "#60A5FA"
                    if is_common
                    else "#A78BFA"
                )

                st.markdown(
                    f"""
                    <div class="card">

                        <div style="
                            color:{badge_color};
                            font-size:11px;
                            font-weight:850;
                            letter-spacing:0.8px;
                            margin-bottom:10px;
                        ">
                            {badge}
                        </div>

                        <h3 style="
                            margin-bottom:8px;
                        ">
                            {subject}
                        </h3>

                        <div style="
                            color:#94A3B8;
                            font-size:14px;
                        ">
                            {QUESTION_LIMITS.get(
                                subject,
                                40
                            )}
                            сұрақ
                        </div>

                        <div style="
                            color:#CBD5E1;
                            font-size:14px;
                            margin-top:5px;
                        ">
                            Максимум:
                            <b>
                                {POINT_LIMITS.get(
                                    subject,
                                    50
                                )}
                            </b>
                            балл
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # =====================================================
    # START
    # =====================================================

    st.markdown(
        """
        <div style="
            margin-top:15px;
            margin-bottom:10px;
        ">

            <h3>
                🚀 Дайынсың ба?
            </h3>

            <p style="color:#64748B;">
                Тестті бастағаннан кейін сұрақтар
                кездейсоқ ретпен беріледі.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🚀 ҰБТ тестін бастау",
        type="primary",
        use_container_width=True,
    ):

        clear_test_progress()

        st.session_state.saved_result_id = None

        start_test(
            assigned_combination
        )

        st.rerun()


# =========================================================
# TEST RENDER
# =========================================================

def render_test():

    subjects = get_test_subjects()

    if not subjects:

        st.error(
            "Тест пәндері табылмады."
        )

        return

    subject_index = (
        st.session_state.current_subject_idx
    )

    question_index = (
        st.session_state.current_question_idx
    )

    if subject_index >= len(subjects):

        finish_test()

        return

    subject = subjects[
        subject_index
    ]

    subject_questions = (
        st.session_state.test_data.get(
            subject,
            []
        )
    )

    if not subject_questions:

        st.warning(
            f"{subject} пәнінде жеткілікті сұрақ жоқ."
        )

        if st.button(
            "⬅️ Басты бетке",
            use_container_width=True,
        ):

            st.session_state.test_started = False

            clear_test_progress()

            st.rerun()

        return

    if question_index >= len(subject_questions):

        question_index = 0

        st.session_state.current_question_idx = 0

    question = subject_questions[
        question_index
    ]

    total_questions = len(
        subject_questions
    )

    answer_key = (
        f"{subject}_{question_index}"
    )

    current_answer = (
        st.session_state.test_answers.get(
            answer_key
        )
    )

    # =====================================================
    # TOP
    # =====================================================

    col1, col2 = st.columns([6, 1])

    with col1:

        st.markdown(
            f"""
            <div style="
                color:#60A5FA;
                font-size:12px;
                font-weight:850;
                letter-spacing:0.8px;
            ">
                ҰБТ ТЕСТІ
            </div>

            <h2 style="margin-top:5px;">
                📚 {subject}
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            f"Сұрақ {question_index + 1} / {total_questions}"
        )

    with col2:

        if st.button(
            "↪ Шығу",
            use_container_width=True,
        ):

            save_test_progress()

            st.session_state.test_started = False

            st.rerun()

    # =====================================================
    # SUBJECT NAVIGATION
    # =====================================================

    st.markdown(
        "### Пәндер"
    )

    subject_cols = st.columns(
        len(subjects)
    )

    for index, sub in enumerate(subjects):

        with subject_cols[index]:

            if st.button(
                sub,
                key=f"subject_nav_{index}",
                use_container_width=True,
            ):

                st.session_state.current_subject_idx = index

                st.session_state.current_question_idx = 0

                save_test_progress()

                st.rerun()

    # =====================================================
    # PALETTE
    # =====================================================

    st.markdown(
        "### 🧭 Сұрақтар"
    )

    palette = []

    for i in range(
        total_questions
    ):

        key = f"{subject}_{i}"

        if i == question_index:

            state = "🔵"

        elif key in st.session_state.test_answers:

            state = "🟢"

        else:

            state = "⚪"

        palette.append(
            (
                i,
                state
            )
        )

    for start in range(
        0,
        len(palette),
        20
    ):

        row = palette[
            start:start + 20
        ]

        cols = st.columns(
            len(row)
        )

        for col, (number, state) in zip(
            cols,
            row
        ):

            with col:

                if st.button(
                    f"{state} {number + 1}",
                    key=f"palette_{subject}_{number}",
                    use_container_width=True,
                ):

                    st.session_state.current_question_idx = number

                    save_test_progress()

                    st.rerun()

    # =====================================================
    # QUESTION
    # =====================================================

    st.markdown(
        f"""
        <div class="question-box">

            <div style="
                color:#60A5FA;
                font-size:12px;
                font-weight:850;
                margin-bottom:12px;
            ">
                СҰРАҚ {question_index + 1}
            </div>

            <div class="question-text">
                {question.get("question", "")}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    options = question.get(
        "options",
        []
    )

    option_labels = [
        "A",
        "B",
        "C",
        "D",
    ]

    radio_options = []

    for index, option in enumerate(
        options
    ):

        if index >= len(option_labels):
            break

        label = (
            f"{option_labels[index]}. {option}"
        )

        radio_options.append(
            label
        )

    selected_index = None

    if current_answer is not None:

        if (
            0 <= current_answer
            < len(radio_options)
        ):

            selected_index = current_answer

    radio_value = 0

    if selected_index is not None:

        radio_value = selected_index

    selected_label = st.radio(
        "Жауапты таңдаңыз:",
        radio_options,
        index=(
            radio_value
            if current_answer is not None
            else None
        ),
        key=f"answer_radio_{subject}_{question_index}",
    )

    if selected_label:

        try:

            selected_index = (
                radio_options.index(
                    selected_label
                )
            )

            st.session_state.test_answers[
                answer_key
            ] = selected_index

            save_test_progress()

        except ValueError:

            pass

    # =====================================================
    # NAVIGATION
    # =====================================================

    st.markdown("---")

    nav1, nav2, nav3 = st.columns(
        [1, 1, 1]
    )

    with nav1:

        if st.button(
            "⬅️ Алдыңғы",
            use_container_width=True,
            disabled=(
                subject_index == 0
                and question_index == 0
            ),
        ):

            if question_index > 0:

                st.session_state.current_question_idx -= 1

            elif subject_index > 0:

                st.session_state.current_subject_idx -= 1

                previous_subject = subjects[
                    subject_index - 1
                ]

                previous_questions = (
                    st.session_state.test_data.get(
                        previous_subject,
                        []
                    )
                )

                st.session_state.current_question_idx = max(
                    len(previous_questions) - 1,
                    0
                )

            save_test_progress()

            st.rerun()

    with nav2:

        answered = len(
            st.session_state.test_answers
        )

        total_all = sum(
            len(
                st.session_state.test_data.get(
                    sub,
                    []
                )
            )
            for sub in subjects
        )

        percentage = 0

        if total_all > 0:

            percentage = round(
                answered / total_all * 100
            )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:7px;
            ">

                <div style="
                    font-size:20px;
                    font-weight:850;
                    color:#F8FAFC;
                ">
                    {answered} / {total_all}
                </div>

                <div style="
                    font-size:11px;
                    color:#64748B;
                ">
                    жауап берілді · {percentage}%
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav3:

        is_last_question = (
            question_index
            == total_questions - 1
            and subject_index
            == len(subjects) - 1
        )

        if is_last_question:

            if st.button(
                "🏁 Аяқтау",
                use_container_width=True,
                type="primary",
            ):

                finish_test()

        else:

            if st.button(
                "Келесі ➡️",
                use_container_width=True,
                type="primary",
            ):

                if (
                    question_index
                    < total_questions - 1
                ):

                    st.session_state.current_question_idx += 1

                else:

                    st.session_state.current_subject_idx += 1

                    st.session_state.current_question_idx = 0

                save_test_progress()

                st.rerun()


# =========================================================
# FINISH
# =========================================================

def finish_test():

    st.session_state.test_started = False

    clear_test_progress()

    st.session_state.page = "result"

    st.rerun()


# =========================================================
# CALCULATE RESULTS
# =========================================================

def calculate_results():

    subjects = get_test_subjects()

    subject_results = {}

    total_score = 0

    total_possible = 0

    total_correct = 0

    total_wrong = 0

    total_unanswered = 0

    for subject in subjects:

        subject_questions = (
            st.session_state.test_data.get(
                subject,
                []
            )
        )

        correct = 0

        wrong = 0

        unanswered = 0

        answers = (
            st.session_state.test_answers
        )

        for index, question in enumerate(
            subject_questions
        ):

            key = f"{subject}_{index}"

            if key not in answers:

                unanswered += 1

                continue

            selected = answers[key]

            correct_answer = question.get(
                "answer",
                0
            )

            if selected == correct_answer:

                correct += 1

            else:

                wrong += 1

        total_questions = len(
            subject_questions
        )

        max_points = POINT_LIMITS.get(
            subject,
            0
        )

        if subject in [
            "Қазақстан тарихы",
            "Оқу сауаттылығы",
            "Математикалық сауаттылық",
        ]:

            score = correct

        else:

            if total_questions > 0:

                score = round(
                    correct
                    / total_questions
                    * max_points,
                    2
                )

            else:

                score = 0

        subject_results[subject] = {

            "correct": correct,

            "wrong": wrong,

            "unanswered": unanswered,

            "total": total_questions,

            "score": score,

            "max_score": max_points,
        }

        total_score += score

        total_possible += max_points

        total_correct += correct

        total_wrong += wrong

        total_unanswered += unanswered

    percentage = 0

    if total_possible > 0:

        percentage = round(
            total_score
            / total_possible
            * 100,
            1
        )

    return {

        "subject_results": subject_results,

        "total_score": round(
            total_score,
            2
        ),

        "total_possible": total_possible,

        "percentage": percentage,

        "total_correct": total_correct,

        "total_wrong": total_wrong,

        "total_unanswered": total_unanswered,
    }


# =========================================================
# SAVE NORMAL RESULT
# =========================================================

def save_normal_result(result_data):

    username = st.session_state.username

    existing_result_id = (
        st.session_state.get(
            "saved_result_id"
        )
    )

    if existing_result_id:

        return

    now = datetime.datetime.now()

    result_id = (
        f"{username}_"
        f"{now.strftime('%Y%m%d%H%M%S')}"
    )

    result_record = {

        "id": result_id,

        "username": username,

        "name": st.session_state.full_name,

        "combination": (
            st.session_state.active_combination
        ),

        "date": now.strftime(
            "%Y-%m-%d %H:%M"
        ),

        "total_score": result_data[
            "total_score"
        ],

        "percentage": result_data[
            "percentage"
        ],

        "subject_results": result_data[
            "subject_results"
        ],
    }

    results_history.append(
        result_record
    )

    save_results(
        results_history
    )

    st.session_state.saved_result_id = (
        result_id
    )


# =========================================================
# RESULT PAGE
# =========================================================

def render_result():

    result_data = calculate_results()

    save_normal_result(
        result_data
    )

    clear_test_progress()

    st.markdown(
        "## 🏆 Тест нәтижесі"
    )

    st.markdown(
        f"""
        <div class="hero"
             style="text-align:center;">

            <div style="
                color:#94A3B8;
                font-size:13px;
                font-weight:800;
                letter-spacing:1px;
            ">
                ЖАЛПЫ НӘТИЖЕ
            </div>

            <div class="score-big"
                 style="margin-top:15px;">

                {result_data["total_score"]:.0f}
                /
                {result_data["total_possible"]}

            </div>

            <div style="
                font-size:22px;
                margin-top:12px;
                color:#60A5FA;
                font-weight:800;
            ">
                {result_data["percentage"]}%
            </div>

            <div style="
                margin-top:16px;
                color:#CBD5E1;
            ">
                {st.session_state.active_combination}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:25px;
                ">
                    🟢
                </div>

                <div class="metric-number">
                    {result_data["total_correct"]}
                </div>

                <div class="metric-label">
                    Дұрыс
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:25px;
                ">
                    🔴
                </div>

                <div class="metric-number">
                    {result_data["total_wrong"]}
                </div>

                <div class="metric-label">
                    Қате
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="
                    font-size:25px;
                ">
                    ⚪
                </div>

                <div class="metric-number">
                    {result_data["total_unanswered"]}
                </div>

                <div class="metric-label">
                    Жауапсыз
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    if result_data["percentage"] >= 80:

        st.success(
            "🔥 Өте жақсы нәтиже! Осы қарқынмен жалғастыр!"
        )

    elif result_data["percentage"] >= 60:

        st.info(
            "👍 Жақсы нәтиже! Әлсіз тақырыптарды тағы қайтала."
        )

    else:

        st.warning(
            "📚 Нәтижеңді көтеруге мүмкіндік көп. Қате сұрақтарды қайталап шық."
        )

    # =====================================================
    # SUBJECT RESULTS
    # =====================================================

    st.markdown(
        "### 📚 Пәндер бойынша нәтиже"
    )

    for subject, data in result_data[
        "subject_results"
    ].items():

        percentage = 0

        if data["total"] > 0:

            percentage = round(
                data["correct"]
                / data["total"]
                * 100,
                1
            )

        st.markdown(
            f"""
            <div class="card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <h3 style="margin:0;">
                        {subject}
                    </h3>

                    <div style="
                        color:#60A5FA;
                        font-weight:850;
                    ">
                        {percentage}%
                    </div>

                </div>

                <div style="
                    margin-top:15px;
                    color:#CBD5E1;
                ">

                    🟢 Дұрыс:
                    <b>{data["correct"]}</b>

                    &nbsp;&nbsp;

                    🔴 Қате:
                    <b>{data["wrong"]}</b>

                    &nbsp;&nbsp;

                    ⚪ Жауапсыз:
                    <b>{data["unanswered"]}</b>

                </div>

                <div style="
                    margin-top:10px;
                    color:#94A3B8;
                ">

                    Балл:
                    <b style="color:#F8FAFC;">
                        {data["score"]:.0f}
                    </b>
                    /
                    {data["max_score"]}

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # REVIEW
    # =====================================================

    st.markdown(
        "### 🔍 Сұрақтарды талдау"
    )

    for subject in get_test_subjects():

        subject_questions = (
            st.session_state.test_data.get(
                subject,
                []
            )
        )

        if not subject_questions:

            continue

        with st.expander(
            f"📖 {subject}"
        ):

            for index, question in enumerate(
                subject_questions
            ):

                key = f"{subject}_{index}"

                selected = (
                    st.session_state.test_answers.get(
                        key
                    )
                )

                correct = question.get(
                    "answer",
                    0
                )

                options = question.get(
                    "options",
                    []
                )

                st.markdown(
                    f"""
                    <div style="
                        font-weight:750;
                        font-size:16px;
                        margin-bottom:10px;
                    ">
                        {index + 1}.
                        {question.get(
                            'question',
                            ''
                        )}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if selected is None:

                    st.markdown(
                        """
                        <div class="unanswered-box">
                            ⚪ Жауап берілмеді
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                elif selected == correct:

                    st.markdown(
                        f"""
                        <div class="correct-box">
                            🟢 Дұрыс жауап:<br>
                            <b>
                                {options[correct]}
                            </b>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="wrong-box">

                            🔴 Сенің жауабың:
                            <b>
                                {options[selected]}
                            </b>

                            <br><br>

                            🟢 Дұрыс жауап:
                            <b>
                                {options[correct]}
                            </b>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("---")

    # =====================================================
    # RETRY
    # =====================================================

    if st.button(
        "🔄 Қате және жауапсыз сұрақтарды қайта тапсыру",
        use_container_width=True,
    ):

        retry_questions = {}

        for subject in get_test_subjects():

            subject_questions = (
                st.session_state.test_data.get(
                    subject,
                    []
                )
            )

            for index, question in enumerate(
                subject_questions
            ):

                key = f"{subject}_{index}"

                selected = (
                    st.session_state.test_answers.get(
                        key
                    )
                )

                correct = question.get(
                    "answer",
                    0
                )

                if (
                    selected is None
                    or selected != correct
                ):

                    if subject not in retry_questions:

                        retry_questions[subject] = []

                    retry_questions[subject].append(
                        question
                    )

        if retry_questions:

            st.session_state.retry_mode = True

            st.session_state.retry_questions = (
                retry_questions
            )

            st.session_state.retry_answers = {}

            st.session_state.retry_subject_idx = 0

            st.session_state.retry_question_idx = 0

            st.session_state.page = "retry_test"

            st.rerun()

        else:

            st.success(
                "🎉 Барлық сұраққа дұрыс жауап бердің!"
            )

    if st.button(
        "🏠 Басты бетке",
        use_container_width=True,
    ):

        st.session_state.page = "home"

        st.session_state.test_started = False

        st.session_state.test_data = {}

        st.session_state.test_answers = {}

        st.session_state.saved_result_id = None

        st.rerun()


# =========================================================
# RETRY TEST
# =========================================================

def render_retry_test():

    retry_questions = (
        st.session_state.retry_questions
    )

    subjects = list(
        retry_questions.keys()
    )

    if not subjects:

        st.session_state.page = "home"

        st.rerun()

        return

    subject_index = (
        st.session_state.get(
            "retry_subject_idx",
            0
        )
    )

    question_index = (
        st.session_state.get(
            "retry_question_idx",
            0
        )
    )

    if subject_index >= len(subjects):

        st.session_state.page = "retry_result"

        st.rerun()

        return

    subject = subjects[
        subject_index
    ]

    subject_questions = retry_questions[
        subject
    ]

    question = subject_questions[
        question_index
    ]

    answer_key = (
        f"{subject}_{question_index}"
    )

    current_answer = (
        st.session_state.retry_answers.get(
            answer_key
        )
    )

    top1, top2 = st.columns([7, 1])

    with top1:

        st.markdown(
            """
            <div class="kasym-title"
                 style="font-size:32px;">
                🔄 Қате сұрақтарды қайталау
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top2:

        if st.button(
            "↪ Шығу",
            use_container_width=True,
        ):

            st.session_state.page = "home"

            st.session_state.retry_mode = False

            st.session_state.retry_questions = {}

            st.session_state.retry_answers = {}

            st.rerun()

    st.markdown(
        f"""
        <div style="
            color:#A78BFA;
            font-weight:800;
            font-size:13px;
            margin-top:15px;
        ">
            {subject}
        </div>

        <div style="
            color:#64748B;
            margin-top:5px;
        ">
            Сұрақ {question_index + 1}
            /
            {len(subject_questions)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="question-box">

            <div style="
                color:#A78BFA;
                font-size:12px;
                font-weight:850;
                margin-bottom:12px;
            ">
                ҚАЙТАЛАУ
            </div>

            <div class="question-text">
                {question.get("question", "")}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    options = question.get(
        "options",
        []
    )

    labels = [
        "A",
        "B",
        "C",
        "D",
    ]

    radio_options = [
        f"{labels[i]}. {option}"
        for i, option in enumerate(options)
        if i < 4
    ]

    selected = st.radio(
        "Жауап:",
        radio_options,
        index=(
            current_answer
            if current_answer is not None
            else None
        ),
        key=f"retry_radio_{subject}_{question_index}",
    )

    if selected:

        selected_index = (
            radio_options.index(
                selected
            )
        )

        st.session_state.retry_answers[
            answer_key
        ] = selected_index

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅️ Алдыңғы",
            use_container_width=True,
            disabled=(
                subject_index == 0
                and question_index == 0
            ),
        ):

            if question_index > 0:

                st.session_state.retry_question_idx -= 1

            else:

                st.session_state.retry_subject_idx -= 1

                previous_subject = subjects[
                    subject_index - 1
                ]

                st.session_state.retry_question_idx = (
                    len(
                        retry_questions[
                            previous_subject
                        ]
                    ) - 1
                )

            st.rerun()

    with col2:

        is_last = (
            subject_index == len(subjects) - 1
            and question_index
            == len(subject_questions) - 1
        )

        if is_last:

            if st.button(
                "🏁 Аяқтау",
                use_container_width=True,
                type="primary",
            ):

                st.session_state.page = "retry_result"

                st.rerun()

        else:

            if st.button(
                "Келесі ➡️",
                use_container_width=True,
                type="primary",
            ):

                if (
                    question_index
                    < len(subject_questions) - 1
                ):

                    st.session_state.retry_question_idx += 1

                else:

                    st.session_state.retry_subject_idx += 1

                    st.session_state.retry_question_idx = 0

                st.rerun()


# =========================================================
# RETRY RESULT
# =========================================================

def render_retry_result():

    questions_data = (
        st.session_state.retry_questions
    )

    answers = (
        st.session_state.retry_answers
    )

    total = 0

    correct = 0

    for subject, subject_questions in (
        questions_data.items()
    ):

        for index, question in enumerate(
            subject_questions
        ):

            total += 1

            key = f"{subject}_{index}"

            selected = answers.get(
                key
            )

            if selected == question.get(
                "answer",
                0
            ):

                correct += 1

    percentage = 0

    if total > 0:

        percentage = round(
            correct / total * 100,
            1
        )

    st.markdown(
        "## 🔄 Қайта тапсыру нәтижесі"
    )

    st.markdown(
        f"""
        <div class="hero"
             style="text-align:center;">

            <div style="
                color:#A78BFA;
                font-size:13px;
                font-weight:850;
            ">
                ҚАЙТА ТАПСЫРУ
            </div>

            <div class="score-big"
                 style="margin-top:15px;">
                {correct} / {total}
            </div>

            <div style="
                font-size:22px;
                margin-top:10px;
                color:#A78BFA;
                font-weight:850;
            ">
                {percentage}%
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="font-size:25px;">
                    🟢
                </div>

                <div class="metric-number">
                    {correct}
                </div>

                <div class="metric-label">
                    Дұрыс
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="font-size:25px;">
                    🔴
                </div>

                <div class="metric-number">
                    {total - correct}
                </div>

                <div class="metric-label">
                    Қате
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-box">

                <div style="font-size:25px;">
                    📈
                </div>

                <div class="metric-number">
                    {percentage}%
                </div>

                <div class="metric-label">
                    Нәтиже
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "ℹ️ Қайта тапсыру нәтижесі негізгі 140 балдық статистикаға қосылмайды."
    )

    if st.button(
        "🏠 Басты бетке",
        use_container_width=True,
    ):

        st.session_state.page = "home"

        st.session_state.retry_mode = False

        st.session_state.retry_questions = {}

        st.session_state.retry_answers = {}

        st.session_state.retry_subject_idx = 0

        st.session_state.retry_question_idx = 0

        st.session_state.saved_result_id = None

        st.rerun()


# =========================================================
# MAIN
# =========================================================

if not st.session_state.logged_in:

    login_page()

else:

    if st.session_state.role == "admin":

        admin_page()

    elif st.session_state.role == "moderator":

        moderator_page()

    elif st.session_state.role == "user":

        if st.session_state.page == "retry_test":

            render_retry_test()

        else:

            user_page()

    else:

        st.error(
            "Белгісіз қолданушы рөлі."
        )
