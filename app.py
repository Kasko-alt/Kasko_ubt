import datetime
import hashlib
import json
import os
import random
import re

import pandas as pd
import streamlit as st


# =========================================================
# 1. КОНФИГУРАЦИЯ
# =========================================================

st.set_page_config(
    page_title="KASYM EDU - Білім беру платформасы",
    page_icon="🎓",
    layout="wide"
)

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"
TEST_PROGRESS_FILE = "test_progress.json"

# users.json бар болса, оның ішіндегі пароль өзгермейді.
# Жаңа users.json жасалған кезде ғана осы пароль қолданылады.
ADMIN_PASSWORD = os.environ.get(
    "KASYM_ADMIN_PASSWORD",
    "CHANGE_ME"
)


# =========================================================
# 2. ҚАУІПСІЗДІК
# =========================================================

def hash_password(password: str) -> str:
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# 3. ПӘНДЕР
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


subject_limits = {
    "Қазақстан тарихы": 20,
    "Оқу сауаттылығы": 10,
    "Математикалық сауаттылық": 10,
    "Математика": 40,
    "Физика": 40,
    "Химия": 40,
    "Биология": 40,
    "Информатика": 40,
    "География": 40,
    "Дүниежүзі тарихы": 40,
    "Ағылшын тілі": 40,
    "Құқық": 40,
}


# =========================================================
# КОМБИНАЦИЯЛАР
# =========================================================

combinations = {

    "Математика - Физика (Инженерлік)": [
        "Математика",
        "Физика",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],

    "Биология - Химия (Медицина)": [
        "Биология",
        "Химия",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],

    "География - Математика (Геодезия/Экономика)": [
        "География",
        "Математика",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],

    "Дүниежүзі тарихы - Ағылшын (Халықаралық)": [
        "Дүниежүзі тарихы",
        "Ағылшын тілі",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],

    "Математика - Информатика (IT / Бағдарламалау)": [
        "Математика",
        "Информатика",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],

    "Құқық - Дүниежүзі тарихы (Юриспруденция)": [
        "Құқық",
        "Дүниежүзі тарихы",
        "Қазақстан тарихы",
        "Оқу сауаттылығы",
        "Математикалық сауаттылық",
    ],
}


# =========================================================
# 4. БАСТАПҚЫ СҰРАҚТАР
# =========================================================

default_questions = {

    "Қазақстан тарихы": [
        {
            "question": "«Ұлы шаньюй» деп аталған тайпа көсемі:",
            "answers": [
                "қаңлыларда",
                "үйсіндерде",
                "ғұндарда",
                "сақтарда"
            ],
            "correct": 2,
            "topic": "Ежелгі Қазақстан",
        },
        {
            "question": "Қазақ хандығы қашан құрылды?",
            "answers": [
                "1465-1466 жж.",
                "1729 ж.",
                "1841 ж.",
                "1916 ж."
            ],
            "correct": 0,
            "topic": "Қазақ хандығы",
        },
    ],

    "Биология": [
        {
            "question": "Фотосинтез процесі қай органоидта жүреді?",
            "answers": [
                "Митохондрия",
                "Хлоропласт",
                "Рибосома",
                "Лизосома"
            ],
            "correct": 1,
            "topic": "Жасуша",
        }
    ],

    "Математика": [
        {
            "question": "Егер x + 5 = 12 болса, x неге тең?",
            "answers": [
                "5",
                "7",
                "12",
                "17"
            ],
            "correct": 1,
            "topic": "Теңдеулер",
        }
    ],

    "Физика": [
        {
            "question": "Жылдамдықтың өлшем бірлігі:",
            "answers": [
                "м/с",
                "кг",
                "Н",
                "Вт"
            ],
            "correct": 0,
            "topic": "Механика",
        }
    ],

    "Оқу сауаттылығы": [
        {
            "question": "Мәтіннің негізгі ойын анықтаңыз: «Еңбек — ерлікке жеткізер»",
            "answers": [
                "Балмұздақ жеу",
                "Еңбектің маңызы",
                "Спортпен шұғылдану",
                "Саяхат"
            ],
            "correct": 1,
            "topic": "Мәтінді түсіну",
        }
    ],

    "Математикалық сауаттылық": [
        {
            "question": "20 санының 20%-ын табыңыз:",
            "answers": [
                "2",
                "4",
                "5",
                "10"
            ],
            "correct": 1,
            "topic": "Пайыз",
        }
    ],
}


# =========================================================
# 5. USERS
# =========================================================

