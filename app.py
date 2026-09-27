import datetime
import hashlib
import json
import os
import random
import re
import streamlit as st

# =========================================================
# 1. КОНФИГУРАЦИЯ ЖӘНЕ ФАЙЛДАР
# =========================================================

st.set_page_config(
    page_title="KASYM EDU - Білім беру платформасы",
    page_icon="🎓",
    layout="wide"
)

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"


# =========================================================
# 2. ҚАУІПСІЗДІК ЖӘНЕ ХЭШТЕУ
# =========================================================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# =========================================================
# 3. ПӘНДЕР МЕН КОМБИНАЦИЯЛАР
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
        }
    ],
}


# =========================================================
# 5. ҚОЛДАНУШЫЛАР
# =========================================================

def default_users():

    return [
        {
            "username": "kas01",
            "password": hash_password("kasko100228550357"),
            "name": "KASYM",
            "role": "admin",
            "combination": None,
        }
    ]


def save_users(users_list):

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


def load_users():

    users_list = default_users()

    if os.path.exists(USERS_FILE):

        try:

            with open(
                USERS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list) and len(data) > 0:
                    users_list = data

        except Exception:
            pass

    admin_found = False

    for user in users_list:

        if user.get("username") == "kas01":

            user["role"] = "admin"

            admin_found = True

    if not admin_found:

        users_list.append(
            {
                "username": "kas01",
                "password": hash_password(
                    "kasko100228550357"
                ),
                "name": "KASYM",
                "role": "admin",
                "combination": None,
            }
        )

    save_users(users_list)

    return users_list


users = load_users()


def find_user(username, password):

    hashed_input = hash_password(password)

    for user in users:

        stored = user.get("password")

        if (
            user.get("username") == username
            and (
                stored == hashed_input
                or stored == password
            )
        ):
            return user

    return None


def username_exists(username):

    return any(
        user.get("username") == username
        for user in users
    )


