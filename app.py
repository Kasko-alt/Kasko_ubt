import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# =========================================================
# SETTINGS & DATA INITS
# =========================================================
st.set_page_config(
    page_title="Білім беру жүйесі",
    page_icon="🎓",
    layout="wide"
)

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

# Session state инициализациясы
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
# HELPER FUNCTIONS & NAVBAR
# =========================================================
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.page = "login"
    st.session_state.current_test = None
    st.rerun()

def top_logout_button():
    col1, col2 = st.columns([8, 2])
    with col1:
        st.write(f"👤 Пайдаланушы: **{st.session_state.username}** ({users_db.get(st.session_state.username, {}).get('name', '')})")
    with col2:
        if st.button("Шығу", key="top_logout"):
            logout()
    st.markdown("---")

# =========================================================
# PAGES
# =========================================================
def login_page():
    st.title("🔐 Жүйеге кіру")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username_input = st.text_input("Пайдаланушы аты (Username)")
        password_input = st.text_input("Құпия сөз", type="password")
        
        if st.button("Кіру", use_container_width=True):
            if username_input in users_db and users_db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = users_db[username_input]["role"]
                st.session_state.page = "home"
                st.success("Cәтті кірдіңіз!")
                st.rerun()
            else:
                st.error("Логин немесе құпия сөз қате!")

