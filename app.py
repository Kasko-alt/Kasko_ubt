import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Білім беру жүйесі",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM CSS STYLES (БАШТАПКЫ КООЗ ДИЗАЙН)
# =========================================================
st.markdown("""
<style>
    /* Негизги фон жана шрифтер */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Карточкалар (Glassmorphism / Neon style) */
    .custom-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.25);
        border: 1px solid rgba(99, 102, 241, 0.4);
    }

    /* Колдонуучунун профиль карточкасы */
    .user-profile-bar {
        background: linear-gradient(90deg, #312e81 0%, #4c1d95 100%);
        padding: 12px 24px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
    }

    /* Баскычтар (Buttons) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease-in-out !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Форма киргизүү талаалары */
    .stTextInput > div > div > input, 
    .stTextArea textarea, 
    .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus, 
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
    }

    /* Заголовкалар жана тексттер */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Метрикалар (Статистика) */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA FILES & INIT
# =========================================================
USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"

DEFAULT_USERS = {
    "president": {"password": "123", "role": "president", "name": "Президент"},
    "pm": {"password": "123", "role": "prime_minister", "name": "Премьер-министр"},
    "student1": {"password": "123", "role": "student", "name": "Асан Әли"}
}

DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "subject": "Математика",
        "question": "5 + 7 = ?",
        "options": ["10", "11", "12", "13"],
        "answer": "12"
    },
    {
        "id": 2,
        "subject": "Қазақстан тарихы",
        "question": "Қазақ хандығы қашан құрылды?",
        "options": ["1465 жыл", "1500 жыл", "1300 жыл", "1750 жыл"],
        "answer": "1465 жыл"
    }
]

def load_json(filepath, default_data):
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default_data

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

users_db = load_json(USERS_FILE, DEFAULT_USERS)
questions_db = load_json(QUESTIONS_FILE, DEFAULT_QUESTIONS)
results_db = load_json(RESULTS_FILE, [])

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_test" not in st.session_state:
    st.session_state.current_test = None
if "test_answers" not in st.session_state:
    st.session_state.test_answers = {}
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =========================================================
# NAVBAR & USER BAR
# =========================================================
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.page = "login"
    st.session_state.current_test = None
    st.rerun()

def top_logout_button():
    user_info = users_db.get(st.session_state.username, {})
    display_name = user_info.get("name", st.session_state.username)
    
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f"""
        <div class="user-profile-bar">
            <span>✨ Пайдаланушы: <b>{st.session_state.username}</b> ({display_name})</span>
            <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 12px; text-transform: uppercase;">
                {st.session_state.role}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Шығу", key="top_logout"):
            logout()

# =========================================================
# PAGES
# =========================================================
def login_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🔐 Жүйеге кіру</h1>", unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        username_input = st.text_input("👤 Пайдаланушы аты (Username)")
        password_input = st.text_input("🔑 Құпия сөз", type="password")
        
        st.write("")
        if st.button("🚀 Кіру", use_container_width=True):
            if username_input in users_db and users_db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = users_db[username_input]["role"]
                st.session_state.page = "home"
                st.success("Сәтті кірдіңіз!")
                st.rerun()
            else:
                st.error("Логин немесе құпия сөз қате!")
        st.markdown('</div>', unsafe_allow_html=True)

def home_page():
    user_info = users_db.get(st.session_state.username, {})
    display_name = user_info.get("name", st.session_state.username)
    role = st.session_state.role

    st.markdown(f"""
    <div class="custom-card">
        <h1>Қош келдіңіз, <span class="gradient-text">{display_name}</span>! 👋</h1>
        <p style="color: #94a3b8; font-size: 16px;">Системадағы ролуңуз: <b>{role.upper()}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📌 Негізгі бөлімдер")
    
    if role == "president":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if st.button("👑 Президент Басқару Панелі"):
            st.session_state.page = "admin"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    if role == "prime_minister":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if st.button("🏛 Премьер-Министр Панелі"):
            st.session_state.page = "prime_minister"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📝 Сұрақ-Жауап")
        if st.button("📝 Тест тапсыру", use_container_width=True):
            st.session_state.page = "combination"
            st.rerun()
        st.write("")
        if st.button("📚 Сұрақтар тізімі", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📊 Аналитика")
        if st.button("📊 Нәтижелер тарихы", use_container_width=True):
            st.session_state.page = "results_history"
            st.rerun()
        st.write("")
        if st.button("📈 Прогресс және Статистика", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def admin_page():
    st.markdown("<h1>👑 Президент Басқару Панелі</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Жаңа пайдаланушы қосу", use_container_width=True):
            st.session_state.page = "create_user"
            st.rerun()
    with col2:
        if st.button("👥 Пайдаланушылар тізімі", use_container_width=True):
            st.session_state.page = "users_list"
            st.rerun()
    with col3:
        if st.button("⬅️ Басты бетке қайту", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def create_user_page():
    st.markdown("<h1>➕ Жаңа пайдаланушы тіркеу</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    new_username = st.text_input("Логин")
    new_name = st.text_input("Аты-жөні")
    new_password = st.text_input("Құпия сөз", type="password")
    new_role = st.selectbox("Рөлі", ["student", "prime_minister", "president"])
    
    st.write("")
    if st.button("💾 Тіркеу"):
        if new_username in users_db:
            st.error("Бұл логин мурда тіркелген!")
        elif new_username and new_password:
            users_db[new_username] = {
                "password": new_password,
                "role": new_role,
                "name": new_name or new_username
            }
            save_json(USERS_FILE, users_db)
            st.success("Пайдаланушы сәтті қосылды!")
        else:
            st.warning("Барлық талааларды толтырыңыз.")
    st.markdown('</div>', unsafe_allow_html=True)
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "admin"
        st.rerun()

def users_list_page():
    st.markdown("<h1>👥 Пайдаланушылар тізімі</h1>", unsafe_allow_html=True)
    
    data = []
    for uname, info in users_db.items():
        data.append({"Логин": uname, "Аты-жөні": info.get("name", ""), "Рөлі": info.get("role", "")})
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.table(pd.DataFrame(data))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ Артқа"):
        st.session_state.page = "admin"
        st.rerun()

def prime_minister_page():
    st.markdown("<h1>🏛 Премьер-Министр Панелі</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Жаңа сұрақ қосу", use_container_width=True):
            st.session_state.page = "add_question"
            st.rerun()
    with col2:
        if st.button("⬅️ Басты бетке қайту", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

def add_question_page():
    st.markdown("<h1>➕ Жаңа тест сұрағын қосу</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    subject = st.text_input("Пән атауы (мисалы: Математика, Физика)")
    question_text = st.text_area("Сұрақ мәтіні")
    
    col1, col2 = st.columns(2)
    with col1:
        opt1 = st.text_input("Вариант A")
        opt2 = st.text_input("Вариант B")
    with col2:
        opt3 = st.text_input("Вариант C")
        opt4 = st.text_input("Вариант D")
    
    correct = st.selectbox("Дұрыс жауапты таңдаңыз", [opt1, opt2, opt3, opt4])
    
    st.write("")
    if st.button("💾 Сақтау"):
        if subject and question_text and opt1 and opt2 and opt3 and opt4:
            new_id = max([q["id"] for q in questions_db], default=0) + 1
            new_q = {
                "id": new_id,
                "subject": subject,
                "question": question_text,
                "options": [opt1, opt2, opt3, opt4],
                "answer": correct
            }
            questions_db.append(new_q)
            save_json(QUESTIONS_FILE, questions_db)
            st.success("Сұрақ сәтті қосылды!")
        else:
            st.warning("Барлық өрістерді толтырыңыз!")
    st.markdown('</div>', unsafe_allow_html=True)
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "prime_minister"
        st.rerun()

def question_list_page():
    st.markdown("<h1>📚 Сұрақтар тізімі</h1>", unsafe_allow_html=True)
    
    if not questions_db:
        st.info("Қорда сұрақтар жоқ.")
    else:
        for idx, q in enumerate(questions_db, start=1):
            with st.expander(f"{idx}. [{q['subject']}] {q['question']}"):
                for opt in q["options"]:
                    if opt == q["answer"]:
                        st.markdown(f"- <span style='color: #4ade80; font-weight: bold;'>{opt} (Дұрыс жауап)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {opt}")
                        
    st.write("")
    if st.button("⬅️ Басты бетке қайту"):
        st.session_state.page = "home"
        st.rerun()

def combination_page():
    st.markdown("<h1>📝 Тест түрін таңдау</h1>", unsafe_allow_html=True)
    
    subjects = list(set(q["subject"] for q in questions_db))
    
    if not subjects:
        st.warning("Базада сұрақтар жоқ!")
        if st.button("⬅️ Басты бет"):
            st.session_state.page = "home"
            st.rerun()
        return

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    selected_subject = st.selectbox("Пәнді таңдаңыз:", subjects)
    st.write("")
    if st.button("🚀 Тестті бастау"):
        filtered_qs = [q for q in questions_db if q["subject"] == selected_subject]
        st.session_state.current_test = filtered_qs
        st.session_state.test_answers = {}
        st.session_state.page = "test"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

def test_page():
    questions = st.session_state.current_test
    if not questions:
        st.warning("Сұрақтар табылмады.")
        st.session_state.page = "home"
        st.rerun()
        return

    st.markdown(f"<h1>✍️ Тест: <span class='gradient-text'>{questions[0]['subject']}</span></h1>", unsafe_allow_html=True)
    
    for i, q in enumerate(questions):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(f"### {i+1}-сұрақ: {q['question']}")
        ans = st.radio(
            "Жауапты таңдаңыз:", 
            q["options"], 
            key=f"q_{q['id']}", 
            index=None
        )
        if ans:
            st.session_state.test_answers[q["id"]] = ans
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🎯 Тестті аяқтау"):
        score = 0
        total = len(questions)
        for q in questions:
            user_ans = st.session_state.test_answers.get(q["id"])
            if user_ans == q["answer"]:
                score += 1
                
        percent = round((score / total) * 100, 1)
        
        result_record = {
            "username": st.session_state.username,
            "subject": questions[0]['subject'],
            "score": score,
            "total": total,
            "percent": percent,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        results_db.append(result_record)
        save_json(RESULTS_FILE, results_db)
        
        st.session_state.last_result = result_record
        st.session_state.page = "result"
        st.rerun()

def result_page():
    st.markdown("<h1>🎯 Тест нәтижесі</h1>", unsafe_allow_html=True)
    res = st.session_state.last_result
    
    if res:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Пән", res["subject"])
        col2.metric("Дұрыс жауаптар", f"{res['score']} / {res['total']}")
        col3.metric("Нәтиже", f"{res['percent']}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if res["percent"] >= 70:
            st.balloons()
            st.success("Өте жақсы нәтиже! 🥳")
        else:
            st.warning("Үйренуді жалғастырыңыз! 📚")
            
    if st.button("🏠 Басты бетке оралу"):
        st.session_state.page = "home"
        st.rerun()

def results_history_page():
    st.markdown("<h1>📊 Нәтижелер тарихы</h1>", unsafe_allow_html=True)
    
    if st.session_state.role == "president":
        user_results = results_db
    else:
        user_results = [r for r in results_db if r["username"] == st.session_state.username]
        
    if not user_results:
        st.info("Тарих бос.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        df = pd.DataFrame(user_results)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

def progress_page():
    st.markdown("<h1>📈 Прогресс және Статистика</h1>", unsafe_allow_html=True)
    
    user_results = [r for r in results_db if r["username"] == st.session_state.username]
    
    if not user_results:
        st.info("Аналитика жасау үшін әлі тест тапсырмадыңыз.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        df = pd.DataFrame(user_results)
        st.subheader("Динамика (Пайыз бойынша)")
        st.line_chart(df.set_index("date")["percent"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

# =========================================================
# ROUTING
# =========================================================

if st.session_state.logged_in:
    top_logout_button()

if not st.session_state.logged_in:
    login_page()
else:
    pg = st.session_state.page

    if pg == "admin":
        if st.session_state.role == "president":
            admin_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "create_user":
        if st.session_state.role == "president":
            create_user_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "users_list":
        if st.session_state.role == "president":
            users_list_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "prime_minister":
        if st.session_state.role == "prime_minister":
            prime_minister_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "add_question":
        if st.session_state.role == "prime_minister":
            add_question_page()
        else:
            st.session_state.page = "home"
            st.rerun()

    elif pg == "question_list":
        question_list_page()

    elif pg == "results_history":
        results_history_page()

    elif pg == "progress":
        progress_page()

    elif pg == "combination":
        combination_page()

    elif pg == "test":
        test_page()

    elif pg == "result":
        result_page()

    else:
        home_page()