# =========================================================
# 6. СҰРАҚТАР БАЗАСЫ
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

                for subject in all_subjects:

                    if subject not in data:

                        data[subject] = default_questions.get(
                            subject,
                            []
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
# 7. НӘТИЖЕЛЕР
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
# 8. SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "full_name" not in st.session_state:
    st.session_state.full_name = ""

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "active_combination" not in st.session_state:
    st.session_state.active_combination = None

if "current_subject_index" not in st.session_state:
    st.session_state.current_subject_index = 0

if "test_answers" not in st.session_state:
    st.session_state.test_answers = {}

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "bulk_preview" not in st.session_state:
    st.session_state.bulk_preview = []

if "bulk_errors" not in st.session_state:
    st.session_state.bulk_errors = []


# =========================================================
# 9. DESIGN
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

        background:
        linear-gradient(
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

        background:
        linear-gradient(
            145deg,
            #1E293B 0%,
            #0F172A 100%
        );

        padding: 24px;

        border-radius: 16px;

        border:
        1px solid rgba(
            255,
            255,
            255,
            0.08
        );

        box-shadow:
        0 10px 25px -5px
        rgba(0,0,0,0.3);

        margin-bottom: 20px;
    }

    .stButton>button {

        border-radius: 12px;

        font-weight: 600;

        border:
        1px solid
        rgba(
            255,
            255,
            255,
            0.08
        );

        background-color: #1E293B;

        color: #F3F4F6;

        transition: all 0.3s ease;
    }

    .stButton>button:hover {

        border-color: #6366F1;

        color: #6366F1;

        transform:
        translateY(-2px);
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stTextArea>div>div>textarea {

        background-color:
        #1E293B !important;

        border-radius:
        10px !important;

        color:
        #F3F4F6 !important;

        border:
        1px solid
        rgba(
            255,
            255,
            255,
            0.08
        ) !important;
    }

    [data-testid="stSidebar"] {

        background-color:
        #0F172A;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 10. LOGOUT
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""
    st.session_state.full_name = ""
    st.session_state.test_started = False
    st.session_state.active_combination = None
    st.session_state.current_subject_index = 0
    st.session_state.test_answers = {}
    st.session_state.bulk_preview = []
    st.session_state.bulk_errors = []

    st.rerun()


# =========================================================
# 11. LOGIN
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

        tab_login, tab_register = st.tabs(
            [
                "🔐 Жүйеге кіру",
                "📝 Тіркелу"
            ]
        )

        # ---------------- LOGIN ----------------

        with tab_login:

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

                user = find_user(
                    username.strip(),
                    password.strip()
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.full_name = user.get(
                        "name",
                        ""
                    )
                    st.session_state.role = user.get(
                        "role",
                        "user"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Логин немесе құпия сөз қате."
                    )

        # ---------------- REGISTER ----------------

        with tab_register:

            reg_name = st.text_input(
                "Толық аты-жөніңіз:"
            )

            reg_user = st.text_input(
                "Жаңа логин таңдаңыз:"
            )

            reg_pass = st.text_input(
                "Құпия сөз ойлап табыңыз:",
                type="password",
                key="reg_pass"
            )

            if st.button(
                "Тіркелуді аяқтау",
                use_container_width=True,
                type="primary"
            ):

                if reg_name and reg_user and reg_pass:

                    if username_exists(
                        reg_user.strip()
                    ):

                        st.error(
                            "❌ Бұл логин бос емес."
                        )

                    else:

                        new_student = {

                            "username":
                            reg_user.strip(),

                            "password":
                            hash_password(
                                reg_pass.strip()
                            ),

                            "name":
                            reg_name.strip(),

                            "role":
                            "user",

                            "combination":
                            None,
                        }

                        users.append(
                            new_student
                        )

                        save_users(users)

                        st.success(
                            "✨ Сәтті тіркелдіңіз!"
                        )

                else:

                    st.error(
                        "⚠️ Барлық өрістерді толтырыңыз!"
                    )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 12. СТАТИСТИКА
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

    avg_score = (
        sum(
            int(
                h.get(
                    "score",
                    0
                ) or 0
            )
            for h in history
        )
        / total_tests
        if total_tests > 0
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

        search_query = st.text_input(
            "🔍 Оқушының аты немесе логині бойынша іздеу:",
            key="stat_search"
        ).strip().lower()

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
            or
            search_query in uname.lower()
        )

        match_comb = (
            comb_filter == "Барлығы"
            or
            comb == comb_filter
        )

        if match_search and match_comb:

            filtered_history.append(
                {
                    "Аты-жөні": name,
                    "Логин": f"@{uname}",
                    "Комбинация": comb,
                    "Ұпай": score,
                    "Күні": date,
                }
            )

    st.caption(
        f"Табылған нәтижелер саны: "
        f"{len(filtered_history)}"
    )

    if not filtered_history:

        st.warning(
            "⚠️ Нәтиже табылмады."
        )

    else:

        st.dataframe(
            filtered_history,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 13. МАССАЛЫҚ ЖҮКТЕУ — ЖАҢА ДҰРЫС ПАРСЕР
# =========================================================

def normalize_correct_letter(letter):

    letter = letter.strip().upper()

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

    return letter_map.get(letter)


def parse_bulk_questions(raw_text):

    parsed_questions = []
    errors = []

    if not raw_text or not raw_text.strip():

        return parsed_questions, errors

    # Windows / Mac жолдарын бір форматқа келтіру
    raw_text = raw_text.replace(
        "\r\n",
        "\n"
    ).replace(
        "\r",
        "\n"
    )

    # Артық бос жолдарды сақтаймыз
    lines = raw_text.split("\n")

    # -----------------------------------------
    # Сұрақ блоктарын бөлу
    # -----------------------------------------

    blocks = []
    current_block = []

    question_start_pattern = re.compile(
        r"^\s*\d+\s*[\.\)]\s+"
    )

    for line in lines:

        stripped = line.strip()

        if question_start_pattern.match(stripped):

            if current_block:

                blocks.append(
                    current_block
                )

            current_block = [stripped]

        else:

            if current_block:

                current_block.append(
                    stripped
                )

    if current_block:

        blocks.append(
            current_block
        )

    # -----------------------------------------
    # Егер нөмірмен бөлінбесе
    # -----------------------------------------

    if not blocks:

        errors.append(
            "Сұрақтар 1. / 2. / 3. форматында басталуы керек."
        )

        return [], errors

    # -----------------------------------------
    # Әр блокты өңдеу
    # -----------------------------------------

    for block_number, block in enumerate(
        blocks,
        start=1
    ):

        try:

            block = [
                line.strip()
                for line in block
                if line.strip()
            ]

            if not block:
                continue

            # Бір блокты бір мәтінге айналдырамыз
            block_text = "\n".join(
                block
            )

            # ---------------------------------
            # Сұрақ нөмірін алып тастау
            # ---------------------------------

            first_line = re.sub(
                r"^\s*\d+\s*[\.\)]\s*",
                "",
                block[0]
            ).strip()

            # ---------------------------------
            # Нұсқаларды іздеу
            # ---------------------------------

            option_pattern = re.compile(
                r"^\s*([A-DА-Гa-dа-г])"
                r"\s*[\.\)\:\-]\s*(.+?)\s*$"
            )

            options = []

            question_lines = []

            correct_index = None

            for line in block:

                # -----------------------------
                # Дұрыс жауап жолы
                # -----------------------------

                answer_match = re.match(
                    r"^\s*"
                    r"(?:Жауабы|Дұрыс жауап|Жауап|Correct)"
                    r"\s*[:\-]?\s*"
                    r"([A-DА-Гa-dа-г])"
                    r"\s*$",
                    line,
                    re.IGNORECASE
                )

                if answer_match:

                    correct_index = normalize_correct_letter(
                        answer_match.group(1)
                    )

                    continue

                # -----------------------------
                # Нұсқа
                # -----------------------------

                option_match = option_pattern.match(
                    line
                )

                if option_match:

                    letter = option_match.group(
                        1
                    )

                    answer_text = option_match.group(
                        2
                    ).strip()

                    # * белгісі арқылы дұрыс жауап
                    is_marked_correct = False

                    if answer_text.startswith("*"):

                        is_marked_correct = True

                        answer_text = (
                            answer_text[1:]
                            .strip()
                        )

                    if answer_text.endswith(
                        "(+)"
                    ):

                        is_marked_correct = True

                        answer_text = (
                            answer_text[:-3]
                            .strip()
                        )

                    option_index = len(
                        options
                    )

                    options.append(
                        answer_text
                    )

                    if is_marked_correct:

                        correct_index = option_index

                else:

                    # Нұсқалар басталмаған кезде
                    # бұл сұрақтың мәтіні

                    if not options:

                        question_lines.append(
                            line
                        )

            # ---------------------------------
            # Сұрақ мәтінін жинау
            # ---------------------------------

            question_text = " ".join(
                question_lines
            ).strip()

            # Бірінші жолдан нөмірді алып тастау
            question_text = re.sub(
                r"^\s*\d+\s*[\.\)]\s*",
                "",
                question_text
            ).strip()

            # ---------------------------------
            # INLINE форматты тексеру
            # ---------------------------------

            if (
                len(options) < 4
                and len(block) == 1
            ):

                inline_text = block[0]

                inline_text = re.sub(
                    r"^\s*\d+\s*[\.\)]\s*",
                    "",
                    inline_text
                )

                inline_matches = list(
                    re.finditer(
                        r"(?<!\w)"
                        r"([A-DА-Гa-dа-г])"
                        r"\s*[\.\)]\s*",
                        inline_text
                    )
                )

                if len(inline_matches) >= 4:

                    question_text = (
                        inline_text[
                            :inline_matches[0].start()
                        ].strip()
                    )

                    options = []

                    for i, match in enumerate(
                        inline_matches[:4]
                    ):

                        start = match.end()

                        if i + 1 < len(
                            inline_matches
                        ):

                            end = inline_matches[
                                i + 1
                            ].start()

                        else:

                            answer_match = re.search(
                                r"\b(?:Жауабы|Дұрыс жауап|Жауап)"
                                r"\s*[:\-]?\s*[A-DА-Гa-dа-г]",
                                inline_text[
                                    start:
                                ],
                                re.IGNORECASE
                            )

                            if answer_match:

                                end = (
                                    start
                                    +
                                    answer_match.start()
                                )

                            else:

                                end = len(
                                    inline_text
                                )

                        answer_text = inline_text[
                            start:end
                        ].strip()

                        options.append(
                            answer_text
                        )

                    answer_line_match = re.search(
                        r"(?:Жауабы|Дұрыс жауап|Жауап)"
                        r"\s*[:\-]?\s*"
                        r"([A-DА-Гa-dа-г])",
                        inline_text,
                        re.IGNORECASE
                    )

                    if answer_line_match:

                        correct_index = (
                            normalize_correct_letter(
                                answer_line_match.group(1)
                            )
                        )

            # ---------------------------------
            # Тексеру
            # ---------------------------------

            if not question_text:

                errors.append(
                    f"{block_number}-сұрақ: "
                    f"сұрақ мәтіні табылмады."
                )

                continue

            if len(options) != 4:

                errors.append(
                    f"{block_number}-сұрақ: "
                    f"4 нұсқа табылмады "
                    f"(табылғаны: {len(options)})."
                )

                continue

            if correct_index is None:

                errors.append(
                    f"{block_number}-сұрақ: "
                    f"дұрыс жауап көрсетілмеген."
                )

                continue

            if correct_index < 0 or correct_index > 3:

                errors.append(
                    f"{block_number}-сұрақ: "
                    f"дұрыс жауап индексі қате."
                )

                continue

            # ---------------------------------
            # Дайын сұрақ
            # ---------------------------------

            parsed_questions.append(
                {
                    "question": question_text,
                    "answers": options[:4],
                    "correct": correct_index,
                }
            )

        except Exception as error:

            errors.append(
                f"{block_number}-сұрақты оқу кезінде "
                f"қате шықты: {error}"
            )

    return parsed_questions, errors


# =========================================================
# 14. МОДЕРАТОР ПАНЕЛІ
# =========================================================

def moderator_page():

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            '<div class="kasym-title" '
            'style="font-size: 32px;">'
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

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "⚡ Массалық жүктеу",
            "✍️ Жеке сұрақ қосу",
            "🗑️ Сұрақтарды жою",
            "📊 Оқушылар статистикасы"
        ]
    )


    # =====================================================
    # МАССАЛЫҚ ЖҮКТЕУ
    # =====================================================

    with tab1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ⚡ Сұрақтарды жаппай жүктеу"
        )

        st.info(
            "💡 Бірден 40, 50 немесе 100 сұрақ "
            "қосуға болады."
        )

        sel_sub_bulk = st.selectbox(
            "📚 Пәнді таңдаңыз:",
            all_subjects,
            key="mod_bulk_sub"
        )

        st.markdown(
            "#### 📝 Қажетті формат:"
        )

        st.code(
            """1. Фотосинтез процесі қай органоидта жүреді?
A) Митохондрия
B) Хлоропласт
C) Рибосома
D) Лизосома
Жауабы: B

2. Адам ағзасындағы ең үлкен мүше:
A) Жүрек
B) Бауыр
C) Тері
D) Өкпе
Жауабы: C""",
            language="text"
        )

        st.markdown(
            "#### 📥 Сұрақтарды осында қойыңыз:"
        )

        raw_text = st.text_area(
            "",
            height=350,
            key="bulk_question_text",
            placeholder=(
                "1. Сұрақ мәтіні?\n"
                "A) Бірінші жауап\n"
                "B) Екінші жауап\n"
                "C) Үшінші жауап\n"
                "D) Төртінші жауап\n"
                "Жауабы: B\n\n"
                "2. Келесі сұрақ..."
            )
        )

        st.markdown("---")

        col_check, col_upload, col_clear = st.columns(
            [1, 1, 1]
        )


        # =================================================
        # ТЕКСЕРУ
        # =================================================

        with col_check:

            if st.button(
                "🔎 Тексеру",
                use_container_width=True
            ):

                if raw_text.strip():

                    parsed, errors = parse_bulk_questions(
                        raw_text
                    )

                    st.session_state.bulk_preview = parsed
                    st.session_state.bulk_errors = errors

                    if parsed:

                        st.success(
                            f"✅ {len(parsed)} сұрақ дұрыс танылды!"
                        )

                    if errors:

                        st.warning(
                            f"⚠️ {len(errors)} сұрақта қате бар."
                        )

                else:

                    st.warning(
                        "⚠️ Алдымен сұрақтарды енгізіңіз."
                    )


        # =================================================
        # БАРЛЫҚ СҰРАҚТЫ БАЗАҒА ҚОСУ
        # =================================================

        with col_upload:

            if st.button(
                "🚀 Базаға жүктеу",
                type="primary",
                use_container_width=True
            ):

                preview = st.session_state.get(
                    "bulk_preview",
                    []
                )

                if not preview:

                    st.error(
                        "❌ Алдымен «🔎 Тексеру» батырмасын басыңыз."
                    )

                else:

                    if sel_sub_bulk not in questions:

                        questions[
                            sel_sub_bulk
                        ] = []

                    old_count = len(
                        questions[
                            sel_sub_bulk
                        ]
                    )

                    questions[
                        sel_sub_bulk
                    ].extend(
                        preview
                    )

                    save_questions()

                    new_count = len(
                        questions[
                            sel_sub_bulk
                        ]
                    )

                    st.success(
                        f"🎉 {len(preview)} сұрақ "
                        f"«{sel_sub_bulk}» пәніне қосылды!"
                    )

                    st.info(
                        f"📊 Бұрын: {old_count} | "
                        f"Қазір: {new_count}"
                    )

                    st.session_state.bulk_preview = []
                    st.session_state.bulk_errors = []


        # =================================================
        # ТАЗАЛАУ
        # =================================================

        with col_clear:

            if st.button(
                "🧹 Тазалау",
                use_container_width=True
            ):

                st.session_state.bulk_preview = []
                st.session_state.bulk_errors = []

                st.rerun()


        # =================================================
        # АЛДЫН АЛА КӨРУ
        # =================================================

        preview = st.session_state.get(
            "bulk_preview",
            []
        )

        errors = st.session_state.get(
            "bulk_errors",
            []
        )


        if preview:

            st.markdown("---")

            st.markdown(
                f"### 👀 Алдын ала тексеру — "
                f"{len(preview)} сұрақ"
            )

            for i, q in enumerate(
                preview,
                start=1
            ):

                correct_letter = [
                    "A",
                    "B",
                    "C",
                    "D"
                ][q["correct"]]

                with st.expander(
                    f"{i}. {q['question']}"
                ):

                    for j, answer in enumerate(
                        q["answers"]
                    ):

                        letter = [
                            "A",
                            "B",
                            "C",
                            "D"
                        ][j]

                        if j == q["correct"]:

                            st.success(
                                f"✅ {letter}) {answer}"
                            )

                        else:

                            st.write(
                                f"{letter}) {answer}"
                            )

                    st.caption(
                        f"Дұрыс жауап: {correct_letter}"
                    )


        # =================================================
        # ҚАТЕЛЕР
        # =================================================

        if errors:

            st.markdown("---")

            st.markdown(
                "### ⚠️ Танылмаған сұрақтар"
            )

            for error in errors:

                st.error(
                    error
                )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # ЖЕКЕ СҰРАҚ
    # =====================================================

    with tab2:

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
        ].index(corr)

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
                ].append(
                    {
                        "question": q_text,
                        "answers": [
                            a1,
                            a2,
                            a3,
                            a4
                        ],
                        "correct": corr_idx,
                    }
                )

                save_questions()

                st.success(
                    "✨ Сұрақ сақталды!"
                )

            else:

                st.error(
                    "⚠️ Барлық өрістерді толтырыңыз!"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # СҰРАҚ ЖОЮ
    # =====================================================

    with tab3:

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
                f"{i+1}. {q['question'][:60]}...":
                i
                for i, q
                in enumerate(sub_list)
            }

            chosen_q = st.selectbox(
                "Жою үшін сұрақты таңдаңыз:",
                list(q_map.keys())
            )

            if st.button(
                "🗑️ Жою",
                type="primary"
            ):

                sub_list.pop(
                    q_map[chosen_q]
                )

                questions[
                    del_sub
                ] = sub_list

                save_questions()

                st.success(
                    "🗑️ Сұрақ жойылды!"
                )

                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # СТАТИСТИКА
    # =====================================================

    with tab4:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        render_statistics_tab()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 15. ADMIN PANEL
