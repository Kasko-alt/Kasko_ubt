import streamlit as st
import random
import hashlib
import json
import os

# Бетті конфигурациялау
st.set_page_config(page_title="ҰБТ Тестілеу жүйесі", page_icon="📚", layout="wide")

# Құпия сөзді хэштеу функциясы
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# JSON файлдарымен жұмыс функциялары
def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Бастапқы файлдарды құру (егер жоқ болса)
if not os.path.exists("users.json"):
    # Әдепкі әкімші (админ) құру: admin / admin123
    save_json("users.json", {
        "admin": {"password": hash_password("admin123"), "role": "admin"}
    })

if not os.path.exists("questions.json"):
    save_json("questions.json", {})

if not os.path.exists("results_history.json"):
    save_json("results_history.json", [])

# Session State бастапқы мәндері
if "user" not in st.session_state:
    st.session_state.user = None
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "test_answers" not in st.session_state:
    st.session_state.test_answers = {}
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = {}

# ҰБТ комбинациялары мен міндетті пәндер
all_subjects = ["Қазақстан тарихы", "Математикалық сауаттылық", "Оқу сауаттылығы"]
combinations = {
    "Математика + Физика": ["Математика", "Физика"] + all_subjects,
    "Математика + Информатика": ["Математика", "Информатика"] + all_subjects,
    "Биология + Химия": ["Биология", "Химия"] + all_subjects,
    "География + Математика": ["География", "Математика"] + all_subjects,
    "Ағылшын тілі + Дүние жүзі тарихы": ["Ағылшын тілі", "Дүние жүзі тарихы"] + all_subjects
}

# --- АВТОРИЗАЦИЯ ЖӘНЕ КІРУ БӨЛІМІ ---
if not st.session_state.user:
    st.subheader("🔑 ҰБТ Жүйесіне кіру")
    username = st.text_input("Логин")
    password = st.text_input("Құпия сөз", type="password")
    
    if st.button("Кіру"):
        users = load_json("users.json", {})
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state.user = {"username": username, "role": users[username]["role"]}
            st.success("Сәтті кірдіңіз!")
            st.rerun()
        else:
            st.error("Логин немесе құпия сөз қате!")
    st.stop()

user = st.session_state.user

# --- САЙДБАР (Қосымша мүмкіндіктер мен калькулятор) ---
with st.sidebar:
    st.write(f"👤 Қолданушы: **{user['username']}** ({user['role']})")
    if st.button("🚪 Шығу"):
        st.session_state.user = None
        st.session_state.test_started = False
        st.session_state.show_results = False
        st.rerun()
        
    st.divider()
    st.subheader("🧮 ҰБТ Калькуляторы")
    calc_input = st.text_input("Өрнек енгізіңіз (мысалы: 25*4+10):")
    if calc_input:
        try:
            # Қауіпсіз есептеу
            allowed_chars = set("0123456789+-*/(). ")
            if all(c in allowed_chars for c in calc_input):
                result = eval(calc_input)
                st.success(f"Нәтиже: {result}")
            else:
                st.error("Қате таңбалар бар!")
        except Exception:
            st.error("Қате өрнек!")

# --- ӘКДІМШІ (ADMIN) ПАНЕЛІ ---
if user["role"] == "admin":
    st.title("🛠️ Админ панелі")
    tab1, tab2 = st.tabs(["📝 Сұрақ қосу / басқару", "👥 Қолданушылар қосу"])
    
    with tab1:
        st.subheader("Жаңа сұрақ қосу")
        questions_db = load_json("questions.json", {})
        
        # Барлық қолжетімді пәндер тізімі
        unique_subjects = list(set([sub for comb in combinations.values() for sub in comb]))
        q_subject = st.selectbox("Пәнді таңдаңыз", unique_subjects)
        
        q_text = st.text_area("Сұрақ мәтіні")
        
        col_a, col_b = st.columns(2)
        with col_a:
            ans1 = st.text_input("1-ші жауап")
            ans2 = st.text_input("2-ші жауап")
        with col_b:
            ans3 = st.text_input("3-ші жауап")
            ans4 = st.text_input("4-ші жауап")
            
        correct_idx = st.selectbox("Дұрыс жауаптың реті", [1, 2, 3, 4]) - 1
        
        if st.button("Сұрақты сақтау"):
            if q_text and ans1 and ans2 and ans3 and ans4:
                if q_subject not in questions_db:
                    questions_db[q_subject] = []
                
                questions_db[q_subject].append({
                    "question": q_text,
                    "answers": [ans1, ans2, ans3, ans4],
                    "correct": correct_idx
                })
                save_json("questions.json", questions_db)
                st.success("Сұрақ базаға сәтті қосылды!")
            else:
                st.error("Барлық өрістерді толтырыңыз!")
                
    with tab2:
        st.subheader("Жаңа қолданушы немесе модератор қосу")
        new_username = st.text_input("Жаңа логин")
        new_password = st.text_input("Жаңа құпия сөз", type="password")
        new_role = st.selectbox("Рөлі", ["user", "moderator", "admin"])
        
        if st.button("Қолданушыны тіркеу"):
            users = load_json("users.json", {})
            if new_username in users:
                st.error("Мұндай логин бар!")
            elif new_username and new_password:
                users[new_username] = {
                    "password": hash_password(new_password),
                    "role": new_role
                }
                save_json("users.json", users)
                st.success(f"Қолданушы {new_username} ({new_role}) тіркелді!")
            else:
                st.error("Барлық өрістерді толтырыңыз!")

