import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Білім беру жүйесі",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# CUSTOM CSS STYLES
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }

    .custom-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .user-profile-bar {
        background: linear-gradient(90deg, #312e81 0%, #4c1d95 100%);
        padding: 12px 24px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin-bottom: 25px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
        border: none !important;
        transition: all 0.3s ease-in-out !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        transform: translateY(-2px);
    }

    .stTextInput > div > div > input, 
    .stTextArea textarea, 
    .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
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
            data = json.load(f)
            return data
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
# NAVBAR
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
    st.markdown("<h1 style='text-align: center;'>🔐 Жүйеге кіру</h1>", unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
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

def home_page():
    user_info = users_db.get(st.session_state.username, {})
    display_name = user_info.get("name", st.session_state.username)
    role = st.session_state.role

    st.markdown(f"<h1>Қош келдіңіз, <span style='color: #818cf8;'>{display_name}</span>! 👋</h1>", unsafe_allow_html=True)
    st.info(f"Сіздің жүйедегі рөліңіз: **{role.upper()}**")

    st.markdown("### 📌 Негізгі бөлімдер")
    
    if role == "president":
        if st.button("👑 Президент Басқару Панелі"):
            st.session_state.page = "admin"
            st.rerun()
            
    if role == "prime_minister":
        if st.button("🏛 Премьер-Министр Панелі"):
            st.session_state.page = "prime_minister"
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Сұрақ-Жауап")
        if st.button("📝 Тест тапсыру", use_container_width=True):
            st.session_state.page = "combination"
            st.rerun()
        st.write("")
        if st.button("📚 Сұрақтар тізімі", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()
            
    with col2:
        st.subheader("📊 Аналитика")
        if st.button("📊 Нәтижелер тарихы", use_container_width=True):
            st.session_state.page = "results_history"
            st.rerun()
        st.write("")
        if st.button("📈 Прогресс және Статистика", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()

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
    
    new_username = st.text_input("Логин")
    new_name = st.text_input("Аты-жөні")
    new_password = st.text_input("Құпия сөз", type="password")
    new_role = st.selectbox("Рөлі", ["student", "prime_minister", "president"])
    
    st.write("")
    if st.button("💾 Тіркеу"):
        if new_username in users_db:
            st.error("Бұл логин бұрын тіркелген!")
        elif new_username and new_password:
            users_db[new_username] = {
                "password": new_password,
                "role": new_role,
                "name": new_name or new_username
            }
            save_json(USERS_FILE, users_db)
            st.success("Пайдаланушы сәтті қосылды!")
        else:
            st.warning("Барлық өрістерді толтырыңыз.")
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "admin"
        st.rerun()

def users_list_page():
    st.markdown("<h1>👥 Пайдаланушылар тізімі</h1>", unsafe_allow_html=True)
    
    data = []
    for uname, info in users_db.items():
        if isinstance(info, dict):
            data.append({"Логин": uname, "Аты-жөні": info.get("name", ""), "Рөлі": info.get("role", "")})
    
    st.table(pd.DataFrame(data))
    
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
    
    with st.form("add_question_form"):
        subject = st.text_input("Пән атауы (мысалы: Математика, Қазақстан тарихы)")
        question_text = st.text_area("Сұрақ мәтіні")
        
        col1, col2 = st.columns(2)
        with col1:
            opt1 = st.text_input("Вариант A")
            opt2 = st.text_input("Вариант B")
        with col2:
            opt3 = st.text_input("Вариант C")
            opt4 = st.text_input("Вариант D")
        
        options = [opt1, opt2, opt3, opt4]
        correct = st.selectbox("Дұрыс жауапты таңдаңыз", options)
        
        submitted = st.form_submit_button("💾 Сақтау")
        if submitted:
            if subject and question_text and all(options):
                valid_qs = [q for q in questions_db if isinstance(q, dict) and "id" in q]
                new_id = max([q["id"] for q in valid_qs], default=0) + 1
                new_q = {
                    "id": new_id,
                    "subject": subject,
                    "question": question_text,
                    "options": options,
                    "answer": correct
                }
                questions_db.append(new_q)
                save_json(QUESTIONS_FILE, questions_db)
                st.success("Сұрақ сәтті қосылды!")
            else:
                st.warning("Барлық өрістерді толтырыңыз!")
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "prime_minister"
        st.rerun()

def question_list_page():
    st.markdown("<h1>📚 Сұрақтар тізімі</h1>", unsafe_allow_html=True)
    
    valid_qs = [q for q in questions_db if isinstance(q, dict)]
    if not valid_qs:
        st.info("Қорда сұрақтар жоқ.")
    else:
        for idx, q in enumerate(valid_qs, start=1):
            with st.expander(f"{idx}. [{q.get('subject', 'Пәнсіз')}] {q.get('question', '')}"):
                for opt in q.get("options", []):
                    if opt == q.get("answer"):
                        st.markdown(f"- **{opt} (Дұрыс жауап)**")
                    else:
                        st.markdown(f"- {opt}")
                        
    st.write("")
    if st.button("⬅️ Басты бетке қайту"):
        st.session_state.page = "home"
        st.rerun()

def combination_page():
    st.markdown("<h1>📝 Тест түрін таңдау</h1>", unsafe_allow_html=True)
    
    # ТҮЗЕТІЛГЕН ҚАДAM (TypeError қатесі жойылды)
    subjects = list(set(q.get("subject") for q in questions_db if isinstance(q, dict) and "subject" in q))
    
    if not subjects:
        st.warning("Базада сұрақтар жоқ!")
        if st.button("⬅️ Басты бет"):
            st.session_state.page = "home"
            st.rerun()
        return

    selected_subject = st.selectbox("Пәнді таңдаңыз:", subjects)
    st.write("")
    if st.button("🚀 Тестті бастау"):
        filtered_qs = [q for q in questions_db if isinstance(q, dict) and q.get("subject") == selected_subject]
        st.session_state.current_test = filtered_qs
        st.session_state.test_answers = {}
        st.session_state.page = "test"
        st.rerun()
        
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

    st.markdown(f"<h1>✍️ Тест: <span style='color: #818cf8;'>{questions[0].get('subject')}</span></h1>", unsafe_allow_html=True)
    
    for i, q in enumerate(questions):
        st.markdown(f"### {i+1}-сұрақ: {q.get('question')}")
        ans = st.radio(
            "Жауапты таңдаңыз:", 
            q.get("options", []), 
            key=f"q_{q.get('id')}", 
            index=None
        )
        if ans:
            st.session_state.test_answers[q.get("id")] = ans
        st.markdown("---")
        
    if st.button("🎯 Тестті аяқтау"):
        score = 0
        total = len(questions)
        for q in questions:
            user_ans = st.session_state.test_answers.get(q.get("id"))
            if user_ans == q.get("answer"):
                score += 1
                
        percent = round((score / total) * 100, 1) if total > 0 else 0
        
        result_record = {
            "username": st.session_state.username,
            "subject": questions[0].get('subject'),
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
        col1, col2, col3 = st.columns(3)
        col1.metric("Пән", res.get("subject"))
        col2.metric("Дұрыс жауаптар", f"{res.get('score')} / {res.get('total')}")
        col3.metric("Нәтиже", f"{res.get('percent')}%")
        
        if res.get("percent", 0) >= 70:
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
        user_results = [r for r in results_db if isinstance(r, dict) and r.get("username") == st.session_state.username]
        
    if not user_results:
        st.info("Тарих бос.")
    else:
        df = pd.DataFrame(user_results)
        st.dataframe(df, use_container_width=True)
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

def progress_page():
    st.markdown("<h1>📈 Прогресс және Статистика</h1>", unsafe_allow_html=True)
    
    user_results = [r for r in results_db if isinstance(r, dict) and r.get("username") == st.session_state.username]
    
    if not user_results:
        st.info("Аналитика жасау үшін әлі тест тапсырмадыңыз.")
    else:
        df = pd.DataFrame(user_results)
        st.subheader("Динамика (Пайыз бойынша)")
        st.line_chart(df.set_index("date")["percent"])
        
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