# =========================================================

def admin_page():

    global users

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            '<div class="kasym-title" '
            'style="font-size: 32px;">'
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

    admin_tabs = st.tabs(
        [
            "👥 Қолданушылар тізімі & Жою",
            "➕ Жаңа қолданушы қосу",
            "📊 Оқушылар статистикасы"
        ]
    )


    with admin_tabs[0]:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📋 Тіркелген қолданушылар"
        )

        if not users:

            st.info(
                "Жүйеде қолданушылар жоқ."
            )

        else:

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

                col_info, col_del = st.columns(
                    [4, 1]
                )

                with col_info:

                    st.write(
                        f"• **{u_name}** "
                        f"(@{u_username}) "
                        f"— Рөлі: `{u_role}`"
                    )

                with col_del:

                    if u_username != "kas01":

                        if st.button(
                            "🗑️ Жою",
                            key=f"del_user_{u_username}"
                        ):

                            users = [
                                x
                                for x in users
                                if x.get(
                                    "username"
                                ) != u_username
                            ]

                            save_users(users)

                            st.success(
                                f"@{u_username} "
                                f"жойылды!"
                            )

                            st.rerun()

                    else:

                        st.caption(
                            "Басты админ"
                        )

                st.markdown(
                    "---"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


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
                "moderator",
                "admin"
            ]
        )

        if st.button(
            "Қолданушыны сақтау",
            type="primary"
        ):

            if new_u and new_p:

                if username_exists(
                    new_u.strip()
                ):

                    st.error(
                        "❌ Бұл логин жүйеде бар!"
                    )

                else:

                    users.append(
                        {
                            "username":
                            new_u.strip(),

                            "password":
                            hash_password(
                                new_p.strip()
                            ),

                            "name":
                            new_n.strip(),

                            "role":
                            new_r,

                            "combination":
                            None,
                        }
                    )

                    save_users(users)

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


    with admin_tabs[2]:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        render_statistics_tab()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 16. USER PANEL