# --- ОҚУШЫ (USER) ИНТЕРФЕЙСІ ---
elif user["role"] in ["user", "moderator"]:
    st.title("🎓 ҰБТ Дайындық жүйесі")
    
    # Нәтиже көрсету экраны
    if st.session_state.show_results:
        st.success("🎉 Тест аяқталды!")
        st.subheader("📊 Сіздің нәтижелеріңіз:")
        
        total_correct = 0
        total_questions = 0
        
        for sub, qs in st.session_state.shuffled_questions.items():
            sub_correct = 0
            for idx, q in enumerate(qs):
                user_ans = st.session_state.test_answers.get((sub, idx))
                if user_ans == q["correct"]:
                    sub_correct += 1
            total_correct += sub_correct
            total_questions += len(qs)
            st.write(f"👉 **{sub}**: {sub_correct} / {len(qs)} дұрыс жауап")
            
        st.info(f"Жалпы жиналған дұрыс жауаптар: **{total_correct} / {total_questions}**")
        
        if st.button("🔄 Жаңа тест бастау"):
            st.session_state.test_started = False
            st.session_state.show_results = False
            st.session_state.test_answers = {}
            st.session_state.shuffled_questions = {}
            st.rerun()
            
    # Тест басталмаған болса комбинация таңдату
    elif not st.session_state.test_started:
        st.subheader("Бейіндік пәндер комбинациясын таңдаңыз:")
        selected_comb = st.selectbox("Комбинациялар", list(combinations.keys()))
        
        if st.button("🚀 Тестті бастау (ҰБТ форматында)", type="primary"):
            st.session_state.test_started = True
            st.session_state.show_results = False
            st.session_state.active_combination = selected_comb
            st.session_state.current_subject_idx = 0
            st.session_state.current_question_idx = 0
            st.session_state.test_answers = {}
            
            # 🎲 СҰРАҚТАРДЫ РАНДОМДАУ ЖӘНЕ ҰБТ СТАНДАРТЫМЕН ЛИМИТТЕУ
            st.session_state.shuffled_questions = {}
            active_subjects = combinations.get(selected_comb, [])
            all_questions_db = load_json("questions.json", {})
            
            for sub in active_subjects:
                sub_qs = all_questions_db.get(sub, []).copy()
                
                if sub_qs:
                    random.shuffle(sub_qs) # Сұрақтарды кездейсоқ араластыру
                    
                    # Әр сұрақтың ішіндегі жауаптарды да араластыру
                    for q in sub_qs:
                        if "answers" in q and "correct" in q:
                            correct_text = q["answers"][q["correct"]]
                            random.shuffle(q["answers"])
                            q["correct"] = q["answers"].index(correct_text)
                    
                    # 🎯 ҰБТ СТАНДАРТЫ БОЙЫНША СҰРАҚ САНЫН ШЕКТЕУ:
                    sub_lower = sub.lower()
                    if "сауаттылық" in sub_lower:
                        limit = 10
                    elif "тарих" in sub_lower:
                        limit = 20
                    else:
                        limit = 40  # Бейіндік пәндер үшін 40 сұрақ
                        
                    st.session_state.shuffled_questions[sub] = sub_qs[:limit]
                else:
                    st.session_state.shuffled_questions[sub] = []
                    
            st.rerun()
            
    # Тестті өту барысы
    else:
        active_comb = st.session_state.active_combination
        subjects = combinations.get(active_comb, [])
        
        sub_idx = st.session_state.current_subject_idx
        current_sub = subjects[sub_idx]
        
        st.markdown(f"### 📖 Пән: {current_sub} (Пән {sub_idx + 1} / {len(subjects)})")
        
        qs = st.session_state.shuffled_questions.get(current_sub, [])
        
        if not qs:
            st.warning(f"'{current_sub}' пәні бойынша базада сұрақтар жоқ немесе жеткіліксіз.")
            col_skip1, col_skip2 = st.columns(2)
            with col_skip1:
                if sub_idx < len(subjects) - 1 and st.button("Келесі пәнге өту ➡️"):
                    st.session_state.current_subject_idx += 1
                    st.session_state.current_question_idx = 0
                    st.rerun()
            with col_skip2:
                if sub_idx == len(subjects) - 1 and st.button("🏁 Тестті аяқтау"):
                    st.session_state.test_started = False
                    st.session_state.show_results = True
                    st.rerun()
        else:
            q_idx = st.session_state.current_question_idx
            q_data = qs[q_idx]
            
            st.markdown(f"**Сұрақ {q_idx + 1} / {len(qs)}**")
            st.write(q_data.get("question", ""))
            
            answer_key = (current_sub, q_idx)
            current_answer = st.session_state.test_answers.get(answer_key, None)
            
            selected_option = st.radio(
                "Жауапты таңдаңыз:",
                q_data.get("answers", []),
                index=current_answer if current_answer is not None else 0,
                key=f"radio_{sub_idx}_{q_idx}"
            )
            
            # Таңдалған жауапты жадқа жазу
            st.session_state.test_answers[answer_key] = q_data.get("answers", []).index(selected_option)
            
            # Навигация батырмалары
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if q_idx > 0 and st.button("⬅️ Алдыңғы"):
                    st.session_state.current_question_idx -= 1
                    st.rer0un = True if "st" in globals() else None # Дұрыстау
                    st.rerun()
            with col3:
                if q_idx < len(qs) - 1:
                    if st.button("Келесі ➡️"):
                        st.session_state.current_question_idx += 1
                        st.rerun()
                else:
                    # Пән соңына келгенде келесі пәнге немесе тестті аяқтауға өту
                    if sub_idx < len(subjects) - 1:
                        if st.button("➡️ Келесі пәнге өту"):
                            st.session_state.current_subject_idx += 1
                            st.session_state.current_question_idx = 0
                            st.rerun()
                    else:
                        if st.button("🏁 Тестті аяқтау", type="primary"):
                            st.session_state.test_started = False
                            st.session_state.show_results = True
                            st.rerun()
