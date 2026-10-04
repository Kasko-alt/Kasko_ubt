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
ADMIN_PASSWORD = os.environ.get("KASYM_ADMIN_PASSWORD", "CHANGE_ME")


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
    "Математикалық сауаттылық": 10,

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
        with open(USERS_FILE, "w", encoding="utf-8") as file:
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
            with open(USERS_FILE, "r", encoding="utf-8") as file:
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
                        "password": hash_password(ADMIN_PASSWORD),
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
            "username": st.session_state.get("username"),
            "full_name": st.session_state.get("full_name"),
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

    "pending_delete_question": None,
    "pending_user_delete": None,

    "retry_mode": False,
    "retry_questions": {},
    "retry_answers": {},
}


for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #172554 0%,
            #0B0F19 35%,
            #080B12 100%
        );
    color: white;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: white !important;
}

.kasym-title {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

.kasym-subtitle {
    font-size: 18px;
    color: #9CA3AF;
    margin-bottom: 25px;
}

.hero {
    padding: 35px;
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.22),
            rgba(15,23,42,0.92)
        );
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    margin-bottom: 25px;
}

.card {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.2);
}

.resume-card {
    background:
        linear-gradient(
            135deg,
            rgba(16,185,129,0.18),
            rgba(15,23,42,0.92)
        );
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 22px;
}

.score-big {
    font-size: 64px;
    font-weight: 900;
    line-height: 1;
}

.metric-box {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
}

.metric-number {
    font-size: 32px;
    font-weight: 800;
}

.metric-label {
    color: #94A3B8;
    font-size: 14px;
}

.question-box {
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
}

.question-text {
    font-size: 21px;
    font-weight: 700;
    line-height: 1.5;
}

.correct-box {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 14px;
    padding: 15px;
    margin-top: 10px;
}

.wrong-box {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 14px;
    padding: 15px;
    margin-top: 10px;
}

.unanswered-box {
    background: rgba(148,163,184,0.1);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 14px;
    padding: 15px;
    margin-top: 10px;
}

.info-box {
    padding: 18px;
    border-radius: 16px;
    background: rgba(37,99,235,0.12);
    border: 1px solid rgba(37,99,235,0.25);
    margin-bottom: 15px;
}

.warning-box {
    padding: 18px;
    border-radius: 16px;
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    margin-bottom: 15px;
}

[data-testid="stButton"] button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: 12px;
}

.stRadio label {
    font-size: 16px !important;
}

.palette-btn {
    text-align: center;
}

.login-container {
    max-width: 480px;
    margin: 7vh auto;
}

.login-card {
    background: rgba(15,23,42,0.92);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 25px;
    padding: 35px;
    box-shadow: 0 25px 80px rgba(0,0,0,0.45);
}

@media (max-width: 768px) {

    .block-container {
        padding: 1rem;
    }

    .kasym-title {
        font-size: 32px;
    }

    .kasym-subtitle {
        font-size: 15px;
    }

    .hero,
    .card,
    .question-box,
    .login-card {
        padding: 18px;
        border-radius: 16px;
    }

    .score-big {
        font-size: 48px;
    }

    .question-text {
        font-size: 18px;
    }
}

