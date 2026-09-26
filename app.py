import json
import os
import random
import datetime
import hashlib
import re
import streamlit as st
import streamlit.components.v1 as components

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
# ҚАУІПСІЗДІК: ПАРОЛЬДІ ХЭШТЕУ
# =========================================================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# =========================================================
# ПӘНДӘР МЕН КОМБИНАЦИЯЛАР
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
    "Математика - Физика (Инженерлік)": ["Математика", "Физика", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"],
    "Биология - Химия (Медицина)": ["Биология", "Химия", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"],
    "География - Математика (Геодезия/Экономика)": ["География", "Математика", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"],
    "Дүниежүзі тарихы - Ағылшын (Халықаралық)": ["Дүниежүзі тарихы", "Ағылшын тілі", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"],
    "Математика - Информатика (IT / Бағдарламалау)": ["Математика", "Информатика", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"],
    "Құқық - Дүниежүзі тарихы (Юриспруденция)": ["Құқық", "Дүниежүзі тарихы", "Қазақстан тарихы", "Оқу сауаттылығы", "Математикалық сауаттылық"]
}

default_questions = {
    "Биология": [
        {
            "question": "Фотосинтез процесі қай органоидта жүреді?",
            "answers": ["Митохондрия", "Хлоропласт", "Рибосома", "Лизосома"],
            "correct": 1,
        },
        {
            "question": "Адам ағзасындағы негізгі тұқықуақыт ақпаратын сақтайтын молекула:",
            "answers": ["РНҚ", "ДНҚ", "Белок", "Липид"],
            "correct": 1,
        }
    ],
    "Информатика": [
        {
            "question": "Python тілінде экранға мәтін шығару үшін қай функция қолданылады?",
            "answers": ["input()", "print()", "output()", "write()"],
            "correct": 1,
        }
    ],
    "Қазақстан тарихы": [
        {
            "question": "Қазақ хандығы қашан құрылды?",
            "answers": ["1465-1466 жж.", "1729 ж.", "1841 ж.", "1916 ж."],
            "correct": 0,
        }
    ]
}

# =========================================================
# ҚОЛДАНУШЫЛАР ЖҮЙЕСІ
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

def username_exists(username):
    return any(user.get("username") == username for user in users)

# =========================================================
# СҰРАҚТАР МЕН НӘТИЖЕЛЕР БАЗАСЫ
# =========================================================
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                for sub in all_subjects:
                    if sub not in data: 
                        data[sub] = []
                return data
        except Exception:
            return default_questions.copy()
    return default_questions.copy()

def save_questions():
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

questions = load_questions()

def load_results_history():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def save_results_history(history):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "role" not in st.session_state: st.session_state.role = None
if "username" not in st.session_state: st.session_state.username = ""
if "full_name" not in st.session_state: st.session_state.full_name = ""
if "page" not in st.session_state: st.session_state.page = "login"
if "test_started" not in st.session_state: st.session_state.test_started = False
if "active_combination" not in st.session_state: st.session_state.active_combination = None

# =========================================================
# СТИЛЬДЕР (DARK MODE & PREMIUM DESIGN)
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
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
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
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #6366F1;
        color: #6366F1;
        transform: translateY(-2px);
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
    st.session_state.test_started = False
    st.session_state.active_combination = None
    st.rerun()

# =========================================================
# LOGIN PAGE
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
                st.session_state.page = "admin" if user["role"] == "admin" else ("moderator" if user["role"] == "moderator" else "home")
                st.rerun()
            else:
                st.error("❌ Логин немесе құпия сөз қате.")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# АВТО-ПАРСЕР ЖӘНЕ СҰРАҚТАРДЫ ЖОЮ ФУНКЦИЯСЫ (МОДЕРАТОР ҮШІН)
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

def render_question_manager():
    tab1, tab2, tab3 = st.tabs(["⚡ Жылдам массалық жүктеу (40+)", "✍️ Жеке сұрақ қосу", "🗑️ Сұрақтарды жою (Удалить)"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_subject_bulk = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects, key="bulk_sub")
        st.info("💡 **Үлгі формат (Барлық сұрақтарды бірден көшіріп қойыңыз):**\n1. Фотосинтез қайда жүреді?\nA) Митохондрия\nB) Хлоропласт\nC) Рибосома\nD) Ядро")

        raw_text_input = st.text_area(
            "✍️ Барлық сұрақтарды осында көшіріп қойыңыз (Ctrl + V):", 
            height=250,
            placeholder="1. Сұрақ...\nA) ...\nB) ...\nC) ...\nD) ..."
        )

        if st.button("🚀 Барлық сұрақтарды базаға қосу", use_container_width=True, type="primary"):
            if raw_text_input.strip():
                parsed = parse_bulk_questions(raw_text_input)
                if parsed:
                    if selected_subject_bulk not in questions:
                        questions[selected_subject_bulk] = []
                    questions[selected_subject_bulk].extend(parsed)
                    save_questions()
                    st.success(f"✨ Сәтті! Барлығы **{len(parsed)}** сұрақ базаға қосылды!")
                else:
                    st.error("⚠️ Формат танылмады. Үлгіні сақтағаныңызға көз жеткізіңіз.")
            else:
                st.warning("⚠️ Өріс бос болмауы тиіс!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_subject = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects, key="single_sub")
        question_text = st.text_area("✍️ Сұрақты толық жазыңыз:", placeholder="Мысалы: Жасушаның энергетикалық станциясы...")

        col_a, col_b = st.columns(2)
        with col_a:
            ans1 = st.text_input("А нұсқасы:")
            ans3 = st.text_input("В нұсқасы:")
        with col_b:
            ans2 = st.text_input("Б нұсқасы:")
            ans4 = st.text_input("Г нұсқасы:")

        correct_option = st.selectbox("✅ Дұрыс жауап:", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"])
        correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(correct_option)

        if st.button("💾 Сұрақты сақтау", use_container_width=True, type="primary"):
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
                st.error("⚠️ Барлық өрістерді толтырыңыз!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🗑️ Сұрақты өшіру (Удалить)")
        del_subject = st.selectbox("📚 Пәнді таңдаңыз:", all_subjects, key="del_sub")
        sub_list = questions.get(del_subject, [])

        if not sub_list:
            st.info(f"⚠️ {del_subject} пәнінде әзірге сұрақтар жоқ.")
        else:
            q_options = {f"{i+1}. {q['question'][:50]}...": i for i, q in enumerate(sub_list)}
            selected_q_label = st.selectbox("Өшіретін сұрақты таңдаңыз:", list(q_options.keys()))

            if st.button("🗑️ Таңдалған сұрақты жою", type="primary"):
                idx_to_delete = q_options[selected_q_label]
                removed = sub_list.pop(idx_to_delete)
                questions[del_subject] = sub_list
                save_questions()
                st.success(f"🗑️ Сәтті жойылды: \"{removed['question'][:40]}...\"")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def moderator_page():
    if st.button("🚪 Шығу"): logout()
    st.markdown('<div class="kasym-title" style="font-size: 32px;">🛠️ Модератор панелі</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Сұрақтар базасын толық басқару және жою</div>', unsafe_allow_html=True)
    render_question_manager()

def admin_page():
    if st.button("🚪 Шығу"): logout()
    st.markdown('<div class="kasym-title" style="font-size: 32px;">👑 Администратор панелі</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">Қолданушыларды басқару және жүйе мониторингі</div>', unsafe_allow_html=True)

    admin_tabs = st.tabs(["👥 Қолданушыларды басқару", "📊 Статистика"])

    with admin_tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ➕ Жаңа қолданушы тіркеу")
        new_u = st.text_input("Логин:")
        new_p = st.text_input("Құпия сөз:", type="password")
        new_n = st.text_input("Толық аты-жөні:")
        new_r = st.selectbox("Ролі:", ["user", "moderator", "admin"])
        
        if st.button("Қолданушыны сақтау", type="primary"):
            if new_u and new_p:
                if username_exists(new_u):
                    st.error("❌ Бұл логин бар!")
                else:
                    users.append({
                        "username": new_u,
                        "password": hash_password(new_p),
                        "name": new_n,
                        "role": new_r,
                        "combination": None
                    })
                    save_users(users)
                    st.success("✨ Қолданушы сәтті тіркелді!")
            else:
                st.error("⚠️ Логин мен құпия сөзді толтырыңыз!")
        
        st.markdown("---")
        st.markdown("### 📋 Қолданушылар тізімі")
        for u in users:
            st.write(f"- **{u.get('name', 'Аты жоқ')}** (@{u.get('username')}) — Ролі: `{u.get('role')}`")
        st.markdown('</div>', unsafe_allow_html=True)

    with admin_tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Жүйе статистикасы")
        total_q = sum(len(q_list) for q_list in questions.values())
        st.metric("Барлық сұрақтар саны", total_q)
        st.metric("Тіркелген қолданушылар саны", len(users))
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ОҚУШЫНЫҢ БАСТЫ БЕТІ ЖӘНЕ КАЛЬКУЛЯТОР БАР ТЕСТ ПАНЕЛІ
# =========================================================
def home_page():
    if st.button("🚪 Шығу"): logout()
    
    with st.sidebar:
        st.markdown(f"### 👋 Сәлем, {st.session_state.full_name}!")
        st.markdown("---")
        st.markdown("### 🧮 Калькулятор")
        calc_html = """
        <div style="background: #1E293B; padding: 10px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <input type="text" id="calc-display" readonly style="
                width: 100%; height: 35px; background: #0F172A; color: #10B981; 
                font-size: 16px; text-align: right; padding: 4px 8px; border: 1px solid rgba(255, 255, 255, 0.1); 
                border-radius: 8px; margin-bottom: 8px; box-sizing: border-box; font-weight: bold;
            " value="0">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px;">
                <button onclick="calcClear()" style="background:#EF4444; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">C</button>
                <button onclick="calcInput('(')" style="background:#4B5563; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">(</button>
                <button onclick="calcInput(')')" style="background:#4B5563; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">)</button>
                <button onclick="calcInput('/')" style="background:#6366F1; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">÷</button>
                <button onclick="calcInput('7')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">7</button>
                <button onclick="calcInput('8')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">8</button>
                <button onclick="calcInput('9')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">9</button>
                <button onclick="calcInput('*')" style="background:#6366F1; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">×</button>
                <button onclick="calcInput('4')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">4</button>
                <button onclick="calcInput('5')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">5</button>
                <button onclick="calcInput('6')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">6</button>
                <button onclick="calcInput('-')" style="background:#6366F1; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">-</button>
                <button onclick="calcInput('1')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">1</button>
                <button onclick="calcInput('2')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">2</button>
                <button onclick="calcInput('3')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">3</button>
                <button onclick="calcInput('+')" style="background:#6366F1; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">+</button>
                <button onclick="calcInput('0')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">0</button>
                <button onclick="calcInput('.')" style="background:#334155; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">.</button>
                <button onclick="calcBackspace()" style="background:#F59E0B; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer;">⌫</button>
                <button onclick="calcCalculate()" style="background:#10B981; color:white; padding:6px; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">=</button>
            </div>
        </div>
        <script>
        let display = document.getElementById('calc-display');
        function calcInput(val) {
            if (display.value === '0' || display.value === 'Қате') display.value = val;
            else display.value += val;
        }
        function calcClear() { display.value = '0'; }
        function calcBackspace() {
            display.value = display.value.slice(0, -1);
            if (display.value === '') display.value = '0';
        }
        function calcCalculate() {
            try { display.value = eval(display.value); } 
            catch (e) { display.value = 'Қате'; }
        }
        </script>
        """
        components.html(calc_html, height=290)

    st.markdown('<div class="kasym-title" style="font-size: 32px;">🏠 Оқушы панелі</div>', unsafe_allow_html=True)
    st.markdown('<div class="kasym-subtitle">ҰБТ-ға дайындық және тест тапсыру</div>', unsafe_allow_html=True)

    current_user_obj = next((u for u in users if u["username"] == st.session_state.username), None)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_comb = st.selectbox("🎯 ҰБТ Бейіндік пәндер комбинациясын таңдаңыз:", list(combinations.keys()))
    
    if st.button("💾 Комбинацияны сақтау", type="primary"):
        if current_user_obj:
            current_user_obj["combination"] = selected_comb
            save_users(users)
            st.success("✨ Комбинация сақталды!")

    st.markdown("---")
    st.markdown("### 🚀 Тестті бастау")
    if st.button("🚀 Тестті бастау (Пәндер бөлігімен)", type="primary", use_container_width=True):
        st.session_state.test_started = True
        st.session_state.active_combination = selected_comb
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("test_started", False):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 📋 ҰБТ Тест Парағы (Пәндер бойынша)")
        
        active_subjects = combinations.get(st.session_state.active_combination, all_subjects[:5])
        subject_tabs = st.tabs(active_subjects)
        
        user_answers = {}
        
        for tab_idx, sub in enumerate(active_subjects):
            with subject_tabs[tab_idx]:
                st.markdown(f"### 📚 {sub} пәні")
                sub_qs = questions.get(sub, [])
                
                if not sub_qs:
                    st.info(f"⚠️ {sub} пәні бойынша әзірге сұрақтар жоқ. Модератор панелі арқылы сұрақтарды қосыңыз.")
                else:
                    for q_idx, q in enumerate(sub_qs):
                        global_key = f"{sub}_{q_idx}"
                        st.markdown(f"**{q_idx + 1}. {q['question']}**")
                        user_answers[global_key] = st.radio(
                            f"Жауапты таңдаңыз ({sub} - {q_idx+1}):", 
                            q["answers"], 
                            key=f"radio_{global_key}", 
                            index=None
                        )
                        st.markdown("---")

        if st.button("✅ Тестті аяқтау және нәтижені көру", type="primary", use_container_width=True):
            correct_count = 0
            total_q_count = 0
            
            for sub in active_subjects:
                sub_qs = questions.get(sub, [])
                for q_idx, q in enumerate(sub_qs):
                    global_key = f"{sub}_{q_idx}"
                    total_q_count += 1
                    selected = user_answers.get(global_key)
                    if selected and q["answers"][q["correct"]] == selected:
                        correct_count += 1
            
            percent = int((correct_count / total_q_count * 100) if total_q_count > 0 else 0)
            
            history = load_results_history()
            history.append({
                "username": st.session_state.username,
                "subject": st.session_state.active_combination,
                "correct": correct_count,
                "total": total_q_count,
                "percent": percent,
                "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            })
            save_results_history(history)

            st.success(f"🎉 Нәтижеңіз: **{correct_count} / {total_q_count}** ({percent}%)")
            if st.button("🔄 Жаңа тест бастау"):
                st.session_state.test_started = False
                st.rerun()
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
        elif p == "moderator": moderator_page()
        else: home_page()

if __name__ == "__main__":
    main()
