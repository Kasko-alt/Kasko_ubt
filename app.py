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

# Деректерді жүктеу функциялары (мысал ретінде)
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

# Мысалға алынған пәндер мен комбинациялар
combinations = {
    "Математика + Физика": ["Математика", "Физика", "Қазақстан тарихы", "Математикалық сауаттылық", "Оқу сауаттылығы"],
    "Биология + Химия": ["Биология", "Химия", "Қазақстан тарихы", "Математикалық сауаттылық", "Оқу сауаттылығы"]
}

# --- АВТОРИЗАЦИЯ БӨЛІМІ ---
if not st.session_state.user:
    st.subheader("🔑 Жүйеге кіру")
    username = st.text_input("Логин")
    password = st.text_input("Құпия сөз", type="password")
    
    if st.button("Кіру"):
        # Қарапайым тексеру (немесе файлдан оқу)
        if username == "admin" and password == hash_password("admin123"): # Мысал үшін
            st.session_state.user = {"username": "admin", "role": "admin"}
            st.rerun()
        else:
            # Дерекқордан іздеу логикасы осында болады
            st.error("Логин немесе құпия сөз қате!")
    st.stop()

# --- ТЕСТІЛЕУ ЛОГИКАСЫ МЕН РАНДОМДАУ ---
user = st.session_state.user

if user["role"] == "user":
    st.title("🎓 ҰБТ Дайындық орталығы")
    
    # Нәтиже көрсетіліп тұрған болса
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
            st.write(f"**{sub}**: {sub_correct} / {len(qs)} дұрыс жауап")
            
        st.info(100 * total_correct // max(1, total_questions)) # Пайыздық көрсеткіш немесе балл
        
        if st.button("🔄 Жаңа тест бастау"):
            st.session_state.test_started = False
            st.session_state.show_results = False
            st.session_state.test_answers = {}
            st.session_state.shuffled_questions = {}
            st.rerun()
            
    elif not st.session_state.test_started:
        st.subheader("Бейіндік пәндер комбинациясын таңдаңыз:")
        selected_comb = st.selectbox("Комбинация", list(combinations.keys()))
        
        if st.button("🚀 Тестті бастау (ҰБТ форматында)", type="primary"):
            st.session_state.test_started = True
            st.session_state.show_results = False
            st.session_state.active_combination = selected_comb
            st.session_state.current_subject_idx = 0
            st.session_state.current_question_idx = 0
            st.session_state.test_answers = {}
            
            # 🎲 СҰРАҚТАРДЫ ЖӘНЕ ЖАУАПТАРДЫ РАНДОМДАУ
            st.session_state.shuffled_questions = {}
            active_subjects = combinations.get(selected_comb, [])
            
            # Базадан сұрақтарды алу (мысал ретінде бос dict немесе функция)
            all_questions_db = load_json("questions.json", {}) 
            
            for sub in active_subjects:
                sub_qs = all_questions_db.get(sub, []).copy()
                
                # Егер сұрақтар жеткілікті болса араластырамыз
                if sub_qs:
                    random.shuffle(sub_qs)
                    
                    # Әр сұрақтың жауаптарын да кездейсоқ орынға ауыстыру
                    for q in sub_qs:
                        if "answers" in q and "correct" in q:
                            correct_text = q["answers"][q["correct"]]
                            random.shuffle(q["answers"])
                            q["correct"] = q["answers"].index(correct_text)
                            
                    # ҰБТ стандарты бойынша шектеу (Мысалы: профильдік 35, басқалары 20 сұрақ)
                    limit = 20 if "сауаттылық" in sub.lower() or "тарих" in sub.lower() else 35
                    st.session_state.shuffled_questions[sub] = sub_qs[:limit]
                else:
                    st.session_state.shuffled_questions[sub] = []
                    
            st.rerun()
            
    else:
        # --- ТЕСТ ӨТУ ПРОЦЕСІ ---
        active_comb = st.session_state.active_combination
        subjects = combinations.get(active_comb, [])
        
        sub_idx = st.session_state.current_subject_idx
        current_sub = subjects[sub_idx]
        
        st.write(### Пән: {current_sub} (Пән {sub_idx + 1} / {len(subjects)}))
        
        qs = st.session_state.shuffled_questions.get(current_sub, [])
        
        if not qs:
            st.warning(Бұл пән бойынша сұрақтар әзірге жоқ.")
            if st.button("Келесі пәнге өту"):
                if sub_idx < len(subjects) - 1:
                    st.session_state.current_subject_idx += 1
                else:
                    st.session_state.test_started = False
                    st.session_state.show_results = True
                st.rerun()
        else:
            q_idx = st.session_state.current_question_idx
            q_data = qs[q_idx]
            
            st.markdown(f"**Сұрақ {q_idx + 1} / {len(qs)}**")
            st.write(q_data.get("question", ""))
            
            # Жауапты сақтау немесе бұрын таңдалғанын көрсету
            answer_key = (current_sub, q_idx)
            current_answer = st.session_state.test_answers.get(answer_key, None)
            
            selected_option = st.radio(
                "Жауапты таңдаңыз:",
                q_data.get("answers", []),
                index=current_answer if current_answer is not None else 0,
                key=f"radio_{sub_idx}_{q_idx}"
            )
            
            # Жауапты жадқа сақтау
            st.session_state.test_answers[answer_key] = q_data.get("answers", []).index(selected_option)
            
            # Навигация түймелері
            col1, col2, col3 = st.columns(3)
            with col1:
                if q_idx > 0 and st.button("⬅️ Алдыңғы"):
                    st.session_state.current_question_idx -= 1
                    st.rerun()
            with col3:
                if q_idx < len(qs) - 1:
                    if st.button("Келесі ➡️"):
                        st.session_state.current_question_idx += 1
                        st.rerun()
                else:
                    # Пән соңы немесе соңғы пән
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