# =========================================================

def user_page():

    col1, col2 = st.columns(
        [6, 1]
    )

    with col1:

        st.markdown(
            f'<div class="kasym-title" '
            f'style="font-size: 32px;">'
            f'🎓 Қош келдіңіз, '
            f'{st.session_state.full_name}!'
            f'</div>',
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
        'Оқушы кабинеті және ҰБТ тест тапсыру'
        '</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.test_started:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🎯 Тест комбинациясын таңдаңыз"
        )

        selected_comb = st.selectbox(
            "Мамандық бағытын таңдаңыз:",
            list(combinations.keys())
        )

        if st.button(
            "🚀 Тестті бастау",
            type="primary",
            use_container_width=True
        ):

            st.session_state.active_combination = (
                selected_comb
            )

            st.session_state.test_started = True

            st.session_state.current_subject_index = 0

            st.session_state.test_answers = {}

            st.session_state.result_saved = False

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:

        comb_name = (
            st.session_state.active_combination
        )

        subj_list = combinations[
            comb_name
        ]

        sub_idx = (
            st.session_state.current_subject_index
        )

        if sub_idx < len(subj_list):

            current_subject = (
                subj_list[sub_idx]
            )

            st.markdown(
                f"### 📚 Пән "
                f"({sub_idx + 1}/{len(subj_list)}): "
                f"{current_subject}"
            )

            st.markdown(
                "---"
            )

            sub_questions = questions.get(
                current_subject,
                []
            )

            if not sub_questions:

                st.info(
                    f"Бұл пәнде "
                    f"({current_subject}) "
                    f"әзірге сұрақтар жоқ."
                )

                if st.button(
                    "Келесі пәнге өту ➡"
                ):

                    st.session_state.current_subject_index += 1

                    st.rerun()

            else:

                with st.form(
                    key=f"subject_form_{sub_idx}"
                ):

                    subject_answers = {}

                    for q_idx, q in enumerate(
                        sub_questions
                    ):

                        ans = st.radio(
                            f"{q_idx + 1}. "
                            f"{q['question']}",
                            q["answers"],
                            key=f"q_{sub_idx}_{q_idx}"
                        )

                        subject_answers[
                            q_idx
                        ] = ans

                        st.markdown("")

                    submitted = (
                        st.form_submit_button(
                            "Келесі пәнге өту ➡"
                            if sub_idx < len(
                                subj_list
                            ) - 1
                            else
                            "Тестті аяқтау 🏁"
                        )
                    )

                    if submitted:

                        st.session_state.test_answers[
                            current_subject
                        ] = subject_answers

                        st.session_state.current_subject_index += 1

                        st.rerun()

        else:

            total_score = 0

            for subject in subj_list:

                sub_questions = questions.get(
                    subject,
                    []
                )

                user_sub_ans = (
                    st.session_state.test_answers.get(
                        subject,
                        {}
                    )
                )

                for q_idx, q in enumerate(
                    sub_questions
                ):

                    chosen = user_sub_ans.get(
                        q_idx
                    )

                    correct_text = q[
                        "answers"
                    ][
                        q["correct"]
                    ]

                    if chosen == correct_text:

                        total_score += 1

            if not st.session_state.get(
                "result_saved",
                False
            ):

                history = load_results_history()

                new_result = {

                    "username":
                    st.session_state.username,

                    "name":
                    st.session_state.full_name,

                    "combination":
                    comb_name,

                    "score":
                    total_score,

                    "date":
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }

                history.append(
                    new_result
                )

                save_results_history(
                    history
                )

                st.session_state.result_saved = True

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### 🎉 Тест аяқталды!"
                f" Жинаған ұпайыңыз: "
                f"**{total_score}**"
            )

            st.info(
                "Нәтижеңіз базаға автоматты түрде сақталды."
            )

            if st.button(
                "🔄 Жаңа тест бастау"
            ):

                st.session_state.test_started = False

                st.session_state.current_subject_index = 0

                st.session_state.test_answers = {}

                st.session_state.result_saved = False

                st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# =========================================================
# 17. ROUTER
# =========================================================

def main():

    if not st.session_state.logged_in:

        login_page()

    else:

        role = st.session_state.get(
            "role",
            "user"
        )

        if role == "admin":

            admin_page()

        elif role == "moderator":

            moderator_page()

        elif role == "user":

            user_page()

        else:

            st.warning(
                f"⚠️ Белгісіз рөл анықталды: {role}"
            )

            if st.button(
                "🚪 Шығу және қайта кіру"
            ):

                logout()


# =========================================================
# 18. START
# =========================================================

if __name__ == "__main__":
    main()
