import json
import os
import datetime
import hashlib
import re
import streamlit as st

# =========================================================
# KASYM EDU CONFIG
# =========================================================
st.set_page_config(
    page_title="KASYM EDU",
    page_icon="🎓",
    layout="wide"
)

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"

# =========================================================
# ПАРОЛЬДІ ХЭШТЕУ
# =========================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# ПӘНДЕР МЕН КОМБИНАЦИЯЛАР
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

default_questions = {
    "Информатика": [
        {
            "question": "Python тілінде экранға мәтін шығару үшін қай функция қолданылады?",
            "answers": ["input()", "print()", "output()", "write()"],
            "correct": 1,
        }
    ]
}

# =========================================================
# АККАУНТ ЖҮЙЕСІ
# =========================================================
def default_users():
    return [
        {
            "username": "kas01",
            "password": hash_password("kasko100228550357"),
            "name": "KASYM",
            "role": "president",
            "combination": None,
        }
    ]

def save_users(users_list):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users_list, file, ensure_ascii=False, indent=4)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    users_list = default_users()
    save_users(users_list)
    return users_list

users = load_users()

def find_user(username, password):
    hashed_input = hash_password(password)
    for user in users:
        stored = user.get("password")
        if user.get("username") == username and (stored == hashed_input or stored == password):
            return user
    return None

# =========================================================
# СҰРАҚТАР МЕН НӘТИЖЕЛЕР
# =========================================================
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                for sub in all_subjects:
                    if sub not in data: data[sub] = []
                return data
        except Exception:
            return default_questions.copy()
    return default_questions.copy()

def save_questions():
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

questions = load_questions()

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = None
if "username" not in st.session_state: st.session_state.username = ""
if "full_name" not in st.session_state: st.session_state.full_name = ""
if "page" not in st.session_state: st.session_state.page = "login"

