import streamlit as st

# =========================
# БАПТАУЛАР
# =========================

st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "selected_combination" not in st.session_state:
    st.session_state.selected_combination = None

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# =========================
# ПӘНДЕР
# =========================

combinations = {
    "Биология + Химия": ["Биология", "Химия"],
    "Физика + Математика": ["Физика", "Математика"],
    "Информатика + Математика": ["Информатика", "Математика"],
    "Дүниежүзі тарихы + Ағылшын тілі": [
        "Дүниежүзі тарихы",
        "Ағылшын тілі"
    ],
    "Биология + География": ["Биология", "География"],
    "География + Математика": ["География", "Математика"],
    "Дүниежүзі тарихы + Құқық": [
        "Дүниежүзі тарихы",
        "Құқық"
    ]
}

common_subjects = [
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Математикалық сауаттылық"
]

# =========================
# БАРЛЫҚ ПӘНДЕР
# =========================

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
    "Математикалық сауаттылық"
]

# =========================
# СҰРАҚТАР
# =========================

questions = {

    "Информатика": [

        {
            "question": "Python тілінде экранға ақпарат шығару үшін қай функция қолданылады?",
            "answers": ["input()", "print()", "len()", "type()"],
            "correct": "print()"
        },

        {
            "question": "Python тілінде пайдаланушыдан мәлімет енгізу үшін қай функция қолданылады?",
            "answers": ["print()", "input()", "str()", "int()"],
            "correct": "input()"
        },

        {
            "question": "int() функциясының қызметі қандай?",
            "answers": [
                "Мәтінге айналдырады",
                "Бүтін санға айналдырады",
                "Ондық санға айналдырады",
                "Тізім құрады"
            ],
            "correct": "Бүтін санға айналдырады"
        },

        {
            "question": "Python тіліндегі / операторы не үшін қолданылады?",
            "answers": [
                "Қосу",
                "Бөлу",
                "Қалдық табу",
                "Дәрежелеу"
            ],
            "correct": "Бөлу"
        },

        {
            "question": "10 % 3 нәтижесі неге тең?",
            "answers": ["1", "2", "3", "0"],
            "correct": "1"
        },

        {
            "question": "10 // 3 нәтижесі неге тең?",
            "answers": ["1", "2", "3", "3.33"],
            "correct": "3"
        },

        {
            "question": "2 ** 3 нәтижесі неге тең?",
            "answers": ["5", "6", "8", "9"],
            "correct": "8"
        },

        {
            "question": "len() функциясы не үшін қолданылады?",
            "answers": [
                "Элементтер санын анықтау",
                "Сан қосу",
                "Мәтінді өзгерту",
                "Экранға шығару"
            ],
            "correct": "Элементтер санын анықтау"
        },

        {
            "question": "Python тіліндегі and операторының мағынасы қандай?",
            "answers": [
                "немесе",
                "және",
                "емес",
                "тең"
            ],
            "correct": "және"
        },

        {
            "question": "Python тіліндегі or операторының мағынасы қандай?",
            "answers": [
                "және",
                "немесе",
                "емес",
                "тең"
            ],
            "correct": "немесе"
        },

        {
            "question": "if операторы не үшін қолданылады?",
            "answers": [
                "Шарт тексеру үшін",
                "Цикл жасау үшін",
                "Мәтін енгізу үшін",
                "Тізім жасау үшін"
            ],
            "correct": "Шарт тексеру үшін"
        },

        {
            "question": "for циклі не үшін қолданылады?",
            "answers": [
                "Қайталау әрекеттерін орындау үшін",
                "Мәтін енгізу үшін",
                "Санның түрін өзгерту үшін",
                "Бағдарламаны тоқтату үшін"
            ],
            "correct": "Қайталау әрекеттерін орындау үшін"
        },

        {
            "question": "bool(0) нәтижесі қандай?",
            "answers": ["True", "False", "0", "None"],
            "correct": "False"
        },

        {
            "question": "str(25) нәтижесінде не пайда болады?",
            "answers": [
                "25 саны",
                "'25' мәтіні",
                "True",
                "False"
            ],
            "correct": "'25' мәтіні"
        },

        {
            "question": "float(5) нәтижесі қандай?",
            "answers": ["5", "5.0", "'5'", "False"],
            "correct": "5.0"
        },

        {
            "question": "int(7.9) нәтижесі қандай?",
            "answers": ["7", "8", "7.9", "6"],
            "correct": "7"
        },

        {
            "question": "float('3.5') нәтижесі қандай?",
            "answers": ["3", "3.5", "'3.5'", "35"],
            "correct": "3.5"
        },

        {
            "question": "type(7) нәтижесі қандай?",
            "answers": [
                "<class 'float'>",
                "<class 'str'>",
                "<class 'int'>",
                "<class 'bool'>"
            ],
            "correct": "<class 'int'>"
        },

        {
            "question": "[1, 2, 3] қандай мәліметтер құрылымы?",
            "answers": [
                "String",
                "List",
                "Integer",
                "Boolean"
            ],
            "correct": "List"
        },

        {
            "question": "10 % 3 нәтижесі қандай?",
            "answers": ["0", "1", "2", "3"],
            "correct": "1"
        }
    ]
}

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #07111f, #0b1d35);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 5px;
}