@media (max-width: 480px) {

    .kasym-title {
        font-size: 27px;
    }

    .metric-number {
        font-size: 24px;
    }

    .score-big {
        font-size: 40px;
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

    st.rerun()


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        """
        <div class="login-container">
            <div class="login-card">
                <div style="text-align:center;">
                    <div style="font-size:58px;">🎓</div>
                    <div class="kasym-title">KASYM EDU</div>
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
# STATISTICS HELPERS
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
        float(result.get("total_score", 0))
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
        st.info(
            "Әзірге тест нәтижелері жоқ."
        )
        return

    scores = [
        float(item.get("total_score", 0))
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

    st.markdown("### 📈 Тест тарихы")

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
                option_text = option_text[1:].strip()

            if option_text.startswith("(+)"):
                is_correct = True
                option_text = option_text[3:].strip()

            if "Дұрыс" in option_text:
                is_correct = True
                option_text = option_text.replace(
                    "Дұрыс",
                    ""
                ).strip()

            options.append(option_text)

            if is_correct:
                correct_index = len(options) - 1

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

        df = pd.read_excel(uploaded_file)

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
                        correct_index = number - 1

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

    col1, col2 = st.columns(
        [7, 1]
    )

    with col1:
        st.markdown(
            "## 🧑‍💼 Модератор панелі"
        )

    with col2:
        if st.button(
            "Шығу",
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

    # -----------------------------------------------------
    # ADD QUESTIONS
    # -----------------------------------------------------

    with tabs[0]:

        subject = st.selectbox(
            "Пән",
            all_subjects,
            key="moderator_subject_add",
        )

        st.markdown(
            """
            ### 📝 Бірден көп сұрақ енгізу

            Формат:

            1. Сұрақ мәтіні  
            A. Жауап  
            B. Жауап  
            C. *Дұрыс жауап  
            D. Жауап  

            Әр сұрақтың арасында бос жол болсын.
            """
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

                questions[subject].extend(parsed)

                save_questions(questions)

                st.success(
                    f"✅ {len(parsed)} сұрақ қосылды!"
                )

                st.rerun()

    # -----------------------------------------------------
    # EXCEL
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # DELETE QUESTIONS
    # -----------------------------------------------------

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

            st.info(
                "Бұл пәнде сұрақ жоқ."
            )

        else:

            question_options = [
                f"{index + 1}. {item.get('question', '')[:100]}"
                for index, item in enumerate(
                    subject_questions
                )
            ]

            selected_question = st.selectbox(
                "Сұрақ",
                question_options,
                key="question_to_delete",
            )

            selected_index = question_options.index(
                selected_question
            )

            question = subject_questions[
                selected_index
            ]

            st.markdown(
                f"""
                <div class="question-box">
                    <b>{question.get('question', '')}</b>
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
                    type="secondary",
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

    col1, col2 = st.columns(
        [7, 1]
    )

    with col1:
        st.markdown(
            "## 👑 Админ панелі"
        )

    with col2:

        if st.button(
            "Шығу",
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

            pending_user_delete = st.session_state.get(
                "pending_user_delete"
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

                        if pending_user_delete == u_username:

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

            username_clean = new_username.strip()

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

        with col1:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-number">
                        {total_users}
                    </div>
                    <div class="metric-label">
                        Қолданушы
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
                        {total_students}
                    </div>
                    <div class="metric-label">
                        Оқушы
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
                        {total_moderators}
                    </div>
                    <div class="metric-label">
                        Модератор
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-number">
                        {total_tests}
                    </div>
                    <div class="metric-label">
                        Тест саны
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

            user_stats = calculate_user_statistics(
                user.get("username")
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
    # TEST SCREEN
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
        ):
            st.session_state.page = "home"
            st.rerun()

        return

    # =====================================================
    # HOME
    # =====================================================

    col1, col2 = st.columns(
        [7, 1]
    )

    with col1:

        st.markdown(
            f"""
            <div class="kasym-title">
                KASYM EDU 🎓
            </div>
            <div class="kasym-subtitle">
                Бүгінгі дайындық — ертеңгі грант
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"### Сәлем, {st.session_state.full_name}! 👋"
        )

    with col2:

        if st.button(
            "Шығу",
            use_container_width=True,
        ):
            logout()

    # =====================================================
    # RESUME
    # =====================================================

    progress = load_test_progress()

    if (
        progress
        and progress.get("username")
        == username
        and progress.get("active_combination")
    ):

        st.markdown(
            """
            <div class="resume-card">
                <h3>🔄 Аяқталмаған тест бар</h3>
                <p>
                    Алдыңғы тестіңіз автоматты түрде сақталған.
                    Жалғастыра аласыз.
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

                st.rerun()

        with c2:

            if st.button(
                "🗑️ Аяқталмаған тестті өшіру",
                use_container_width=True,
            ):

                clear_test_progress()

                st.success(
                    "Сақталған тест өшірілді."
                )

                st.rerun()

    # =====================================================
    # CABINET
    # =====================================================

    stats = calculate_user_statistics(
        username
    )

    st.markdown(
        "## 👤 Жеке кабинет"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-number">
                    {stats["attempts"]}
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
                    {stats["best"]:.0f}
                </div>
                <div class="metric-label">
                    Үздік нәтиже / 140
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
        "📊 Менің аналитикам",
        use_container_width=True,
    ):

        st.session_state.page = "analytics"
        st.rerun()

    # =====================================================
    # NEW TEST
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

    st.markdown(
        "## 📝 Жаңа тест"
    )

    if not assigned_combination:

        st.warning(
            "Сізге ҰБТ бағыты әлі тағайындалмаған."
        )

        return

    st.markdown(
        f"""
        <div class="hero">
            <h2>🎯 {assigned_combination}</h2>
            <p>
                Бұл бағытта Қазақстан тарихы,
                Оқу сауаттылығы,
                Математикалық сауаттылық және
                екі бейіндік пән бар.
            </p>
            <p>
                <b>Жалпы максимум: 140 балл</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    combination_info = combinations.get(
        assigned_combination
    )

    if combination_info:

        st.markdown(
            "### 📚 Пәндер"
        )

        subjects = (
            combination_info["common"]
            + combination_info["pair"]
        )

        cols = st.columns(
            len(subjects)
        )

        for index, subject in enumerate(
            subjects
        ):

            with cols[index]:

                st.markdown(
                    f"""
                    <div class="card">
                        <h4>{subject}</h4>
                        <p>
                            {QUESTION_LIMITS.get(subject, 40)}
                            сұрақ
                        </p>
                        <p>
                            Макс:
                            {POINT_LIMITS.get(subject, 50)}
                            балл
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.button(
        "🚀 Тестті бастау",
        type="primary",
        use_container_width=True,
    ):

        clear_test_progress()

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
            "⬅️ Басты бетке"
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

    current_answer = st.session_state.test_answers.get(
        answer_key
    )

    # =====================================================
    # TOP
    # =====================================================

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            f"## 📚 {subject}"
        )

        st.caption(
            f"Сұрақ {question_index + 1} / {total_questions}"
        )

    with col2:

        if st.button(
            "Шығу",
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
    # QUESTION PALETTE
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
        index=radio_value if current_answer is not None else None,
        key=f"answer_radio_{subject}_{question_index}",
    )

    if selected_label:

        try:

            selected_index = radio_options.index(
                selected_label
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

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:10px;
                font-weight:700;
            ">
                {answered} / {total_all} жауап
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

                if question_index < total_questions - 1:

                    st.session_state.current_question_idx += 1

                else:

                    st.session_state.current_subject_idx += 1
                    st.session_state.current_question_idx = 0

                save_test_progress()

                st.rerun()


# =========================================================
# FINISH TEST
# =========================================================

def finish_test():

    st.session_state.test_started = False

    clear_test_progress()

    st.session_state.page = "result"

    st.rerun()


# =========================================================
# RESULT
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

        answers = st.session_state.test_answers

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

    existing_result_id = st.session_state.get(
        "saved_result_id"
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
        "combination": st.session_state.active_combination,
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

    st.session_state.saved_result_id = result_id


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
        <div class="hero" style="text-align:center;">
            <div style="color:#94A3B8;">
                Жалпы нәтиже
            </div>

            <div class="score-big">
                {result_data["total_score"]:.0f}
                /
                {result_data["total_possible"]}
            </div>

            <div style="font-size:20px;margin-top:10px;">
                {result_data["percentage"]}%
            </div>

            <div style="margin-top:15px;color:#CBD5E1;">
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
                <div class="metric-number">
                    🟢 {result_data["total_correct"]}
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
                <div class="metric-number">
                    🔴 {result_data["total_wrong"]}
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
                <div class="metric-number">
                    ⚪ {result_data["total_unanswered"]}
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
                <h3>{subject}</h3>
                <p>
                    🟢 Дұрыс: {data["correct"]}
                    &nbsp;&nbsp;
                    🔴 Қате: {data["wrong"]}
                    &nbsp;&nbsp;
                    ⚪ Жауапсыз: {data["unanswered"]}
                </p>
                <p>
                    <b>
                        Балл: {data["score"]:.0f}
                        / {data["max_score"]}
                    </b>
                </p>
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
                    f"**{index + 1}. {question.get('question', '')}**"
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
                            {options[correct]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="wrong-box">
                            🔴 Сенің жауабың:
                            {options[selected]}
                            <br><br>
                            🟢 Дұрыс жауап:
                            {options[correct]}
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

    subject_index = st.session_state.get(
        "retry_subject_idx",
        0
    )

    question_index = st.session_state.get(
        "retry_question_idx",
        0
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

    st.markdown(
        "## 🔄 Қате сұрақтарды қайталау"
    )

    st.caption(
        f"{subject} — "
        f"{question_index + 1} / "
        f"{len(subject_questions)}"
    )

    st.markdown(
        f"""
        <div class="question-box">
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
    ]

    selected = st.radio(
        "Жауап:",
        radio_options,
        index=current_answer
        if current_answer is not None
        else None,
        key=f"retry_radio_{subject}_{question_index}",
    )

    if selected:

        selected_index = radio_options.index(
            selected
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

    for subject, subject_questions in questions_data.items():

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
        <div class="hero" style="text-align:center;">
            <div class="score-big">
                {correct} / {total}
            </div>

            <div style="font-size:22px;margin-top:10px;">
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
                <div class="metric-number">
                    🟢 {correct}
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
                <div class="metric-number">
                    🔴 {total - correct}
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

        if st.session_state.page == "home":
            moderator_page()
        else:
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