# =========================================================
# ТҰРАҚТЫ ҚАРАҢҒЫ РЕЖИМ СТИЛІ (DARK MODE)
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
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
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
        background-color: #1E293B;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background-color: #1E293B;
        color: #F3F4F6;
    }
    .stButton>button:hover {
        border-color: #6366F1;
        color: #6366F1;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #1E293B !important;
        border-radius: 10px !important;
        color: #F3F4F6 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "login"
    st.rerun()

# =========================================================
# LOGIN БЕТІ
# =========================================================
def login_page():
    st.markdown('<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🔐 Жүйеге кіру</h3>", unsafe_allow_html=True)
        username = st.text_input("Логин", key="login_username")
        password = st.text_input("Құпия сөз", type="password", key="login_password")

        if st.button("Кіру →", use_container_width=True, type="primary"):
            user = find_user(username.strip(), password.strip())
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.full_name = user.get("name", "")
                st.session_state.role = user.get("role", "user")
                st.session_state.page = "admin" if user["role"] == "president" else ("prime_minister" if user["role"] == "prime_minister" else "home")
                st.rerun()
            else:
                st.error("❌ Логин немесе құпия сөз қате.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# АҚЫЛДЫ АВТО-ПАРСЕР ФУНКЦИЯСЫ (Мәтіннен 40+ сұрақты бөліп алу)
# =========================================================
def parse_bulk_questions(raw_text):
    questions_list = []
    blocks = re.split(r'\n\s*(?=\d+[\.\)])', raw_text)
    
    for block in blocks:
        if not block.strip():
            continue
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        if len(lines) < 5:
            continue
            
        q_text = lines[0]
        q_text = re.sub(r'^\d+[\.\)]\s*', '', q_text)
        
        answers = []
        correct_index = 0
        
        for idx, line in enumerate(lines[1:5]):
            match = re.match(r'^([A-DА-Гa-dа-г])[\.\)]\s*(.*)', line, re.IGNORECASE)
            if match:
                opt_letter = match.group(1).upper()
                opt_text = match.group(2)
                answers.append(opt_text)
                if "*" in line or "(+)" in line or "Дұрыс" in line:
                    if opt_letter in ['A', 'А']: correct_index = idx
                    elif opt_letter in ['B', 'Б']: correct_index = idx
                    elif opt_letter in ['C', 'В']: correct_index = idx
                    elif opt_letter in ['D', 'Г']: correct_index = idx
            else:
                answers.append(line)
        
        if len(answers) >= 4:
            questions_list.append({
                "question": q_text,
                "answers": answers[:4],
                "correct": correct_index
            })
            
    return questions_list

# =========================================================
# ПРЕМЬЕР-МИНИСТР ПАНЕЛІ (СҰРАҚ ҚОСУ ЖӘНЕ АВТО-ЖҮКТЕУ)
# =========================================================
def prime_minister_page():
    if st.button("🚪 Шығу"): logout()
    
    st.markdown('<div class="kasym-title" style="font-size: 32px;">➕ Сұрақтарды басқару панелі</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Жалғызлап немесе 40-50 сұрақты бірден автоматты түрде жүктеңіз</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⚡ Жылдам массалық жүктеу (Авто-парсер)", "✍️ Жеке сұрақ қосу"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_subject_bulk = st.selectbox("📚 Пәнді таңдаңыз (Авто-жүктеу):", all_subjects, key="bulk_sub")
        st.info("💡 **Үлгі формат:**\n1. 2 + 2 өрнегінің мәні?\nA) 2\nB) 4\nC) 5\nD) 3")

        raw_text_input = st.text_area(
            "✍️ Барлық сұрақтарды осында көшіріп қойыңыз (Ctrl + V):", 
            height=250,
            placeholder="1. Сұрақ...\nA) ...\nB) ...\nC) ...\nD) ..."
        )

        if st.button("🚀 Барлық сұрақтарды бірден базаға қосу", use_container_width=True, type="primary"):
            if raw_text_input.strip():
                parsed_questions = parse_bulk_questions(raw_text_input)
                if parsed_questions:
                    if selected_subject_bulk not in questions:
                        questions[selected_subject_bulk] = []
                    questions[selected_subject_bulk].extend(parsed_questions)
                    save_questions()
                    st.success(f"✨ Сәтті! Барлығы **{len(parsed_questions)}** сұрақ автоматты түрде қосылды!")
                else:
                    st.error("⚠️ Сұрақтар форматын тану мүмкін болмады. Үлгіге сәйкестігін тексеріңіз.")
            else:
                st.warning("⚠️ Мәтін өрісі бос болмауы тиіс!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_subject = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects, key="single_sub")
        question_text = st.text_area("✍️ Сұрақты толық жазыңыз:", placeholder="Мысалы: Фотосинтез процесі қай органоидта жүреді?")

        col_a, col_b = st.columns(2)
        with col_a:
            ans1 = st.text_input("А нұсқасы:")
            ans3 = st.text_input("В нұсқасы:")
        with col_b:
            ans2 = st.text_input("Б нұсқасы:")
            ans4 = st.text_input("Г нұсқасы:")

        correct_option = st.selectbox("✅ Дұрыс жауап қайсысы?", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"])
        correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(correct_option)

        if st.button("💾 Сұрақты базаға сақтау", use_container_width=True, type="primary"):
            if question_text and ans1 and ans2 and ans3 and ans4:
                new_q = {
                    "question": question_text,
                    "answers": [ans1, ans2, ans3, ans4],
                    "correct": correct_index,
                }
                if selected_subject not in questions:
                    questions[selected_subject] = []
                questions[selected_subject].append(new_q)
                save_questions()
                st.success("✨ Сұрақ сәтті сақталды!")
            else:
                st.error("⚠️ Барлық өрістерді толық толтырыңыз!")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ПРЕЗИДЕНТ ПАНЕЛІ
# =========================================================
def admin_page():
    if st.button("🚪 Шығу"): logout()
    st.markdown('<div class="kasym-title" style="font-size: 32px;">👑 Президент панелі</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Жүйені басқару және бақылау орталығы</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"Қош келдіңіз, **{st.session_state.full_name}**! Мұнда барлық статистика мен қолданушылар тізімі көрсетіледі.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ОҚУШЫНЫҢ БАСТЫ БЕТІ
# =========================================================
def home_page():
    if st.button("🚪 Шығу"): logout()
    st.markdown('<div class="kasym-title" style="font-size: 32px;">🏠 Басты бет (Оқушы)</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">ҰБТ-ға дайындық және тест тапсыру бөлімі</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"Сәлем, **{st.session_state.full_name}**! Тест тапсыру парақтары мен пәндерді осы жерден таңдайсыз.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# РОУТЕР
# =========================================================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        p = st.session_state.page
        if p == "admin": admin_page()
        elif p == "prime_minister": prime_minister_page()
        else: home_page()

if __name__ == "__main__":
    main()