def home_page():
    st.title("🏠 Басты бет")
    role = st.session_state.role
    
    st.write(f"Қош келдіңіз, **{users_db[st.session_state.username]['name']}**!")
    st.info(f"Сіздің жүйедегі рөліңіз: **{role.upper()}**")
    
    st.markdown("### Қолжетімді бөлімдер:")
    
    # Рөлге байланысты меню
    if role == "president":
        if st.button("👑 Президент панелі"):
            st.session_state.page = "admin"
            st.rerun()
            
    if role == "prime_minister":
        if st.button("🏛 Премьер-Министр панелі"):
            st.session_state.page = "prime_minister"
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Тест тапсыру", use_container_width=True):
            st.session_state.page = "combination"
            st.rerun()
        if st.button("📚 Сұрақтар тізімі", use_container_width=True):
            st.session_state.page = "question_list"
            st.rerun()
            
    with col2:
        if st.button("📊 Нәтижелер тарихы", use_container_width=True):
            st.session_state.page = "results_history"
            st.rerun()
        if st.button("📈 Прогресс және Статистика", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()

# --- Admin / President Pages ---
def admin_page():
    st.title("👑 Президент Басқару Панелі")
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
    st.title("➕ Жаңа пайдаланушы тіркеу")
    
    new_username = st.text_input("Логин")
    new_name = st.text_input("Аты-жөні")
    new_password = st.text_input("Құпия сөз", type="password")
    new_role = st.selectbox("Рөлі", ["student", "prime_minister", "president"])
    
    if st.button("Тіркеу"):
        if new_username in users_db:
            st.error("Бұндай логин тіркеліп қойған!")
        elif new_username and new_password:
            users_db[new_username] = {
                "password": new_password,
                "role": new_role,
                "name": new_name or new_username
            }
            save_json(USERS_FILE, users_db)
            st.success("Пайдаланушы сәтті қосылды!")
        else:
            st.warning("Барлық өрісті толтырыңыз.")
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "admin"
        st.rerun()

def users_list_page():
    st.title("👥 Пайдаланушылар тізімі")
    
    data = []
    for uname, info in users_db.items():
        data.append({"Логин": uname, "Аты-жөні": info.get("name", ""), "Рөлі": info.get("role", "")})
    
    st.table(pd.DataFrame(data))
    
    if st.button("⬅️ Артқа"):
        st.session_state.page = "admin"
        st.rerun()

# --- Prime Minister Pages ---
def prime_minister_page():
    st.title("🏛 Премьер-Министр Панелі")
    
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
    st.title("➕ Жаңа тест сұрағын қосу")
    
    subject = st.text_input("Пән атауы (мысалы: Математика, Физика)")
    question_text = st.text_area("Сұрақ матні")
    
    opt1 = st.text_input("Вариант A")
    opt2 = st.text_input("Вариант B")
    opt3 = st.text_input("Вариант C")
    opt4 = st.text_input("Вариант D")
    
    correct = st.selectbox("Дұрыс жауапты таңдаңыз", [opt1, opt2, opt3, opt4])
    
    if st.button("Сақтау"):
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
            
    if st.button("⬅️ Артқа"):
        st.session_state.page = "prime_minister"
        st.rerun()

# --- General Navigation Pages ---
def question_list_page():
    st.title("📚 Сұрақтар тізімі")
    
    if not questions_db:
        st.info("Қорда сұрақтар жоқ.")
    else:
        for idx, q in enumerate(questions_db, start=1):
            with st.expander(f"{idx}. [{q['subject']}] {q['question']}"):
                for opt in q["options"]:
                    if opt == q["answer"]:
                        st.markdown(f"- **{opt} (Дұрыс жауап)**")
                    else:
                        st.markdown(f"- {opt}")
                        
    if st.button("⬅️ Басты бетке қайту"):
        st.session_state.page = "home"
        st.rerun()

def combination_page():
    st.title("📝 Тест түрін таңдау")
    
    subjects = list(set(q["subject"] for q in questions_db))
    
    if not subjects:
        st.warning("Базада сұрақтар жоқ!")
        if st.button("⬅️ Басты бет"):
            st.session_state.page = "home"
            st.rerun()
        return

    selected_subject = st.selectbox("Пәнді таңдаңыз:", subjects)
    
    if st.button("Тестті бастау"):
        filtered_qs = [q for q in questions_db if q["subject"] == selected_subject]
        st.session_state.current_test = filtered_qs
        st.session_state.test_answers = {}
        st.session_state.page = "test"
        st.rerun()
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

def test_page():
    st.title("✍️ Тест тапсыру")
    
    questions = st.session_state.current_test
    if not questions:
        st.warning("Сұрақтар табылмады.")
        st.session_state.page = "home"
        st.rerun()
        return

    st.subheader(f"Пән: {questions[0]['subject']}")
    
    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}-сұрақ:** {q['question']}")
        ans = st.radio(
            "Жауапты таңдаңыз:", 
            q["options"], 
            key=f"q_{q['id']}", 
            index=None
        )
        if ans:
            st.session_state.test_answers[q["id"]] = ans
        st.markdown("---")
        
    if st.button("Тестті аяқтау"):
        # Нәтижені есептеу
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
    st.title("🎯 Тест нәтижесі")
    res = st.session_state.last_result
    
    if res:
        st.metric("Пән", res["subject"])
        st.metric("Дұрыс жауаптар", f"{res['score']} / {res['total']}")
        st.metric("Нәтиже пайызбен", f"{res['percent']}%")
        
        if res["percent"] >= 70:
            st.balloons()
            st.success("Өте жақсы нәтиже!")
        else:
            st.warning("Үйренуді жалғастырыңыз!")
            
    if st.button("Басты бетке оралу"):
        st.session_state.page = "home"
        st.rerun()

def results_history_page():
    st.title("📊 Нәтижелер тарихы")
    
    # Тек ағымдағы пайдаланушының нәтижесін көрсету (егер Президент болмаса)
    if st.session_state.role == "president":
        user_results = results_db
    else:
        user_results = [r for r in results_db if r["username"] == st.session_state.username]
        
    if not user_results:
        st.info("Тарих бос.")
    else:
        df = pd.DataFrame(user_results)
        st.dataframe(df, use_container_width=True)
        
    if st.button("⬅️ Басты бет"):
        st.session_state.page = "home"
        st.rerun()

def progress_page():
    st.title("📈 Прогресс және Аналитика")
    
    user_results = [r for r in results_db if r["username"] == st.session_state.username]
    
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