def default_users():

    return [
        {
            "username": "kas01",
            "password": hash_password(
                ADMIN_PASSWORD
            ),
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

    # =====================================================
    # users.json бар болса —
    # оның ішіндегі парольдерге тимейміз.
    # =====================================================

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

                    if user.get("username") == "kas01":

                        user["role"] = "admin"
                        admin_found = True

                # Парольді қайта жазбаймыз!
                if admin_found:

                    return data

                # kas01 жоқ болса ғана жаңадан қосамыз.
                data.append({
                    "username": "kas01",
                    "password": hash_password(
                        ADMIN_PASSWORD
                    ),
                    "name": "KASYM",
                    "role": "admin",
                    "combination": None,
                })

                save_users(data)

                return data

        except Exception:

            # Файл бұзылған болса,
            # төменде жаңа users.json жасалады.
            pass

    # users.json мүлдем жоқ
    data = default_users()

    save_users(data)

    return data


users = load_users()


def find_user(username, password):

    username = (username or "").strip()

    # Парольді strip жасамаймыз.
    # Себебі парольдің ішінде бос орын болуы мүмкін.
    password = password or ""

    if not username or not password:
        return None

    hashed_input = hash_password(
        password
    )

    for user in users:

        if user.get("username") != username:
            continue

        stored_password = str(
            user.get(
                "password",
                ""
            )
        ).strip()

        # SHA-256 арқылы сақталған пароль
        if stored_password == hashed_input:

            return user

        # Ескі users.json ішінде
        # пароль жай мәтін болып қалса,
        # соны да оқуға мүмкіндік береміз.
        if stored_password == password:

            return user

    return None


def username_exists(username):

    username = (username or "").strip()

    return any(
        user.get("username") == username
        for user in users
    )


# =========================================================
# 6. QUESTIONS
# =========================================================

def load_questions():

    if os.path.exists(QUESTIONS_FILE):

        try:

            with open(
                QUESTIONS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):

                data = {}

            for subject in all_subjects:

                if subject not in data:

                    data[subject] = (
                        default_questions.get(
                            subject,
                            []
                        )
                    )

            return data

        except Exception:

            return default_questions.copy()

    return default_questions.copy()


def save_questions():

    with open(
        QUESTIONS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            questions,
            file,
            ensure_ascii=False,
            indent=4
        )


questions = load_questions()


# =========================================================
# 7. RESULTS
# =========================================================

def load_results_history():

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


def save_results_history(history):

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================================================
# 8. TEST PROGRESS
# =========================================================

def load_all_test_progress():

    if not os.path.exists(
        TEST_PROGRESS_FILE
    ):

        return {}

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


def save_all_test_progress(data):

    try:

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


def get_test_progress(username):

    if not username:

        return None

    all_progress = (
        load_all_test_progress()
    )

    return all_progress.get(
        username
    )


def clear_test_progress(username):

    if not username:

        return

    all_progress = (
        load_all_test_progress()
    )

    if username in all_progress:

        del all_progress[username]

        save_all_test_progress(
            all_progress
        )


def normalize_test_answers(raw_answers):

    result = {}

    if not isinstance(
        raw_answers,
        dict
    ):

        return result

    for subject, answers in raw_answers.items():

        if not isinstance(
            answers,
            dict
        ):

            result[subject] = {}
            continue

        result[subject] = {}

        for q_index, answer_index in answers.items():

            try:

                result[subject][
                    int(q_index)
                ] = int(
                    answer_index
                )

            except Exception:

                pass

    return result


def save_current_test_progress():

    username = st.session_state.get(
        "username",
        ""
    )

    if not username:

        return

    if not st.session_state.get(
        "test_started",
        False
    ):

        return

    progress = {
        "active_combination": (
            st.session_state.get(
                "active_combination"
            )
        ),

        "current_subject_index": (
            st.session_state.get(
                "current_subject_index",
                0
            )
        ),

        "current_question_index": (
            st.session_state.get(
                "current_question_index",
                0
            )
        ),

        "test_answers": (
            st.session_state.get(
                "test_answers",
                {}
            )
        ),

        "shuffled_test_data": (
            st.session_state.get(
                "shuffled_test_data",
                {}
            )
        ),

        "retry_mode": (
            st.session_state.get(
                "retry_mode",
                False
            )
        ),

        "retry_data": (
            st.session_state.get(
                "retry_data",
                {}
            )
        ),

        "saved_at": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }

    all_progress = (
        load_all_test_progress()
    )

    all_progress[username] = progress

    save_all_test_progress(
        all_progress
    )


def restore_test_progress(progress):

    if not progress:

        return False

    try:

        st.session_state.active_combination = (
            progress.get(
                "active_combination"
            )
        )

        st.session_state.current_subject_index = int(
            progress.get(
                "current_subject_index",
                0
            )
        )

        st.session_state.current_question_index = int(
            progress.get(
                "current_question_index",
                0
            )
        )

        st.session_state.test_answers = (
            normalize_test_answers(
                progress.get(
                    "test_answers",
                    {}
                )
            )
        )

        st.session_state.shuffled_test_data = (
            progress.get(
                "shuffled_test_data",
                {}
            )
        )

        st.session_state.retry_mode = bool(
            progress.get(
                "retry_mode",
                False
            )
        )

        st.session_state.retry_data = (
            progress.get(
                "retry_data",
                {}
            )
        )

        st.session_state.test_started = True
        st.session_state.result_saved = False

        return True

    except Exception:

        return False


# =========================================================
# 9. SESSION STATE
# =========================================================

session_defaults = {

    "logged_in": False,

    "role": None,

    "username": "",

    "full_name": "",

    "test_started": False,

    "active_combination": None,

    "current_subject_index": 0,

    "current_question_index": 0,

    "test_answers": {},

    "shuffled_test_data": {},

    "current_subject_results": [],

    "result_saved": False,

    "retry_mode": False,

    "retry_data": {},

    "retry_results": {},

    "pending_delete_question": None,

    "resume_checked": False,
}


for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# 10. DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
        font-family: 'Inter', sans-serif;
    }

    .kasym-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;

        background: linear-gradient(
            135deg,
            #6366F1 0%,
            #A855F7 100%
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 0px;
    }

    .kasym-subtitle {
        font-size: 16px;
        text-align: center;
        color: #9CA3AF;
        margin-bottom: 30px;
        font-weight: 500;
    }

    .card {
        background: linear-gradient(
            145deg,
            #1E293B 0%,
            #0F172A 100%
        );

        padding: 24px;

        border-radius: 16px;

        border: 1px solid
        rgba(255,255,255,0.08);

        box-shadow:
            0 10px 25px -5px
            rgba(0,0,0,0.3);

        margin-bottom: 20px;
    }

    .stButton > button {

        border-radius: 8px;

        font-weight: 700;

        font-size: 15px !important;

        border: 1px solid
        rgba(255,255,255,0.15);

        background-color: #1E293B;

        color: #FFFFFF !important;

        transition: all 0.2s ease;

        padding: 4px 8px;

        min-height: 42px;
    }

    .stButton > button:hover {

        border-color: #6366F1;

        background-color: #312E81;

        color: #FFFFFF !important;

        transform: translateY(-1px);
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {

        background-color: #1E293B !important;

        border-radius: 10px !important;

        color: #F3F4F6 !important;

        border: 1px solid
        rgba(255,255,255,0.08) !important;
    }

    .nav-legend {

        background: #111827;

        padding: 10px 14px;

        border-radius: 10px;

        margin-bottom: 12px;

        text-align: center;

        font-size: 14px;
    }

    .analytics-good {

        color: #22C55E;

        font-weight: 700;
    }

    .analytics-bad {

        color: #EF4444;

        font-weight: 700;
    }

    .resume-box {

        background: linear-gradient(
            145deg,
            #172554,
            #1E1B4B
        );

        border: 1px solid
        rgba(99,102,241,0.35);

        border-radius: 16px;

        padding: 20px;

        margin-bottom: 20px;
    }

    .score-big {

        font-size: 48px;

        font-weight: 800;

        text-align: center;

        margin: 5px 0;
    }

    .score-label {

        text-align: center;

        color: #9CA3AF;

        font-size: 14px;
    }

    @media (max-width: 768px) {

        .kasym-title {

            font-size: 30px !important;

        }

        .kasym-subtitle {

            font-size: 13px !important;

            margin-bottom: 18px !important;

        }

        .card {

            padding: 14px !important;

            border-radius: 12px !important;

        }

        .stButton > button {

            min-height: 46px !important;

            font-size: 13px !important;

        }

        .stRadio label {

            font-size: 15px !important;

        }

        .nav-legend {

            font-size: 11px !important;

            padding: 9px 5px !important;

        }

        .score-big {

            font-size: 36px !important;

        }

        [data-testid="stHorizontalBlock"] {

            gap: 0.35rem !important;

        }

    }

    @media (max-width: 480px) {

        .kasym-title {

            font-size: 27px !important;

        }

        .kasym-subtitle {

            font-size: 12px !important;

        }

        .stMarkdown {

            font-size: 14px;

        }

        .stRadio label {

            font-size: 14px !important;

        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 11. LOGOUT
# =========================================================

def logout():

    # Егер тест аяқталмаған болса,
    # автоматты түрде сақтаймыз.
    if st.session_state.get(
        "test_started",
        False
    ):

        save_current_test_progress()

    for key, value in session_defaults.items():

        st.session_state[key] = value

    st.rerun()


# =========================================================
# 12. LOGIN
# =========================================================

def login_page():

    st.markdown(
        '<div class="kasym-title">KASYM EDU</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="kasym-subtitle">'
        'Бүгінгі дайындық — ертеңгі грант'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(
        [1, 1.2, 1]
    )

    with c2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🔐 Жүйеге кіру"
        )

        username = st.text_input(
            "Логин",
            key="login_username"
        )

        password = st.text_input(
            "Құпия сөз",
            type="password",
            key="login_password"
        )

        if st.button(
            "Кіру →",
            use_container_width=True,
            type="primary"
        ):

            # Парольді strip жасамай береміз.
            user = find_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = (
                    user["username"]
                )

                st.session_state.full_name = (
                    user.get(
                        "name",
                        ""
                    )
                )

                st.session_state.role = (
                    user.get(
                        "role",
                        "user"
                    )
                )

                st.rerun()

            else:

                st.error(
                    "❌ Логин немесе құпия сөз қате."
                )

        st.info(
            "🔐 Жаңа аккаунтты тек администратор жасайды."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 13. СТАТИСТИКА
# =========================================================

def render_statistics_tab():

    st.markdown(
        "### 📊 Оқушылардың тест нәтижелері мен статистикасы"
    )

    history = load_results_history()

    if not history:

        st.info(
            "⚠️ Әзірге ешбір оқушы тест тапсырған жоқ."
        )

        return

    total_tests = len(history)

    normal_tests = [
        h for h in history
        if h.get(
            "test_type",
            "normal"
        ) == "normal"
    ]

    avg_score = (
        sum(
            int(
                h.get(
                    "score",
                    0
                ) or 0
            )
            for h in normal_tests
        )
        / len(normal_tests)
        if normal_tests
        else 0
    )

    col_m1, col_m2 = st.columns(2)

    with col_m1:

        st.metric(
            "📈 Барлық тапсырылған тесттер",
            total_tests
        )

    with col_m2:

        st.metric(
            "⭐ Орташа ұпай",
            f"{avg_score:.1f}"
        )

    st.markdown("---")

    sc1, sc2 = st.columns(2)

    with sc1:

        search_query = (
            st.text_input(
                "🔍 Оқушының аты немесе логині бойынша іздеу:",
                key="stat_search"
            )
            .strip()
            .lower()
        )

    with sc2:

        comb_filter = st.selectbox(
            "🎯 Комбинация бойынша сүзу:",
            ["Барлығы"] + list(
                combinations.keys()
            ),
            key="stat_comb_filter"
        )

    filtered_history = []

    for h in history:

        name = h.get(
            "name",
            "Аты жоқ"
        )

        uname = h.get(
            "username",
            "белгісіз"
        )

        comb = h.get(
            "combination",
            "Көрсетілмеген"
        )

        score = h.get(
            "score",
            0
        )

        date = h.get(
            "date",
            "Уақыты белгісіз"
        )

        match_search = (
            search_query in name.lower()
            or search_query in uname.lower()
        )

        match_comb = (
            comb_filter == "Барлығы"
            or comb == comb_filter
        )

        if match_search and match_comb:

            filtered_history.append({
                "Аты-жөні": name,
                "Логин": f"@{uname}",
                "Комбинация": comb,
                "Ұпай": score,
                "Түрі": (
                    "Қайта тапсыру"
                    if h.get(
                        "test_type"
                    ) == "retry"
                    else "Негізгі тест"
                ),
                "Күні": date,
            })

    st.caption(
        f"Табылған нәтижелер саны: "
        f"{len(filtered_history)}"
    )

    if not filtered_history:

        st.warning(
            "⚠️ Іздеу шарттарына сәйкес нәтиже табылмады."
        )

    else:

        st.dataframe(
            filtered_history,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 14. ANALYTICS
# =========================================================

def render_analytics(username=None):

    history = load_results_history()

    if username:

        history = [
            h for h in history
            if h.get(
                "username"
            ) == username
        ]

    history = [
        h for h in history
        if h.get(
            "test_type",
            "normal"
        ) == "normal"
    ]

    st.markdown(
        "### 📊 Пәндер бойынша аналитика"
    )

    if not history:

        st.info(
            "Аналитика жасау үшін алдымен тест тапсыру керек."
        )

        return

    subject_stats = {}

    for result in history:

        for item in result.get(
            "subject_results",
            []
        ):

            subject = item.get(
                "subject",
                "Белгісіз"
            )

            correct = int(
                item.get(
                    "correct",
                    0
                )
            )

            total = int(
                item.get(
                    "questions",
                    0
                )
            )

            if subject not in subject_stats:

                subject_stats[subject] = {
                    "correct": 0,
                    "total": 0,
                    "attempts": 0
                }

            subject_stats[subject][
                "correct"
            ] += correct

            subject_stats[subject][
                "total"
            ] += total

            subject_stats[subject][
                "attempts"
            ] += 1

    analytics_data = []

    for subject, data in subject_stats.items():

        percentage = (
            data["correct"]
            / data["total"]
            * 100
            if data["total"]
            else 0
        )

        analytics_data.append({
            "Пән": subject,
            "Дұрыс": data["correct"],
            "Барлық сұрақ": data["total"],
            "Дәлдік": round(
                percentage,
                1
            ),
            "Тест саны": data["attempts"]
        })

    analytics_data.sort(
        key=lambda x: x["Дәлдік"]
    )

    if analytics_data:

        weakest = analytics_data[0]
        strongest = analytics_data[-1]

        col1, col2 = st.columns(2)

        with col1:

            st.error(
                f"🔴 Әлсіз пән: "
                f"**{weakest['Пән']}** — "
                f"{weakest['Дәлдік']}%"
            )

        with col2:

            st.success(
                f"🟢 Күшті пән: "
                f"**{strongest['Пән']}** — "
                f"{strongest['Дәлдік']}%"
            )

        st.markdown("---")

        chart_data = pd.DataFrame(
            analytics_data
        ).set_index(
            "Пән"
        )

        st.bar_chart(
            chart_data["Дәлдік"]
        )

        st.dataframe(
            analytics_data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 15. BULK PARSER
# =========================================================

def parse_bulk_questions(raw_text):

    questions_list = []

    blocks = re.split(
        r"(?=\b\d+[\.\)]\s)",
        raw_text
    )

    for block in blocks:

        if not block.strip():
            continue

        full_text = " ".join(
            block.strip().split("\n")
        )

        q_match = re.search(
            r"^\d+[\.\)]\s*(.*?)(?=[A-DА-Гa-dа-г][\.\)]|\bЖауабы:|$)",
            full_text
        )

        if not q_match:
            continue

        q_text = q_match.group(
            1
        ).strip()

        options = re.findall(
            r"([A-DА-Гa-dа-г])[\.\)]\s*"
            r"([^A-DА-Гa-dа-г\.\)]+)",
            full_text
        )

        answers = []

        if len(options) >= 4:

            answers = [
                opt[1].strip()
                for opt in options[:4]
            ]

        correct_index = 0

        ans_match = re.search(
            r"Жауабы:\s*([A-DА-Гa-dа-г])",
            full_text,
            re.IGNORECASE
        )

        if ans_match:

            corr_letter = (
                ans_match.group(
                    1
                ).upper()
            )

            letter_map = {
                "A": 0,
                "А": 0,
                "B": 1,
                "Б": 1,
                "C": 2,
                "В": 2,
                "D": 3,
                "Г": 3,
            }

            correct_index = letter_map.get(
                corr_letter,
                0
            )

        topic_match = re.search(
            r"Тақырыбы:\s*(.*?)(?=\s+(?:Жауабы:)|$)",
            full_text,
            re.IGNORECASE
        )

        topic = (
            topic_match.group(
                1
            ).strip()
            if topic_match
            else "Жалпы"
        )

        if len(answers) >= 4:

            questions_list.append({
                "question": q_text,
                "answers": answers[:4],
                "correct": correct_index,
                "topic": topic,
            })

    return questions_list


# =========================================================
# 16. EXCEL
# =========================================================

def normalize_column_name(name):

    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def find_excel_column(
    columns,
    possible_names
):

    normalized = {
        normalize_column_name(c): c
        for c in columns
    }

    for name in possible_names:

        key = normalize_column_name(
            name
        )

        if key in normalized:

            return normalized[key]

    return None


def parse_correct_answer(
    value,
    answers
):

    if pd.isna(value):

        return None

    text = str(
        value
    ).strip()

    letter_map = {
        "A": 0,
        "А": 0,
        "B": 1,
        "Б": 1,
        "C": 2,
        "В": 2,
        "D": 3,
        "Г": 3,
    }

    upper = text.upper()

    if upper in letter_map:

        return letter_map[
            upper
        ]

    if text in [
        "1",
        "2",
        "3",
        "4"
    ]:

        return int(text) - 1

    for index, answer in enumerate(
        answers
    ):

        if text == str(
            answer
        ).strip():

            return index

    return None


def import_excel_questions(df):

    question_col = find_excel_column(
        df.columns,
        [
            "Сұрақ",
            "Сұрақ мәтіні",
            "question",
            "questiontext"
        ]
    )

    a_col = find_excel_column(
        df.columns,
        [
            "А",
            "A",
            "A нұсқасы",
            "answerA"
        ]
    )

    b_col = find_excel_column(
        df.columns,
        [
            "Б",
            "B",
            "Б нұсқасы",
            "answerB"
        ]
    )

    c_col = find_excel_column(
        df.columns,
        [
            "В",
            "C",
            "В нұсқасы",
            "answerC"
        ]
    )

    d_col = find_excel_column(
        df.columns,
        [
            "Г",
            "D",
            "Г нұсқасы",
            "answerD"
        ]
    )

    correct_col = find_excel_column(
        df.columns,
        [
            "Дұрыс жауап",
            "Дұрыс",
            "Жауап",
            "Correct",
            "CorrectAnswer"
        ]
    )

    topic_col = find_excel_column(
        df.columns,
        [
            "Тақырып",
            "Тақырыбы",
            "Topic"
        ]
    )

    required = [
        question_col,
        a_col,
        b_col,
        c_col,
        d_col,
        correct_col
    ]

    if any(
        col is None
        for col in required
    ):

        return [], (
            "Excel бағандары дұрыс емес. "
            "Керек бағандар: "
            "Сұрақ, А, Б, В, Г, Дұрыс жауап."
        )

    result = []
    errors = []

    for index, row in df.iterrows():

        question_text = str(
            row[question_col]
        ).strip()

        answers = [
            str(
                row[a_col]
            ).strip(),

            str(
                row[b_col]
            ).strip(),

            str(
                row[c_col]
            ).strip(),

            str(
                row[d_col]
            ).strip(),
        ]

        if (
            not question_text
            or any(
                x == ""
                or x.lower() == "nan"
                for x in answers
            )
        ):

            errors.append(
                f"{index + 2}-жол: "
                "сұрақ немесе жауап бос."
            )

            continue

        correct = parse_correct_answer(
            row[correct_col],
            answers
        )

        if correct is None:

            errors.append(
                f"{index + 2}-жол: "
                "дұрыс жауап анықталмады."
            )

            continue

        topic = "Жалпы"

        if topic_col:

            raw_topic = row[
                topic_col
            ]

            if not pd.isna(
                raw_topic
            ):

                topic = str(
                    raw_topic
                ).strip() or "Жалпы"

        result.append({
            "question": question_text,
            "answers": answers,
            "correct": correct,
            "topic": topic,
        })

    return result, errors


# =========================================================
# 17. MODERATOR
# =========================================================

def moderator_page():

    if (
        not st.session_state.get(
            "logged_in"
        )
        or st.session_state.get(
            "role"
        ) not in (
            "moderator",
            "admin"
        )
    ):

        st.error(
            "⛔ Бұл бөлімге кіруге рұқсатыңыз жоқ."
        )

        st.stop()

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            '<div class="kasym-title" '
            'style="font-size:32px;">'
            '🛠️ Модератор панелі'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        if st.button(
            "🚪 Шығу",
            use_container_width=True
        ):

            logout()

    st.markdown(
        '<div class="kasym-subtitle">'
        'Сұрақтар базасы және оқушылар статистикасы'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚡ Массалық жүктеу",
        "📥 Excel импорт",
        "✍️ Жеке сұрақ қосу",
        "🗑️ Сұрақтарды жою",
        "📊 Статистика",
    ])


    # =====================================================
    # TAB 1
    # =====================================================

    with tab1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        sel_sub_bulk = st.selectbox(
            "📚 Пәнді таңдаңыз:",
            all_subjects,
            key="mod_bulk_sub"
        )

        raw_text = st.text_area(
            "Сұрақтарды осында көшіріп қойыңыз:",
            height=250
        )

        st.caption(
            "Мысал: 1. Сұрақ? А) ... Б) ... "
            "В) ... Г) ... Жауабы: А"
        )

        if st.button(
            "🚀 Жүктеу",
            type="primary"
        ):

            if raw_text.strip():

                parsed = parse_bulk_questions(
                    raw_text
                )

                if parsed:

                    if sel_sub_bulk not in questions:

                        questions[
                            sel_sub_bulk
                        ] = []

                    questions[
                        sel_sub_bulk
                    ].extend(
                        parsed
                    )

                    save_questions()

                    st.success(
                        f"✨ {len(parsed)} "
                        "сұрақ қосылды."
                    )

                else:

                    st.error(
                        "⚠️ Формат қате."
                    )

            else:

                st.warning(
                    "Өріс бос."
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📥 Excel арқылы сұрақтарды жүктеу"
        )

        st.info(
            "Excel файлында мына бағандар болуы керек: "
            "**Сұрақ | А | Б | В | Г | Дұрыс жауап**. "
            "Қосымша **Тақырып** бағанын қосуға болады."
        )

        excel_subject = st.selectbox(
            "📚 Қай пәнге импорттаймыз?",
            all_subjects,
            key="excel_subject"
        )

        uploaded_file = st.file_uploader(
            "Excel файлын таңдаңыз (.xlsx)",
            type=["xlsx"],
            key="excel_uploader"
        )

        if uploaded_file:

            try:

                df = pd.read_excel(
                    uploaded_file
                )

                st.markdown(
                    "#### 👀 Алдын ала көру"
                )

                st.dataframe(
                    df.head(10),
                    use_container_width=True,
                    hide_index=True
                )

                imported_questions, import_errors = (
                    import_excel_questions(df)
                )

                if imported_questions:

                    st.success(
                        f"Дайын сұрақтар: "
                        f"{len(imported_questions)}"
                    )

                if import_errors:

                    st.warning(
                        f"Қате жолдар: "
                        f"{len(import_errors)}"
                    )

                    with st.expander(
                        "Қате жолдарды көру"
                    ):

                        for error in import_errors:

                            st.write(
                                "⚠️",
                                error
                            )

                if st.button(
                    "📥 Excel сұрақтарын сақтау",
                    type="primary",
                    key="save_excel_questions"
                ):

                    if imported_questions:

                        if excel_subject not in questions:

                            questions[
                                excel_subject
                            ] = []

                        questions[
                            excel_subject
                        ].extend(
                            imported_questions
                        )

                        save_questions()

                        st.success(
                            f"✨ "
                            f"{len(imported_questions)} "
                            "сұрақ сәтті қосылды!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Сақтайтын сұрақ табылмады."
                        )

            except Exception as error:

                st.error(
                    "Excel файлын оқу кезінде қате шықты."
                )

                st.code(
                    str(error)
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 3
    # =====================================================

    with tab3:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        sel_sub_single = st.selectbox(
            "📚 Пәнді таңдаңыз:",
            all_subjects,
            key="mod_single_sub"
        )

        q_text = st.text_area(
            "Сұрақ мәтіні:"
        )

        topic = st.text_input(
            "📚 Тақырып:",
            placeholder="Мысалы: Теңдеулер"
        )

        c1, c2 = st.columns(2)

        with c1:

            a1 = st.text_input(
                "А нұсқасы:"
            )

            a3 = st.text_input(
                "В нұсқасы:"
            )

        with c2:

            a2 = st.text_input(
                "Б нұсқасы:"
            )

            a4 = st.text_input(
                "Г нұсқасы:"
            )

        corr = st.selectbox(
            "Дұрыс жауап:",
            [
                "А нұсқасы",
                "Б нұсқасы",
                "В нұсқасы",
                "Г нұсқасы"
            ]
        )

        corr_idx = [
            "А нұсқасы",
            "Б нұсқасы",
            "В нұсқасы",
            "Г нұсқасы"
        ].index(
            corr
        )

        if st.button(
            "💾 Сақтау",
            type="primary"
        ):

            if (
                q_text
                and a1
                and a2
                and a3
                and a4
            ):

                if sel_sub_single not in questions:

                    questions[
                        sel_sub_single
                    ] = []

                questions[
                    sel_sub_single
                ].append({

                    "question": q_text,

                    "answers": [
                        a1,
                        a2,
                        a3,
                        a4
                    ],

                    "correct": corr_idx,

                    "topic": (
                        topic.strip()
                        or "Жалпы"
                    ),
                })

                save_questions()

                st.success(
                    "✨ Сұрақ сақталды!"
                )

                st.rerun()

            else:

                st.error(
                    "Барлық өрістерді толтырыңыз!"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 4
    # =====================================================

    with tab4:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        del_sub = st.selectbox(
            "📚 Пәнді таңдаңыз:",
            all_subjects,
            key="mod_del_sub"
        )

        sub_list = questions.get(
            del_sub,
            []
        )

        if not sub_list:

            st.info(
                "Бұл пәнде сұрақтар жоқ."
            )

        else:

            q_map = {
                f"{i+1}. {q.get('question', '')[:60]}...": i
                for i, q in enumerate(
                    sub_list
                )
            }

            chosen_q = st.selectbox(
                "Жою үшін сұрақты таңдаңыз:",
                list(
                    q_map.keys()
                ),
                key="delete_question_select"
            )

            chosen_index = q_map[
                chosen_q
            ]

            st.markdown("---")

            pending = (
                st.session_state.get(
                    "pending_delete_question"
                )
            )

            if (
                pending
                and pending.get(
                    "subject"
                ) == del_sub
                and pending.get(
                    "index"
                ) == chosen_index
            ):

                st.warning(
                    "⚠️ Бұл сұрақты шынымен өшіргіңіз келе ме?"
                )

                confirm_col1, confirm_col2 = st.columns(2)

                with confirm_col1:

                    if st.button(
                        "✅ Иә, өшіру",
                        type="primary",
                        use_container_width=True,
                        key="confirm_delete"
                    ):

                        sub_list.pop(
                            chosen_index
                        )

                        questions[
                            del_sub
                        ] = sub_list

                        save_questions()

                        st.session_state.pending_delete_question = None

                        st.success(
                            "🗑️ Сұрақ өшірілді."
                        )

                        st.rerun()

                with confirm_col2:

                    if st.button(
                        "❌ Болдырмау",
                        use_container_width=True,
                        key="cancel_delete"
                    ):

                        st.session_state.pending_delete_question = None

                        st.rerun()

            else:

                if st.button(
                    "🗑️ Жою",
                    type="primary",
                    key="delete_question_start"
                ):

                    st.session_state.pending_delete_question = {

                        "subject": del_sub,

                        "index": chosen_index
                    }

                    st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # TAB 5
    # =====================================================

    with tab5:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        render_statistics_tab()

        st.markdown("---")

        render_analytics()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 18. ADMIN
# =========================================================

def admin_page():

    if (
        not st.session_state.get(
            "logged_in"
        )
        or st.session_state.get(
            "role"
        ) != "admin"
    ):

        st.error(
            "⛔ Администратор бөліміне кіруге рұқсатыңыз жоқ."
        )

        st.stop()

    global users

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            '<div class="kasym-title" '
            'style="font-size:32px;">'
            '👑 Администратор панелі'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        if st.button(
            "🚪 Шығу",
            use_container_width=True
        ):

            logout()

    st.markdown(
        '<div class="kasym-subtitle">'
        'Қолданушыларды басқару және статистика'
        '</div>',
        unsafe_allow_html=True
    )

    admin_tabs = st.tabs([
        "👥 Қолданушылар",
        "➕ Жаңа қолданушы",
        "📊 Статистика",
    ])


    # =====================================================
    # USERS
    # =====================================================

    with admin_tabs[0]:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📋 Тіркелген қолданушылар"
        )

        for u in list(users):

            u_name = u.get(
                "name",
                "Аты жоқ"
            )

            u_username = u.get(
                "username"
            )

            u_role = u.get(
                "role"
            )

            current_combination = u.get(
                "combination"
            )

            st.markdown(
                f"**{u_name}** · "
                f"`@{u_username}` · "
                f"Рөлі: `{u_role}`"
            )

            if u_role == "user":

                comb_options = list(
                    combinations.keys()
                )

                current_index = (
                    comb_options.index(
                        current_combination
                    )
                    if current_combination
                    in comb_options
                    else 0
                )

                col_comb, col_save, col_del = st.columns(
                    [4, 1.2, 1.2]
                )

                with col_comb:

                    selected_combination = st.selectbox(
                        "🎯 Бекітілген комбинация",
                        comb_options,
                        index=current_index,
                        key=f"user_comb_{u_username}"
                    )

                with col_save:

                    st.write("")
                    st.write("")

                    if st.button(
                        "💾 Сақтау",
                        key=f"save_comb_{u_username}"
                    ):

                        for item in users:

                            if (
                                item.get(
                                    "username"
                                )
                                == u_username
                            ):

                                item[
                                    "combination"
                                ] = (
                                    selected_combination
                                )

                                break

                        save_users(
                            users
                        )

                        st.success(
                            "Комбинация сақталды!"
                        )

                        st.rerun()

                with col_del:

                    st.write("")
                    st.write("")

                    if st.button(
                        "🗑️ Жою",
                        key=f"del_user_{u_username}"
                    ):

                        users = [
                            x for x in users
                            if x.get(
                                "username"
                            ) != u_username
                        ]

                        save_users(
                            users
                        )

                        st.rerun()

                if current_combination:

                    st.caption(
                        f"Қазір бекітілгені: "
                        f"{current_combination}"
                    )

                else:

                    st.warning(
                        "⚠️ Комбинация бекітілмеген."
                    )

            else:

                if u_role == "admin":

                    st.caption(
                        "👑 Администратор"
                    )

                elif u_role == "moderator":

                    st.caption(
                        "📝 Модератор / Премьер министр"
                    )

                if u_username != "kas01":

                    if st.button(
                        "🗑️ Жою",
                        key=f"del_user_{u_username}"
                    ):

                        users = [
                            x for x in users
                            if x.get(
                                "username"
                            ) != u_username
                        ]

                        save_users(
                            users
                        )

                        st.rerun()

                else:

                    st.caption(
                        "🔒 Басты админ — жоюға болмайды."
                    )

            st.markdown("---")

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # ADD USER
    # =====================================================

    with admin_tabs[1]:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ➕ Жаңа қолданушы қосу"
        )

        new_u = st.text_input(
            "Логин:"
        )

        new_p = st.text_input(
            "Құпия сөз:",
            type="password"
        )

        new_n = st.text_input(
            "Толық аты-жөні:"
        )

        new_r = st.selectbox(
            "Рөлі:",
            [
                "user",
                "moderator"
            ]
        )

        new_combination = None

        if new_r == "user":

            new_combination = st.selectbox(
                "🎯 Оқушының комбинациясы:",
                list(
                    combinations.keys()
                ),
                key="new_user_combination"
            )

        if st.button(
            "Қолданушыны сақтау",
            type="primary"
        ):

            if new_u and new_p:

                if username_exists(
                    new_u
                ):

                    st.error(
                        "❌ Бұл логин жүйеде бар!"
                    )

                else:

                    users.append({

                        "username": (
                            new_u.strip()
                        ),

                        "password": (
                            hash_password(
                                new_p
                            )
                        ),

                        "name": (
                            new_n.strip()
                        ),

                        "role": new_r,

                        "combination": (
                            new_combination
                        ),
                    })

                    save_users(
                        users
                    )

                    st.success(
                        "✨ Қолданушы сәтті тіркелді!"
                    )

                    st.rerun()

            else:

                st.error(
                    "⚠️ Логин мен құпия сөзді толтырыңыз!"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # STATISTICS
    # =====================================================

    with admin_tabs[2]:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        render_statistics_tab()

        st.markdown("---")

        render_analytics()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 19. TEST PREPARATION
# =========================================================

def prepare_test_data(
    subjects,
    source_data=None
):

    shuffled_data = {}

    for subject in subjects:

        if source_data is not None:

            sub_qs = [
                dict(q)
                for q in source_data.get(
                    subject,
                    []
                )
            ]

        else:

            sub_qs = [
                dict(q)
                for q in questions.get(
                    subject,
                    []
                )
            ]

            random.shuffle(
                sub_qs
            )

            limit = subject_limits.get(
                subject,
                40
            )

            sub_qs = sub_qs[
                :limit
            ]

        processed_qs = []

        for q in sub_qs:

            answers = list(
                q.get(
                    "answers",
                    []
                )
            )

            if len(answers) < 4:

                continue

            correct_index = q.get(
                "correct",
                0
            )

            if not (
                0 <= correct_index
                < len(answers)
            ):

                continue

            correct_text = answers[
                correct_index
            ]

            random.shuffle(
                answers
            )

            new_correct_idx = answers.index(
                correct_text
            )

            processed_qs.append({

                "question": q.get(
                    "question",
                    ""
                ),

                "answers": answers,

                "correct": new_correct_idx,

                "topic": q.get(
                    "topic",
                    "Жалпы"
                ),
            })

        shuffled_data[
            subject
        ] = processed_qs

    return shuffled_data


# =========================================================
# 20. RETRY TEST
# =========================================================

def create_retry_test():

    retry_data = {}

    for subject, sub_questions in (
        st.session_state.shuffled_test_data.items()
    ):

        answers = (
            st.session_state.test_answers.get(
                subject,
                {}
            )
        )

        wrong_questions = []

        for index, q in enumerate(
            sub_questions
        ):

            selected = answers.get(
                index
            )

            is_wrong = (
                selected is None
                or selected
                != q.get(
                    "correct"
                )
            )

            if is_wrong:

                wrong_questions.append({

                    "question": q.get(
                        "question",
                        ""
                    ),

                    "answers": list(
                        q.get(
                            "answers",
                            []
                        )
                    ),

                    "correct": q.get(
                        "correct",
                        0
                    ),

                    "topic": q.get(
                        "topic",
                        "Жалпы"
                    ),
                })

        if wrong_questions:

            retry_data[
                subject
            ] = wrong_questions

    if not retry_data:

        return False

    subjects = list(
        retry_data.keys()
    )

    new_data = prepare_test_data(
        subjects,
        source_data=retry_data
    )

    st.session_state.retry_data = (
        new_data
    )

    st.session_state.shuffled_test_data = (
        new_data
    )

    st.session_state.test_started = True

    st.session_state.retry_mode = True

    st.session_state.current_subject_index = 0

    st.session_state.current_question_index = 0

    st.session_state.test_answers = {}

    st.session_state.result_saved = False

    # Автоматты сақтау
    save_current_test_progress()

    return True


# =========================================================
# 21. USER PAGE
# =========================================================

def user_page():

    # =====================================================
    # HOME
    # =====================================================

    if not st.session_state.test_started:

        col_top1, col_top_out = st.columns(
            [6, 1]
        )

        with col_top1:

            st.markdown(
                f"### 👤 Қош келдіңіз, "
                f"{st.session_state.full_name}!"
            )

        with col_top_out:

            if st.button(
                "🚪 Шығу",
                use_container_width=True
            ):

                logout()

        st.markdown("---")


        # =================================================
        # RESUME TEST
        # =================================================

        saved_progress = get_test_progress(
            st.session_state.username
        )

        if saved_progress:

            saved_combination = (
                saved_progress.get(
                    "active_combination"
                )
            )

            saved_time = (
                saved_progress.get(
                    "saved_at",
                    "белгісіз"
                )
            )

            st.markdown(
                '<div class="resume-box">',
                unsafe_allow_html=True
            )

            st.markdown(
                "### 🔄 Аяқталмаған тест бар!"
            )

            st.write(
                "Сізде бұрын аяқталмай қалған "
                "тест сақталған."
            )

            if saved_combination:

                st.info(
                    f"🎯 Бағыт: "
                    f"**{saved_combination}**"
                )

            st.caption(
                f"Соңғы сақталған уақыт: {saved_time}"
            )

            resume_col1, resume_col2 = st.columns(2)

            with resume_col1:

                if st.button(
                    "🔄 Тестті жалғастыру",
                    type="primary",
                    use_container_width=True,
                    key="resume_saved_test"
                ):

                    if restore_test_progress(
                        saved_progress
                    ):

                        st.rerun()

                    else:

                        st.error(
                            "Сақталған тестті қалпына келтіру мүмкін болмады."
                        )

            with resume_col2:

                if st.button(
                    "🗑️ Аяқталмаған тестті өшіру",
                    use_container_width=True,
                    key="delete_saved_test"
                ):

                    clear_test_progress(
                        st.session_state.username
                    )

                    st.success(
                        "Аяқталмаған тест өшірілді."
                    )

                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # =================================================
        # PERSONAL CABINET
        # =================================================

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🗂️ Менің жеке кабинетім"
        )

        history = load_results_history()

        user_history = [
            h for h in history
            if h.get(
                "username"
            )
            == st.session_state.username

            and h.get(
                "test_type",
                "normal"
            ) == "normal"
        ]

        if not user_history:

            st.info(
                "ℹ️ Сіз әлі тест тапсырған жоқсыз."
            )

        else:

            total_tests = len(
                user_history
            )

            best_score = max(
                int(
                    h.get(
                        "score",
                        0
                    )
                )
                for h in user_history
            )

            avg_score = (
                sum(
                    int(
                        h.get(
                            "score",
                            0
                        )
                    )
                    for h in user_history
                )
                / total_tests
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Жалпы тесттер саны",
                    total_tests
                )

            with col2:

                st.metric(
                    "Ең жоғары ұпай",
                    f"{best_score} / 140"
                )

            with col3:

                st.metric(
                    "Орташа ұпай",
                    f"{avg_score:.1f}"
                )

            st.markdown("---")

            st.markdown(
                "#### 📈 Ұпайлардың өсу динамикасы"
            )

            scores_list = [
                int(
                    h.get(
                        "score",
                        0
                    )
                )
                for h in user_history
            ]

            st.line_chart(
                scores_list
            )

            st.markdown(
                "#### 📋 Тест тарихы"
            )

            display_data = []

            for h in user_history:

                display_data.append({

                    "Комбинация": h.get(
                        "combination"
                    ),

                    "Ұпай": (
                        f'{h.get("score", 0)} / '
                        f'{h.get("max_score", 140)}'
                    ),

                    "Күні": h.get(
                        "date"
                    ),
                })

            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            render_analytics(
                st.session_state.username
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # =================================================
        # START TEST
        # =================================================

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🎯 Жаңа тест тапсыру"
        )

        current_user = next(
            (
                u for u in users
                if u.get(
                    "username"
                )
                == st.session_state.username
            ),
            None
        )

        assigned_combination = (
            current_user or {}
        ).get(
            "combination"
        )

        if (
            assigned_combination
            and assigned_combination
            in combinations
        ):

            st.success(
                f"🎯 Сізге бекітілген бағыт: "
                f"**{assigned_combination}**"
            )

            st.caption(
                "Бұл бағытты оқушы өзі өзгерте алмайды."
            )

        else:

            st.warning(
                "⚠️ Сізге әлі тест бағыты бекітілмеген."
            )

        if st.button(
            "🚀 Тестті бастау",
            type="primary",
            use_container_width=True,
            disabled=not (
                assigned_combination
                and assigned_combination
                in combinations
            )
        ):

            # Ескі progress болса,
            # жаңа тест басталғанда өшіреміз.
            clear_test_progress(
                st.session_state.username
            )

            st.session_state.active_combination = (
                assigned_combination
            )

            st.session_state.test_started = True

            st.session_state.retry_mode = False

            st.session_state.current_subject_index = 0

            st.session_state.current_question_index = 0

            st.session_state.test_answers = {}

            st.session_state.result_saved = False

            st.session_state.shuffled_test_data = (
                prepare_test_data(
                    combinations[
                        assigned_combination
                    ]
                )
            )

            # Бірден сақтау
            save_current_test_progress()

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        return


    # =====================================================
    # TEST
    # =====================================================

    comb_name = (
        st.session_state.active_combination
    )

    if st.session_state.retry_mode:

        subj_list = list(
            st.session_state.shuffled_test_data.keys()
        )

    else:

        subj_list = combinations.get(
            comb_name,
            []
        )

    sub_idx = (
        st.session_state.current_subject_index
    )


    # =====================================================
    # TOP NAVIGATION
    # =====================================================

    col_top1, col_top_prev, col_top_next, col_top_out = st.columns(
        [3, 1.2, 1.2, 0.8]
    )

    with col_top1:

        if st.session_state.retry_mode:

            st.markdown(
                "**🔁 Қате сұрақтарды қайта тапсыру**"
            )

        else:

            st.markdown(
                f"**👤 {st.session_state.full_name}**"
            )

    with col_top_prev:

        if st.button(
            "< Алдыңғы пән",
            use_container_width=True,
            disabled=(
                sub_idx == 0
            )
        ):

            if sub_idx > 0:

                st.session_state.current_subject_index -= 1

                st.session_state.current_question_index = 0

                save_current_test_progress()

                st.rerun()

    with col_top_next:

        is_last_subject = (
            sub_idx >= len(
                subj_list
            ) - 1
        )

        next_subj_label = (
            "Нәтижеге 🏁"
            if is_last_subject
            else "Келесі пән >"
        )

        if st.button(
            next_subj_label,
            use_container_width=True,
            type="primary",
            key=f"top_next_subj_{sub_idx}"
        ):

            if not is_last_subject:

                st.session_state.current_subject_index += 1

                st.session_state.current_question_index = 0

                save_current_test_progress()

            else:

                st.session_state.current_subject_index = len(
                    subj_list
                )

                save_current_test_progress()

            st.rerun()

    with col_top_out:

        if st.button(
            "🚪 Шығу",
            use_container_width=True
        ):

            # logout() ішінде save болады.
            logout()

    st.markdown("---")


    # =====================================================
    # QUESTION
    # =====================================================

    if sub_idx < len(
        subj_list
    ):

        current_subject = subj_list[
            sub_idx
        ]

        sub_questions = (
            st.session_state.shuffled_test_data.get(
                current_subject,
                []
            )
        )

        if not sub_questions:

            st.warning(
                f"{current_subject} пәнінде "
                "әзірге сұрақ жоқ."
            )

            return

        curr_q_idx = (
            st.session_state.current_question_index
        )

        # Қауіпсіздік
        if curr_q_idx < 0:

            curr_q_idx = 0

            st.session_state.current_question_index = 0

        if curr_q_idx >= len(
            sub_questions
        ):

            curr_q_idx = len(
                sub_questions
            ) - 1

            st.session_state.current_question_index = (
                curr_q_idx
            )

        num_qs = len(
            sub_questions
        )

        st.markdown(
            f"**Бөлім: {current_subject}**"
        )


        # =================================================
        # LEGEND
        # =================================================

        st.markdown(
            """
            <div class="nav-legend">
                🔵 Қазіргі сұрақ
                &nbsp;&nbsp;&nbsp;
                🟢 Жауап берілген
                &nbsp;&nbsp;&nbsp;
                ⚪ Жауап берілмеген
            </div>
            """,
            unsafe_allow_html=True
        )


        if current_subject not in (
            st.session_state.test_answers
        ):

            st.session_state.test_answers[
                current_subject
            ] = {}


        current_answers = (
            st.session_state.test_answers[
                current_subject
            ]
        )


        # =================================================
        # QUESTION PALETTE
        # =================================================

        cols_per_row = 20

        for i in range(
            0,
            num_qs,
            cols_per_row
        ):

            chunk = range(
                i,
                min(
                    i + cols_per_row,
                    num_qs
                )
            )

            pal_cols = st.columns(
                len(chunk)
            )

            for idx, q_i in enumerate(
                chunk
            ):

                with pal_cols[idx]:

                    is_current = (
                        q_i == curr_q_idx
                    )

                    is_answered = (
                        q_i
                        in current_answers
                    )

                    if is_current:

                        label = (
                            f"🔵 {q_i + 1}"
                        )

                    elif is_answered:

                        label = (
                            f"🟢 {q_i + 1}"
                        )

                    else:

                        label = (
                            f"⚪ {q_i + 1}"
                        )

                    btn_type = (
                        "primary"
                        if is_current
                        else "secondary"
                    )

                    if st.button(
                        label,
                        key=f"pal_{sub_idx}_{q_i}",
                        use_container_width=True,
                        type=btn_type
                    ):

                        st.session_state.current_question_index = q_i

                        save_current_test_progress()

                        st.rerun()

        st.markdown("---")


        # =================================================
        # QUESTION TITLE
        # =================================================

        col_q_title, col_next_q_btn = st.columns(
            [6, 1.5]
        )

        with col_q_title:

            st.markdown(
                f"#### Сұрақ №{curr_q_idx + 1}"
            )

        with col_next_q_btn:

            is_last_q_in_sub = (
                curr_q_idx
                == num_qs - 1
            )

            nxt_label = (
                "Келесі пән >"
                if is_last_q_in_sub
                else "Келесі сұрақ >"
            )

            if st.button(
                nxt_label,
                type="primary",
                use_container_width=True,
                key=f"next_btn_{sub_idx}_{curr_q_idx}"
            ):

                if not is_last_q_in_sub:

                    st.session_state.current_question_index += 1

                else:

                    st.session_state.current_subject_index += 1

                    st.session_state.current_question_index = 0

                save_current_test_progress()

                st.rerun()


        # =================================================
        # CURRENT QUESTION
        # =================================================

        q_data = sub_questions[
            curr_q_idx
        ]

        st.markdown(
            f"**{q_data['question']}**"
        )

        saved_ans_idx = (
            current_answers.get(
                curr_q_idx
            )
        )

        selected_option = st.radio(
            "Жауапты таңдаңыз:",
            q_data["answers"],
            key=f"radio_{sub_idx}_{curr_q_idx}",
            index=(
                saved_ans_idx
                if saved_ans_idx is not None
                and 0 <= saved_ans_idx < len(
                    q_data["answers"]
                )
                else None
            )
        )

        if selected_option is not None:

            chosen_idx = (
                q_data["answers"].index(
                    selected_option
                )
            )

            st.session_state.test_answers[
                current_subject
            ][curr_q_idx] = chosen_idx

            # Жауапты бірден файлға сақтаймыз.
            save_current_test_progress()


    # =====================================================
    # RESULT
    # =====================================================

    else:

        if st.session_state.retry_mode:

            render_retry_result()

        else:

            render_normal_result()


# =========================================================
# 22. NORMAL RESULT
# =========================================================

def render_normal_result():

    st.markdown(
        "## 🏆 Тест аяқталды!"
    )

    st.success(
        "Тестіңіз сәтті аяқталды. "
        "Төменнен толық нәтижеңізді көре аласыз."
    )

    comb_name = (
        st.session_state.active_combination
    )

    subj_list = combinations.get(
        comb_name,
        []
    )


    # =====================================================
    # 140 БАЛЛДЫҚ СИСТЕМА
    # =====================================================

    subject_max_points = {

        "Қазақстан тарихы": 20,

        "Оқу сауаттылығы": 10,

        "Математикалық сауаттылық": 10,

        "Математика": 50,

        "Физика": 50,

        "Химия": 50,

        "Биология": 50,

        "Информатика": 50,

        "География": 50,

        "Дүниежүзі тарихы": 50,

        "Ағылшын тілі": 50,

        "Құқық": 50,
    }

    subject_results = []

    total_score = 0

    total_max_points = 0

    total_correct = 0

    total_questions = 0

    total_unanswered = 0


    for sub in subj_list:

        sub_qs = (
            st.session_state.shuffled_test_data.get(
                sub,
                []
            )
        )

        sub_ans = (
            st.session_state.test_answers.get(
                sub,
                {}
            )
        )

        question_count = len(
            sub_qs
        )

        correct_count = sum(
            1
            for idx, q in enumerate(
                sub_qs
            )
            if sub_ans.get(
                idx
            ) == q.get(
                "correct"
            )
        )

        unanswered_count = sum(
            1
            for idx in range(
                question_count
            )
            if idx not in sub_ans
        )

        max_points = subject_max_points.get(
            sub,
            question_count
        )

        expected_questions = (
            subject_limits.get(
                sub,
                question_count
            )
        )

        if question_count > 0:

            score = round(
                correct_count
                * max_points
                / question_count
            )

        else:

            score = 0

        total_score += score

        total_max_points += max_points

        total_correct += correct_count

        total_questions += question_count

        total_unanswered += (
            unanswered_count
        )

        subject_results.append({

            "subject": sub,

            "correct": correct_count,

            "questions": question_count,

            "score": score,

            "max_score": max_points,

            "expected_questions": expected_questions,
        })


    # Негізгі тест үшін максимум 140.
    # Қалыпты комбинацияда:
    # 50 + 50 + 20 + 10 + 10 = 140
    if total_max_points != 140:

        total_max_points = 140


    total_wrong = (
        total_questions
        - total_correct
        - total_unanswered
    )

    percentage = (
        round(
            total_score
            / total_max_points
            * 100,
            1
        )
        if total_max_points
        else 0
    )

    st.session_state.current_subject_results = (
        subject_results
    )


    # =====================================================
    # BIG SCORE
    # =====================================================

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="score-label">'
        'Сіздің жалпы нәтижеңіз'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="score-big">'
        f'{total_score} / {total_max_points}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="score-label">'
        f'{percentage}%'
        f'</div>',
        unsafe_allow_html=True
    )

    st.progress(
        min(
            max(
                total_score
                / total_max_points
                if total_max_points
                else 0,
                0
            ),
            1
        )
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # SUMMARY
    # =====================================================

    summary1, summary2, summary3, summary4 = st.columns(4)

    with summary1:

        st.metric(
            "✅ Дұрыс",
            total_correct
        )

    with summary2:

        st.metric(
            "❌ Қате",
            total_wrong
        )

    with summary3:

        st.metric(
            "⚪ Жауапсыз",
            total_unanswered
        )

    with summary4:

        st.metric(
            "📊 Пайыз",
            f"{percentage}%"
        )


    # =====================================================
    # MESSAGE
    # =====================================================

    if percentage >= 90:

        st.success(
            "🔥 Керемет нәтиже! "
            "Сіз өте жақсы дайындалып жатырсыз."
        )

    elif percentage >= 70:

        st.info(
            "💪 Жақсы нәтиже! "
            "Әлсіз тақырыптарды тағы қайталап көріңіз."
        )

    elif percentage >= 50:

        st.warning(
            "📚 Жаман емес, бірақ нәтижеңізді "
            "көтеруге мүмкіндік көп."
        )

    else:

        st.error(
            "🎯 Негізгі тақырыптарды қайталап, "
            "тағы бір тест тапсырып көріңіз."
        )


    # =====================================================
    # SUBJECT RESULTS
    # =====================================================

    st.markdown("---")

    st.markdown(
        "### 📚 Пәндер бойынша нәтиже"
    )

    for item in subject_results:

        subject_name = item[
            "subject"
        ]

        correct = item[
            "correct"
        ]

        questions_count = item[
            "questions"
        ]

        score = item[
            "score"
        ]

        max_score = item[
            "max_score"
        ]

        subject_percent = (
            round(
                score
                / max_score
                * 100,
                1
            )
            if max_score
            else 0
        )

        st.markdown(
            f"**{subject_name}** — "
            f"{correct} / {questions_count} дұрыс · "
            f"🎯 **{score} / {max_score} балл** "
            f"({subject_percent}%)"
        )

        progress_value = (
            score / max_score
            if max_score
            else 0
        )

        st.progress(
            min(
                max(
                    progress_value,
                    0.0
                ),
                1.0
            )
        )


    # =====================================================
    # TABLE
    # =====================================================

    st.markdown(
        "#### 📋 Қысқаша кесте"
    )

    result_table = []

    for item in subject_results:

        result_table.append({

            "Пән": item[
                "subject"
            ],

            "Дұрыс жауап": (
                f'{item["correct"]} / '
                f'{item["questions"]}'
            ),

            "Ұпай": (
                f'{item["score"]} / '
                f'{item["max_score"]}'
            ),
        })

    st.dataframe(
        result_table,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # REVIEW
    # =====================================================

    question_review = {}

    st.markdown("---")

    st.markdown(
        "### 🔎 Сұрақтарды толық талдау"
    )

    st.caption(
        "Қай сұраққа қате немесе жауапсыз кеткеніңізді "
        "толық көре аласыз."
    )

    for sub in subj_list:

        sub_qs = (
            st.session_state.shuffled_test_data.get(
                sub,
                []
            )
        )

        sub_ans = (
            st.session_state.test_answers.get(
                sub,
                {}
            )
        )

        subject_review = []

        with st.expander(
            f"📚 {sub} — "
            f"{len(sub_qs)} сұрақ"
        ):

            for q_idx, q in enumerate(
                sub_qs
            ):

                selected_idx = (
                    sub_ans.get(
                        q_idx
                    )
                )

                correct_idx = q.get(
                    "correct"
                )

                answers = q.get(
                    "answers",
                    []
                )

                if selected_idx is None:

                    status = (
                        "⚪ Жауап берілмеді"
                    )

                elif selected_idx == correct_idx:

                    status = "✅ Дұрыс"

                else:

                    status = "❌ Қате"

                selected_text = (

                    answers[
                        selected_idx
                    ]

                    if (
                        selected_idx
                        is not None
                        and 0 <= selected_idx
                        < len(answers)
                    )

                    else "Жауап берілмеді"
                )

                correct_text = (

                    answers[
                        correct_idx
                    ]

                    if (
                        correct_idx
                        is not None
                        and 0 <= correct_idx
                        < len(answers)
                    )

                    else "Көрсетілмеген"
                )

                st.markdown(
                    f"#### {q_idx + 1}. "
                    f"{status}"
                )

                st.markdown(
                    f"**{q.get('question', '')}**"
                )

                st.markdown(
                    f"📝 **Сіздің жауабыңыз:** "
                    f"{selected_text}"
                )

                st.markdown(
                    f"🎯 **Дұрыс жауап:** "
                    f"{correct_text}"
                )

                for option_idx, option_text in enumerate(
                    answers
                ):

                    if option_idx == correct_idx:

                        prefix = "🟢"

                    elif option_idx == selected_idx:

                        prefix = "🔴"

                    else:

                        prefix = "⚪"

                    st.write(
                        f"{prefix} {option_text}"
                    )

                st.markdown(
                    "---"
                )

                subject_review.append({

                    "question_number": (
                        q_idx + 1
                    ),

                    "question": q.get(
                        "question",
                        ""
                    ),

                    "answers": answers,

                    "selected_answer": selected_text,

                    "correct_answer": correct_text,

                    "selected_index": selected_idx,

                    "correct_index": correct_idx,

                    "status": status,

                    "topic": q.get(
                        "topic",
                        "Жалпы"
                    ),
                })

        question_review[
            sub
        ] = subject_review


    # =====================================================
    # SAVE RESULT
    # =====================================================

    if not st.session_state.get(
        "result_saved",
        False
    ):

        history = load_results_history()

        history.append({

            "username": (
                st.session_state.username
            ),

            "name": (
                st.session_state.full_name
            ),

            "combination": comb_name,

            "score": total_score,

            "max_score": total_max_points,

            "subject_results": subject_results,

            "question_review": question_review,

            "test_type": "normal",

            "date": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
        })

        save_results_history(
            history
        )

        st.session_state.result_saved = True

        # Тест аяқталды.
        # Ескі progress енді қажет емес.
        clear_test_progress(
            st.session_state.username
        )

        st.success(
            "✨ Нәтижеңіз жеке кабинетке сақталды!"
        )


    # =====================================================
    # RETRY
    # =====================================================

    wrong_count = 0

    for sub, sub_qs in (
        st.session_state.shuffled_test_data.items()
    ):

        sub_ans = (
            st.session_state.test_answers.get(
                sub,
                {}
            )
        )

        for idx, q in enumerate(
            sub_qs
        ):

            if (
                sub_ans.get(
                    idx
                )
                != q.get(
                    "correct"
                )
            ):

                wrong_count += 1


    st.markdown("---")

    if wrong_count > 0:

        st.info(
            f"🔁 Сізде қайта қарауға "
            f"**{wrong_count}** қате немесе "
            "жауапсыз сұрақ бар."
        )

        if st.button(
            "🔁 Қате және жауапсыз сұрақтарды қайта тапсыру",
            type="primary",
            use_container_width=True,
            key="retry_wrong_questions"
        ):

            if create_retry_test():

                st.rerun()

    else:

        st.success(
            "🎉 Барлық сұраққа дұрыс жауап бердіңіз!"
        )


    # =====================================================
    # HOME
    # =====================================================

    if st.button(
        "🔄 Басты бетке қайту",
        type="primary",
        use_container_width=True,
        key="return_home_btn"
    ):

        clear_test_progress(
            st.session_state.username
        )

        st.session_state.test_started = False

        st.session_state.current_subject_index = 0

        st.session_state.current_question_index = 0

        st.session_state.current_subject_results = []

        st.session_state.retry_mode = False

        st.session_state.shuffled_test_data = {}

        st.session_state.test_answers = {}

        st.rerun()


# =========================================================
# 23. RETRY RESULT
# =========================================================

def render_retry_result():

    st.markdown(
        "## 🔁 Қайта тапсыру нәтижесі"
    )

    total_questions = 0

    correct_answers = 0

    retry_subject_results = []

    for subject, sub_qs in (
        st.session_state.shuffled_test_data.items()
    ):

        answers = (
            st.session_state.test_answers.get(
                subject,
                {}
            )
        )

        subject_total = len(
            sub_qs
        )

        subject_correct = sum(
            1
            for idx, q in enumerate(
                sub_qs
            )
            if answers.get(
                idx
            ) == q.get(
                "correct"
            )
        )

        total_questions += (
            subject_total
        )

        correct_answers += (
            subject_correct
        )

        retry_subject_results.append({

            "Пән": subject,

            "Дұрыс": subject_correct,

            "Барлығы": subject_total,
        })


    percentage = (

        round(
            correct_answers
            / total_questions
            * 100,
            1
        )

        if total_questions

        else 0
    )


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Дұрыс жауап",
            f"{correct_answers} / {total_questions}"
        )

    with col2:

        st.metric(
            "📊 Нәтиже",
            f"{percentage}%"
        )

    st.progress(
        percentage / 100
        if percentage
        else 0
    )

    st.markdown("---")

    st.markdown(
        "### 📚 Пән бойынша"
    )

    st.dataframe(
        retry_subject_results,
        use_container_width=True,
        hide_index=True
    )

    if correct_answers == total_questions:

        st.success(
            "🔥 Керемет! Қате сұрақтардың "
            "барлығын дұрыс орындадыңыз!"
        )

    else:

        st.warning(
            "💪 Кейбір сұрақтар әлі де қате. "
            "Негізгі тесттен қайта қарап шығыңыз."
        )

    st.info(
        "ℹ️ Қайта тапсыру нәтижесі негізгі "
        "140 балдық статистикаға қосылмайды."
    )

    if st.button(
        "🏠 Басты бетке қайту",
        type="primary",
        use_container_width=True,
        key="retry_home"
    ):

        clear_test_progress(
            st.session_state.username
        )

        st.session_state.test_started = False

        st.session_state.retry_mode = False

        st.session_state.current_subject_index = 0

        st.session_state.current_question_index = 0

        st.session_state.test_answers = {}

        st.session_state.shuffled_test_data = {}

        st.session_state.retry_data = {}

        st.rerun()


# =========================================================
# 24. MAIN
# =========================================================

def main():

    if not st.session_state.logged_in:

        login_page()

    else:

        role = (
            st.session_state.role
        )

        if role == "admin":

            admin_page()

        elif role == "moderator":

            moderator_page()

        elif role == "user":

            user_page()

        else:

            logout()


# =========================================================
# 25. START
# =========================================================

if __name__ == "__main__":

    main()
