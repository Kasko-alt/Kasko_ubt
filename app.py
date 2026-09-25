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

.wrong-card {
    background: rgba(70, 25, 35, 0.85);
    padding: 22px;
    border-radius: 18px;
    margin-top: 15px;
    border-left: 5px solid #ff5c6c;
}

.correct-card {
    background: rgba(20, 70, 45, 0.85);
    padding: 22px;
    border-radius: 18px;
    margin-top: 15px;
    border-left: 5px solid #42e695;
}

.big-number {
    font-size: 55px;
    font-weight: 900;
}

.small-text {
    color: #aabbd5;
    font-size: 17px;
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

    st.markdown('<div class="card">', unsafe_allow_html=True)

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

    if st.button("🚀 Кіру", use_container_width=True):

        if username and password:
            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.rerun()

        else:
            st.error("Логин мен құпия сөзді енгізіңіз!")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# НЕГІЗГІ САЙТ
# =========================

else:

    # HEADER

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown(
            "## 🎓 KASYM EDU"
        )

    with col2:
        if st.button("🚪 Шығу"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.divider()

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

        st.title(f"📚 {combination}")

        st.write("")

        st.subheader("🎯 Негізгі пәндер")

        main_subjects = combinations[combination]

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

        st.subheader("📌 Міндетті пәндер")

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

            subject_questions = questions[subject]

            current_index = st.session_state.current_question

            current = subject_questions[current_index]

            st.markdown(
                f"## 💻 {subject}"
            )

            st.markdown(
                "### 📝 ҰБТ тесті"
            )

            st.progress(
                (current_index + 1) / len(subject_questions)
            )

            st.write(
                f"### Сұрақ {current_index + 1} / {len(subject_questions)}"
            )

            st.markdown(
                '<div class="question-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### {current['question']}"
            )

            saved_answer = st.session_state.user_answers.get(
                current_index,
                None
            )

            if saved_answer in current["answers"]:
                default_index = current["answers"].index(saved_answer)
            else:
                default_index = None

            answer = st.radio(
                "Жауабыңызды таңдаңыз:",
                current["answers"],
                index=default_index,
                key=f"question_{current_index}"
            )

            st.markdown('</div>', unsafe_allow_html=True)

            st.write("")

            if st.button(
                "Келесі →",
                use_container_width=True
            ):

                if answer is None:

                    st.warning("Алдымен жауапты таңдаңыз!")

                else:

                    st.session_state.user_answers[
                        current_index
                    ] = answer

                    if current_index + 1 < len(subject_questions):

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

        subject_questions = questions[subject]

        correct_count = 0
        wrong_questions = []

        for i, question in enumerate(subject_questions):

            user_answer = st.session_state.user_answers.get(
                i,
                None
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

        total = len(subject_questions)

        percentage = int(
            correct_count / total * 100
        )

        wrong_count = total - correct_count

        # НӘТИЖЕ

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("## 🎯 Тест аяқталды")

        st.markdown(
            f'<div class="big-number">{percentage}%</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"### Дұрыс жауап: {correct_count} / {total}"
        )

        st.write("")

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

        # =========================
        # ҚАТЕ СҰРАҚТАР
        # =========================

        if wrong_questions:

            st.markdown("## ❌ Қате кеткен сұрақтар")

            st.write(
                "Төменнен қай сұрақтарда қате кеткеніңізді көре аласыз:"
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

                    st.write("")

                    st.info(
                        "Бұл сұрақты қайта қарап шығыңыз."
                    )

        else:

            st.success(
                "🔥 Керемет! Барлық сұраққа дұрыс жауап бердіңіз!"
            )

        st.write("")

        # =========================
        # БАТЫРМАЛАР
        # =========================

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