.slogan {
    text-align: center;
    font-size: 20px;
    color: #8eb8ff;
    margin-bottom: 35px;
}

.card {
    background: rgba(20, 39, 65, 0.9);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(120,170,255,0.15);
    margin-bottom: 18px;
}

.question-card {
    background: rgba(17, 35, 60, 0.95);
    padding: 30px;
    border-radius: 22px;
    margin-top: 20px;
    border: 1px solid rgba(100,160,255,0.2);
}

.result-card {
    background: rgba(18, 40, 70, 0.95);
    padding: 35px;
    border-radius: 25px;
    text-align: center;
    margin-top: 20px;
}

.big-number {
    font-size: 55px;
    font-weight: 900;
}

.admin-card {
    background: rgba(28, 48, 80, 0.95);
    padding: 28px;
    border-radius: 22px;
    border: 1px solid rgba(100,160,255,0.25);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🎓 KASYM EDU</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="slogan">Бүгінгі дайындық — ертеңгі грант</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("🔐 Кіру")

    username = st.text_input(
        "Логин",
        placeholder="Логинді енгізіңіз"
    )

    password = st.text_input(
        "Құпия сөз",
        type="password",
        placeholder="Құпия сөзді енгізіңіз"
    )

    if st.button(
        "🚀 Кіру",
        use_container_width=True
    ):

        if username and password:

            # ПРЕЗИДЕНТ
            if username == "president" and password == "1234":

                st.session_state.logged_in = True
                st.session_state.role = "president"
                st.session_state.page = "admin"

            # ҚОЛДАНУШЫ
            else:

                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.page = "home"

            st.rerun()

        else:

            st.error(
                "Логин мен құпия сөзді енгізіңіз!"
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# =========================
# НЕГІЗГІ САЙТ
# =========================

else:

    # =========================
    # HEADER
    # =========================

    col1, col2, col3 = st.columns([5, 2, 1])

    with col1:

        st.markdown(
            "## 🎓 KASYM EDU"
        )

    with col2:

        if st.session_state.role == "president":

            st.markdown(
                "### 👑 Президент"
            )

        else:

            st.markdown(
                "### 👤 Қолданушы"
            )

    with col3:

        if st.button("🚪 Шығу"):

            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.page = "login"
            st.rerun()

    st.divider()

    # ==================================================
    # ПРЕЗИДЕНТ ПАНЕЛІ
    # ==================================================

    if st.session_state.role == "president":

        # =========================
        # ADMIN HOME
        # =========================

        if st.session_state.page == "admin":

            st.markdown(
                '<div class="main-title">👑 Президент панелі</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="slogan">KASYM EDU басқару орталығы</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    '<div class="admin-card">',
                    unsafe_allow_html=True
                )

                st.subheader("➕ Сұрақ қосу")

                st.write(
                    "Жаңа ҰБТ сұрағын өзіңіз құрастырыңыз."
                )

                if st.button(
                    "➕ Жаңа сұрақ құрастыру",
                    use_container_width=True
                ):

                    st.session_state.page = "add_question"
                    st.rerun()

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    '<div class="admin-card">',
                    unsafe_allow_html=True
                )

                st.subheader("📋 Сұрақтар")

                total_questions = sum(
                    len(q)
                    for q in questions.values()
                )

                st.markdown(
                    f"### {total_questions} сұрақ"
                )

                st.write(
                    "Қазіргі сұрақтар базасын көріңіз."
                )

                if st.button(
                    "📋 Сұрақтарды көру",
                    use_container_width=True
                ):

                    st.session_state.page = "question_list"
                    st.rerun()

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            st.write("")

            if st.button(
                "🌐 Қолданушы режиміне өту",
                use_container_width=True
            ):

                st.session_state.role = "user"
                st.session_state.page = "home"
                st.rerun()

        # =========================
        # ADD QUESTION
        # =========================

        elif st.session_state.page == "add_question":

            st.title("➕ Жаңа сұрақ құрастыру")

            st.write(
                "Төмендегі ақпараттарды толтырыңыз."
            )

            st.markdown(
                '<div class="admin-card">',
                unsafe_allow_html=True
            )

            subject = st.selectbox(
                "📚 Пәнді таңдаңыз",
                all_subjects
            )

            question_text = st.text_area(
                "❓ Сұрақ мәтіні",
                placeholder="Мысалы: Python тілінде print() функциясы не үшін қолданылады?"
            )

            st.write("### 🔘 Жауап нұсқалары")

            answer1 = st.text_input(
                "A)",
                placeholder="Бірінші жауап"
            )

            answer2 = st.text_input(
                "B)",
                placeholder="Екінші жауап"
            )

            answer3 = st.text_input(
                "C)",
                placeholder="Үшінші жауап"
            )

            answer4 = st.text_input(
                "D)",
                placeholder="Төртінші жауап"
            )

            st.write("")

            correct_answer = st.radio(
                "✅ Дұрыс жауапты таңдаңыз",
                [
                    "A",
                    "B",
                    "C",
                    "D"
                ],
                horizontal=True
            )

            st.write("")

            if st.button(
                "💾 Сұрақты сақтау",
                use_container_width=True
            ):

                if not question_text:

                    st.error(
                        "❌ Сұрақ мәтінін енгізіңіз!"
                    )

                elif not answer1 or not answer2 or not answer3 or not answer4:

                    st.error(
                        "❌ 4 жауаптың барлығын енгізіңіз!"
                    )

                else:

                    answers = [
                        answer1,
                        answer2,
                        answer3,
                        answer4
                    ]

                    correct_index = {
                        "A": 0,
                        "B": 1,
                        "C": 2,
                        "D": 3
                    }

                    new_question = {

                        "question": question_text,

                        "answers": answers,

                        "correct": answers[
                            correct_index[correct_answer]
                        ]
                    }

                    if subject not in questions:

                        questions[subject] = []

                    questions[subject].append(
                        new_question
                    )

                    st.success(
                        "✅ Сұрақ сәтті қосылды!"
                    )

                    st.session_state.page = "question_list"

                    st.rerun()

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "⬅️ Президент панеліне қайту",
                use_container_width=True
            ):

                st.session_state.page = "admin"
                st.rerun()

        # =========================
        # QUESTION LIST
        # =========================

        elif st.session_state.page == "question_list":

            st.title("📋 Сұрақтар базасы")

            total_questions = sum(
                len(q)
                for q in questions.values()
            )

            st.write(
                f"Барлығы: **{total_questions} сұрақ**"
            )

            for subject, subject_questions in questions.items():

                if subject_questions:

                    st.subheader(
                        f"📚 {subject}"
                    )

                    for i, question in enumerate(
                        subject_questions
                    ):

                        with st.expander(
                            f"{i + 1}. {question['question']}"
                        ):

                            st.write(
                                "### Жауаптар:"
                            )

                            for answer in question["answers"]:

                                if answer == question["correct"]:

                                    st.success(
                                        f"✅ {answer}"
                                    )

                                else:

                                    st.write(
                                        f"▫️ {answer}"
                                    )

            st.write("")

            if st.button(
                "➕ Тағы сұрақ қосу",
                use_container_width=True
            ):

                st.session_state.page = "add_question"
                st.rerun()

            if st.button(
                "⬅️ Президент панелі",
                use_container_width=True
            ):

                st.session_state.page = "admin"
                st.rerun()

    # ==================================================
    # ҚОЛДАНУШЫ БӨЛІМІ
    # ==================================================

    else:

        # =========================
        # HOME
        # =========================

        if st.session_state.page == "home":

            st.markdown(
                '<div class="main-title">ҰБТ дайындық орталығы</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="slogan">Бүгінгі дайындық — ертеңгі грант</div>',
                unsafe_allow_html=True
            )

            st.subheader("📚 Пәндер комбинациясы")

            for combination in combinations:

                if st.button(
                    f"📖 {combination}   →",
                    key=f"comb_{combination}",
                    use_container_width=True
                ):

                    st.session_state.selected_combination = combination
                    st.session_state.page = "combination"
                    st.rerun()

        # =========================
        # COMBINATION
        # =========================

        elif st.session_state.page == "combination":

            combination = st.session_state.selected_combination

            st.title(
                f"📚 {combination}"
            )

            st.subheader(
                "🎯 Негізгі пәндер"
            )

            main_subjects = combinations[
                combination
            ]

            for subject in main_subjects:

                if st.button(
                    f"📘 {subject}   →",
                    key=f"main_{subject}",
                    use_container_width=True
                ):

                    st.session_state.selected_subject = subject
                    st.session_state.current_question = 0
                    st.session_state.user_answers = {}
                    st.session_state.page = "test"
                    st.rerun()

            st.subheader(
                "📌 Міндетті пәндер"
            )

            for subject in common_subjects:

                if st.button(
                    f"📗 {subject}   →",
                    key=f"common_{subject}",
                    use_container_width=True
                ):

                    st.session_state.selected_subject = subject
                    st.session_state.current_question = 0
                    st.session_state.user_answers = {}
                    st.session_state.page = "test"
                    st.rerun()

            st.write("")

            if st.button("⬅️ Артқа"):

                st.session_state.page = "home"
                st.rerun()

        # =========================
        # TEST
        # =========================

        elif st.session_state.page == "test":

            subject = st.session_state.selected_subject

            if subject not in questions:

                st.warning(
                    f"⚠️ {subject} пәнінің сұрақтары әлі қосылған жоқ."
                )

                if st.button("⬅️ Артқа"):

                    st.session_state.page = "combination"
                    st.rerun()

            else:

                subject_questions = questions[
                    subject
                ]

                current_index = st.session_state.current_question

                current = subject_questions[
                    current_index
                ]

                st.markdown(
                    f"## 📘 {subject}"
                )

                st.markdown(
                    "### 📝 ҰБТ тесті"
                )

                st.progress(
                    (current_index + 1)
                    / len(subject_questions)
                )

                st.write(
                    f"### Сұрақ {current_index + 1} / "
                    f"{len(subject_questions)}"
                )

                st.markdown(
                    '<div class="question-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"### {current['question']}"
                )

                saved_answer = (
                    st.session_state.user_answers.get(
                        current_index,
                        None
                    )
                )

                if saved_answer in current["answers"]:

                    default_index = (
                        current["answers"].index(
                            saved_answer
                        )
                    )

                else:

                    default_index = None

                answer = st.radio(
                    "Жауабыңызды таңдаңыз:",
                    current["answers"],
                    index=default_index,
                    key=f"question_{current_index}"
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                st.write("")

                if st.button(
                    "Келесі →",
                    use_container_width=True
                ):

                    if answer is None:

                        st.warning(
                            "Алдымен жауапты таңдаңыз!"
                        )

                    else:

                        st.session_state.user_answers[
                            current_index
                        ] = answer

                        if (
                            current_index + 1
                            < len(subject_questions)
                        ):

                            st.session_state.current_question += 1
                            st.rerun()

                        else:

                            st.session_state.page = "result"
                            st.rerun()

        # =========================
        # RESULT
        # =========================

        elif st.session_state.page == "result":

            subject = st.session_state.selected_subject

            subject_questions = questions[
                subject
            ]

            correct_count = 0

            wrong_questions = []

            for i, question in enumerate(
                subject_questions
            ):

                user_answer = (
                    st.session_state.user_answers.get(
                        i,
                        None
                    )
                )

                if user_answer == question["correct"]:

                    correct_count += 1

                else:

                    wrong_questions.append({

                        "number": i + 1,

                        "question": question["question"],

                        "user_answer": user_answer,

                        "correct_answer": question["correct"]
                    })

            total = len(
                subject_questions
            )

            percentage = int(
                correct_count / total * 100
            )

            wrong_count = (
                total - correct_count
            )

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                "## 🎯 Тест аяқталды"
            )

            st.markdown(
                f'<div class="big-number">{percentage}%</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### Дұрыс жауап: "
                f"{correct_count} / {total}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.success(
                    f"✅ Дұрыс: {correct_count}"
                )

            with col2:

                st.error(
                    f"❌ Қате: {wrong_count}"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.write("")

            if wrong_questions:

                st.markdown(
                    "## ❌ Қате кеткен сұрақтар"
                )

                for item in wrong_questions:

                    with st.expander(
                        f"❌ Сұрақ {item['number']}"
                    ):

                        st.markdown(
                            f"### {item['question']}"
                        )

                        st.write("")

                        st.markdown(
                            f"🔴 **Сіздің жауабыңыз:** "
                            f"{item['user_answer']}"
                        )

                        st.markdown(
                            f"🟢 **Дұрыс жауап:** "
                            f"{item['correct_answer']}"
                        )

            else:

                st.success(
                    "🔥 Керемет! Барлық сұраққа дұрыс жауап бердіңіз!"
                )

            st.write("")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🔄 Тестті қайта тапсыру",
                    use_container_width=True
                ):

                    st.session_state.current_question = 0
                    st.session_state.user_answers = {}
                    st.session_state.page = "test"
                    st.rerun()

            with col2:

                if st.button(
                    "⬅️ Пәндерге қайту",
                    use_container_width=True
                ):

                    st.session_state.current_question = 0
                    st.session_state.user_answers = {}
                    st.session_state.page = "combination"
                    st.rerun()
