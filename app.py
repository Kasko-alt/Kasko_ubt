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
    page_title="KASYM EDU - Білім беру платформасы", page_icon="🎓", layout="wide"
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
# 3. ПӘНДЕР МЕН КОМБИНАЦИЯЛАР ЖӘНЕ СҰРАҚТАР ЛИМИТІ
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

subject_limits = {
    "Қазақстан тарихы": 20,
    "Оқу сауаттылығы": 10,
    "Математикалық сауаттылық": 10,
    "Математика": 40,
    "Физика": 40,
    "Химия": 40,
    "Биология": 40,
    "Информатика": 40,
    "География": 40,
    "Дүниежүзі тарихы": 40,
    "Ағылшын тілі": 40,
    "Құқық": 40,
}

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

default_questions = {
    "Қазақстан тарихы": [
        {
            "question": "«Ұлы шаньюй» деп аталған тайпа көсемі:",
            "answers": ["қаңлыларда", "үйсіндерде", "ғұндарда", "сақтарда"],
            "correct": 2,
        },
        {
            "question": "Қазақ хандығы қашан құрылды?",
            "answers": ["1465-1466 жж.", "1729 ж.", "1841 ж.", "1916 ж."],
            "correct": 0,
        },
    ],
    "Биология": [{
        "question": "Фотосинтез процесі қай органоидта жүреді?",
        "answers": ["Митохондрия", "Хлоропласт", "Рибосома", "Лизосома"],
        "correct": 1,
    }],
    "Математика": [{
        "question": "Егер x + 5 = 12 болса, x неге тең?",
        "answers": ["5", "7", "12", "17"],
        "correct": 1,
    }],
    "Физика": [{
        "question": "Жылдамдықтың өлшем бірлігі:",
        "answers": ["м/с", "кг", "Н", "Вт"],
        "correct": 0,
    }],
    "Оқу сауаттылығы": [{
        "question":
            "Мәтіннің негізгі ойын анықтаңыз: «Еңбек — ерлікке жеткізер»",
            "answers": [
                "Балмұздақ жеу",
                "Еңбектің маңызы",
                "Спортпен шұғылдану",
                "Саяхат",
            ],
            "correct": 1,
    }],
    "Математикалық сауаттылық": [{
        "question": "20 санының 20%-ын табыңыз:",
        "answers": ["2", "4", "5", "10"],
        "correct": 1,
    }],
}


# =========================================================
# 4. ДЕРЕКТЕРДІ БАСҚАРУ
# =========================================================
def default_users():
  return [{
      "username": "kas01",
      "password": hash_password("kasko100228550357"),
      "name": "KASYM",
      "role": "admin",
      "combination": None,
  }]


def save_users(users_list):
  with open(USERS_FILE, "w", encoding="utf-8") as file:
    json.dump(users_list, file, ensure_ascii=False, indent=4)


def load_users():
  users_list = default_users()
  if os.path.exists(USERS_FILE):
    try:
      with open(USERS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, list) and len(data) > 0:
          users_list = data
    except Exception:
      pass

  admin_found = False
  for u in users_list:
    if u.get("username") == "kas01":
      u["role"] = "admin"
      admin_found = True

  if not admin_found:
    users_list.append({
        "username": "kas01",
        "password": hash_password("kasko100228550357"),
        "name": "KASYM",
        "role": "admin",
        "combination": None,
    })

  save_users(users_list)
  return users_list


users = load_users()


def find_user(username, password):
  hashed_input = hash_password(password)
  for user in users:
    stored = user.get("password")
    if user.get("username") == username and (
        stored == hashed_input or stored == password
    ):
      return user
  return None


def username_exists(username):
  return any(user.get("username") == username for user in users)


def load_questions():
  if os.path.exists(QUESTIONS_FILE):
    try:
      with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        for sub in all_subjects:
          if sub not in data:
            data[sub] = default_questions.get(sub, [])
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
# 5. SESSION STATE ИНИЦИАЛИЗАЦИЯСЫ
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
if "current_question_index" not in st.session_state:
  st.session_state.current_question_index = 0
if "test_answers" not in st.session_state:
  st.session_state.test_answers = {}
if "shuffled_test_data" not in st.session_state:
  st.session_state.shuffled_test_data = {}

# =========================================================
# 6. UI СТИЛЬДЕРІ (DESIGN)
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
        border-radius: 10px;
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
    /* Горизонталь палитра контейнерін ықшамдау */
    .palette-container {
        display: flex;
        overflow-x: auto;
        gap: 5px;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def logout():
  st.session_state.logged_in = False
  st.session_state.role = None
  st.session_state.username = ""
  st.session_state.full_name = ""
  st.session_state.test_started = False
  st.session_state.active_combination = None
  st.session_state.current_subject_index = 0
  st.session_state.current_question_index = 0
  st.session_state.test_answers = {}
  st.session_state.shuffled_test_data = {}
  st.rerun()


# =========================================================
# 7. КІРУ ЖӘНЕ ТІРКЕЛУ БЕТІ
# =========================================================
def login_page():
  st.markdown(
      '<div class="kasym-title">KASYM EDU</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="kasym-subtitle">Бүгінгі дайындық — ертеңгі грант</div>',
      unsafe_allow_html=True,
  )

  c1, c2, c3 = st.columns([1, 1.2, 1])
  with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tab_login, tab_register = st.tabs(["🔐 Жүйеге кіру", "📝 Тіркелу"])

    with tab_login:
      username = st.text_input("Логин", key="login_username")
      password = st.text_input(
          "Құпия сөз", type="password", key="login_password"
      )

      if st.button("Кіру →", use_container_width=True, type="primary"):
        user = find_user(username.strip(), password.strip())
        if user:
          st.session_state.logged_in = True
          st.session_state.username = user["username"]
          st.session_state.full_name = user.get("name", "")
          st.session_state.role = user.get("role", "user")
          st.rerun()
        else:
          st.error("❌ Логин немесе құпия сөз қате.")

    with tab_register:
      reg_name = st.text_input("Толық аты-жөніңіз:")
      reg_user = st.text_input("Жаңа логин таңдаңыз:")
      reg_pass = st.text_input(
          "Құпия сөз ойлап табыңыз:", type="password", key="reg_pass"
      )

      if st.button(
          "Тіркелуді аяқтау", use_container_width=True, type="primary"
      ):
        if reg_name and reg_user and reg_pass:
          if username_exists(reg_user):
            st.error("❌ Бұл логин бос емес, басқа логин таңдаңыз.")
          else:
            new_student = {
                "username": reg_user.strip(),
                "password": hash_password(reg_pass.strip()),
                "name": reg_name.strip(),
                "role": "user",
                "combination": None,
            }
            users.append(new_student)
            save_users(users)
            st.success("✨ Сәтті тіркелдіңіз! Енді кіре аласыз.")
        else:
          st.error("⚠️ Барлық өрістерді толтырыңыз!")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# СТАТИСТИКА ЖӘНЕ КЕСТЕ
# =========================================================
def render_statistics_tab():
  st.markdown("### 📊 Оқушылардың тест нәтижелері мен статистикасы")
  history = load_results_history()

  if not history:
    st.info("⚠️ Әзірге ешбір оқушы тест тапсырған жоқ.")
    return

  total_tests = len(history)
  avg_score = (
      sum(int(h.get("score", 0) or 0) for h in history) / total_tests
      if total_tests > 0
      else 0
  )

  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.metric(label="📈 Барлық тапсырылған тесттер", value=total_tests)
  with col_m2:
    st.metric(label="⭐ Орташа ұпай", value=f"{avg_score:.1f}")

  st.markdown("---")

  sc1, sc2 = st.columns(2)
  with sc1:
    search_query = (
        st.text_input(
            "🔍 Оқушының аты немесе логині бойынша іздеу:", key="stat_search"
        )
        .strip()
        .lower()
    )
  with sc2:
    comb_filter = st.selectbox(
        "🎯 Комбинация бойынша сүзу:",
        ["Барлығы"] + list(combinations.keys()),
        key="stat_comb_filter",
    )

  filtered_history = []
  for h in history:
    name = h.get("name") or "Аты жоқ"
    uname = h.get("username") or "белгісіз"
    comb = h.get("combination") or "Көрсетілмеген"
    score = h.get("score") if h.get("score") is not None else 0
    date = h.get("date") or "Уақыты белгісіз"

    match_search = search_query in name.lower() or search_query in uname.lower()
    match_comb = comb_filter == "Барлығы" or comb == comb_filter

    if match_search and match_comb:
      filtered_history.append({
          "Аты-жөні": name,
          "Логин": f"@{uname}",
          "Комбинация": comb,
          "Ұпай": score,
          "Күні": date,
      })

  st.caption(f"Табылған нәтижелер саны: {len(filtered_history)}")

  if not filtered_history:
    st.warning("⚠️ Іздеу шарттарына сәйкес ешбір нәтиже табылмады.")
  else:
    st.dataframe(
        filtered_history,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 8. МОДЕРАТОР ПАНЕЛІ
# =========================================================
def parse_bulk_questions(raw_text):
  questions_list = []
  blocks = re.split(r"(?=\b\d+[\.\)]\s)", raw_text)
  for block in blocks:
    if not block.strip():
      continue
    full_text = " ".join(block.strip().split("\n"))
    q_match = re.search(
        r"^\d+[\.\)]\s*(.*?)(?=[A-DА-Гa-dа-г][\.\)]|\bЖауабы:|$)", full_text
    )
    if not q_match:
      continue
    q_text = q_match.group(1).strip()
    options = re.findall(
        r"([A-DА-Гa-dа-г])[\.\)]\s*([^A-DА-Гa-dа-г\.\)]+)", full_text
    )
    answers = []
    if len(options) >= 4:
      answers = [opt[1].strip() for opt in options[:4]]
    correct_index = 0
    ans_match = re.search(r"Жауабы:\s*([A-DА-Гa-dа-г])", full_text, re.IGNORECASE)
    if ans_match:
      corr_letter = ans_match.group(1).upper()
      letter_map = {"A": 0, "А": 0, "B": 1, "Б": 1, "C": 2, "В": 2, "D": 3, "Г": 3}
      correct_index = letter_map.get(corr_letter, 0)
    if len(answers) >= 4:
      questions_list.append({
          "question": q_text,
          "answers": answers[:4],
          "correct": correct_index,
      })
  return questions_list


def moderator_page():
  col1, col2 = st.columns([6, 1])
  with col1:
    st.markdown(
        '<div class="kasym-title" style="font-size: 32px;">🛠️ Модератор'
        " панелі</div>",
        unsafe_allow_html=True,
    )
  with col2:
    if st.button("🚪 Шығу", use_container_width=True):
      logout()

  st.markdown(
      '<div class="kasym-subtitle">Сұрақтар базасы және оқушылар'
      " статистикасы</div>",
      unsafe_allow_html=True,
  )

  tab1, tab2, tab3, tab4 = st.tabs([
      "⚡ Массалық жүктеу",
      "✍️ Жеке сұрақ қосу",
      "🗑️ Сұрақтарды жою",
      "📊 Оқушылар статистикасы",
  ])

  with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sel_sub_bulk = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="mod_bulk_sub"
    )
    raw_text = st.text_area("Сұрақтарды осында көшіріп қойыңыз:", height=200)
    if st.button("🚀 Жүктеу", type="primary"):
      if raw_text.strip():
        parsed = parse_bulk_questions(raw_text)
        if parsed:
          if sel_sub_bulk not in questions:
            questions[sel_sub_bulk] = []
          questions[sel_sub_bulk].extend(parsed)
          save_questions()
          st.success(f"✨ Сәтті! {len(parsed)} сұрақ қосылды.")
        else:
          st.error("⚠️ Формат қате немесе сұрақтар танылмады.")
      else:
        st.warning("Өріс бос.")
    st.markdown("</div>", unsafe_allow_html=True)

  with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sel_sub_single = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="mod_single_sub"
    )
    q_text = st.text_area("Сұрақ мәтіні:")
    c1, c2 = st.columns(2)
    with c1:
      a1 = st.text_input("А нұсқасы:")
      a3 = st.text_input("В нұсқасы:")
    with c2:
      a2 = st.text_input("Б нұсқасы:")
      a4 = st.text_input("Г нұсқасы:")
    corr = st.selectbox(
        "Дұрыс жауап:", ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"]
    )
    corr_idx = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(corr)

    if st.button("💾 Сақтау", type="primary"):
      if q_text and a1 and a2 and a3 and a4:
        if sel_sub_single not in questions:
          questions[sel_sub_single] = []
        questions[sel_sub_single].append({
            "question": q_text,
            "answers": [a1, a2, a3, a4],
            "correct": corr_idx,
        })
        save_questions()
        st.success("✨ Сұрақ сақталды!")
      else:
        st.error("Барлық өрістерді толтырыңыз!")
    st.markdown("</div>", unsafe_allow_html=True)

  with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    del_sub = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="mod_del_sub"
    )
    sub_list = questions.get(del_sub, [])
    if not sub_list:
      st.info("Бұл пөнде сұрақтар жоқ.")
    else:
      q_map = {f"{i+1}. {q['question'][:40]}...": i for i, q in enumerate(sub_list)}
      chosen_q = st.selectbox("Жою үшін сұрақты таңдаңыз:", list(q_map.keys()))
      if st.button("🗑️ Жою", type="primary"):
        sub_list.pop(q_map[chosen_q])
        questions[del_sub] = sub_list
        save_questions()
        st.success("Жойылды!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

  with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_statistics_tab()
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 9. ӘКІМШІ (ADMIN) ПАНЕЛІ
# =========================================================
def admin_page():
  global users
  col1, col2 = st.columns([6, 1])
  with col1:
    st.markdown(
        '<div class="kasym-title" style="font-size: 32px;">👑 Администратор'
        " панелі</div>",
        unsafe_allow_html=True,
    )
  with col2:
    if st.button("🚪 Шығу", use_container_width=True):
      logout()

  st.markdown(
      '<div class="kasym-subtitle">Қолданушыларды басқару және іздеу жүйесі бар'
      " статистика</div>",
      unsafe_allow_html=True,
  )

  admin_tabs = st.tabs([
      "👥 Қолданушылар тізімі & Жою",
      "➕ Жаңа қолданушы қосу",
      "📊 Оқушылар статистикасы",
  ])

  with admin_tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        "### 📋 Тіркелген қолданушылар тізімі (Қажетсіздерін жоюға болады)"
    )
    if not users:
      st.info("Жүйеде қолданушылар жоқ.")
    else:
      for u in list(users):
        u_name = u.get("name", "Аты жоқ")
        u_username = u.get("username")
        u_role = u.get("role")

        col_info, col_del = st.columns([4, 1])
        with col_info:
          st.write(f"• **{u_name}** (@{u_username}) — Ролі: `{u_role}`")
        with col_del:
          if u_username != "kas01":
            if st.button("🗑️ Жою", key=f"del_user_{u_username}"):
              users = [
                  x for x in users if x.get("username") != u_username
              ]
              save_users(users)
              st.success(f"@{u_username} логині сәтті жойылды!")
              st.rerun()
          else:
            st.caption("Басты админ")
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

  with admin_tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ➕ Жаңа қолданушы қосу")
    new_u = st.text_input("Логин:")
    new_p = st.text_input("Құпия сөз:", type="password")
    new_n = st.text_input("Толық аты-жөні:")
    new_r = st.selectbox("Ролі:", ["user", "moderator", "admin"])

    if st.button("Қолданушыны сақтау", type="primary"):
      if new_u and new_p:
        if username_exists(new_u):
          st.error("❌ Бұл логин жүйеде бар!")
        else:
          users.append({
              "username": new_u.strip(),
              "password": hash_password(new_p.strip()),
              "name": new_n.strip(),
              "role": new_r,
              "combination": None,
          })
          save_users(users)
          st.success("✨ Қолданушы сәтті тіркелді!")
          st.rerun()
      else:
        st.error("⚠️ Логин мен құпия сөзді толтырыңыз!")
    st.markdown("</div>", unsafe_allow_html=True)

  with admin_tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_statistics_tab()
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 10. ОҚУШЫ (USER) ПАНЕЛІ (ҰБТ стиліндегі кең экранды формат)
# =========================================================
def user_page():
  # Жоғарғы жақ шапка (Аты-жөні және «Алдыңғы пән / Келесі пән» батырмалары)
  col_top1, col_top_prev, col_top_next, col_top_out = st.columns([3, 1.2, 1.2, 0.8])
  
  with col_top1:
    st.markdown(f"**👤 {st.session_state.full_name}**", unsafe_allow_html=True)

  comb_name = st.session_state.active_combination
  subj_list = combinations[comb_name] if comb_name else []
  sub_idx = st.session_state.current_subject_index

  with col_top_prev:
    if st.button("< Алдыңғы пән", use_container_width=True, disabled=(sub_idx == 0)):
      if sub_idx > 0:
        st.session_state.current_subject_index -= 1
        st.session_state.current_question_index = 0
        st.rerun()

  with col_top_next:
    is_last_subject = (sub_idx >= len(subj_list) - 1)
    next_subj_label = "Нәтижеге 🏁" if is_last_subject else "Келесі пән >"
    if st.button(next_subj_label, use_container_width=True, type="primary"):
      if not is_last_subject:
        st.session_state.current_subject_index += 1
        st.session_state.current_question_index = 0
      else:
        # Егер соңғы пән болса, соңына апару үшін index-ті соңына қоямыз
        st.session_state.current_subject_index = len(subj_list)
      st.rerun()

  with col_top_out:
    if st.button("🚪 Шығу", use_container_width=True):
      logout()

  st.markdown("---")

  if not st.session_state.test_started:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Тест комбинациясын таңдаңыз")
    selected_comb = st.selectbox(
        "Мамандық бағытын таңдаңыз:", list(combinations.keys())
    )

    if st.button("🚀 Тестті бастау", type="primary", use_container_width=True):
      st.session_state.active_combination = selected_comb
      st.session_state.test_started = True
      st.session_state.current_subject_index = 0
      st.session_state.current_question_index = 0
      st.session_state.test_answers = {}
      st.session_state.result_saved = False

      shuffled_data = {}
      for sub in combinations[selected_comb]:
        sub_qs = questions.get(sub, []).copy()
        random.shuffle(sub_qs)

        limit = subject_limits.get(sub, 40)
        sub_qs = sub_qs[:limit]

        processed_qs = []
        for q in sub_qs:
          answers = q["answers"].copy()
          correct_text = answers[q["correct"]]

          indexed_answers = list(enumerate(answers))
          random.shuffle(indexed_answers)

          new_answers = [item[1] for item in indexed_answers]
          new_correct_idx = new_answers.index(correct_text)

          processed_qs.append({
              "question": q["question"],
              "answers": new_answers,
              "correct": new_correct_idx,
          })
        shuffled_data[sub] = processed_qs

      st.session_state.shuffled_test_data = shuffled_data
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
  else:
    if sub_idx < len(subj_list):
      current_subject = subj_list[sub_idx]
      sub_questions = st.session_state.shuffled_test_data.get(
          current_subject, []
      )

      if not sub_questions:
        st.info(f"Бұл пөнде ({current_subject}) әзірге сұрақтар жоқ.")
      else:
        curr_q_idx = st.session_state.current_question_index
        num_qs = len(sub_questions)

        # ҰБТ стиліндегі жоғарғы жақтағы горизонталь палитра батырмалары
        st.markdown(f"**Бөлім: {current_subject}**")
        
        # Барлық сұрақтардың номерлерін горизонталь тізіп шығару (scrollbar арқылы)
        if "test_answers" not in st.session_state:
          st.session_state.test_answers = {}
        if current_subject not in st.session_state.test_answers:
          st.session_state.test_answers[current_subject] = {}

        cols_palette = st.columns(min(num_qs, 32)) # Элементтер көп болса да сыйғызу үшін
        for q_i in range(num_qs):
          col_idx = q_i % len(cols_palette)
          with cols_palette[col_idx]:
            is_current = (q_i == curr_q_idx)
            btn_label = f"[{q_i+1}]" if is_current else str(q_i+1)
            if st.button(btn_label, key=f"pal_{sub_idx}_{q_i}", use_container_width=True):
              st.session_state.current_question_index = q_i
              st.rerun()

        st.markdown("---")

        # Оң жақ жоғары бұрышта «Келесі сұрақ» батырмасы және сұрақ нөмірі
        col_q_title, col_next_q_btn = st.columns([6, 1.5])
        with col_q_title:
          st.markdown(f"#### Сұрақ №{curr_q_idx + 1}")
        with col_next_q_btn:
          is_last_q_in_sub = (curr_q_idx == num_qs - 1)
          nxt_label = "Келесі пән >" if is_last_q_in_sub else "Келесі сұрақ >"
          if st.button(nxt_label, type="primary", use_container_width=True):
            if not is_last_q_in_sub:
              st.session_state.current_question_index += 1
            else:
              st.session_state.current_subject_index += 1
              st.session_state.current_question_index = 0
            st.rerun()

        # Сұрақ және нұсқалар
        q = sub_questions[curr_q_idx]
        st.write(q["question"])

        current_sub_ans = st.session_state.test_answers[current_subject]
        prev_ans = current_sub_ans.get(curr_q_idx)
        default_ix = 0
        if prev_ans in q["answers"]:
          default_ix = q["answers"].index(prev_ans)

        selected_ans = st.radio(
            "Жауап нұсқасын таңдаңыз:",
            q["answers"],
            index=default_ix,
            key=f"radio_q_{sub_idx}_{curr_q_idx}"
        )

        st.session_state.test_answers[current_subject][curr_q_idx] = selected_ans

    else:
      # Барлық пәндер аяқталды -> Нәтиже мен қателермен жұмыс
      total_score = 0
      for subject in subj_list:
        sub_questions = st.session_state.shuffled_test_data.get(subject, [])
        user_sub_ans = st.session_state.test_answers.get(subject, {})
        for q_idx, q in enumerate(sub_questions):
          chosen = user_sub_ans.get(q_idx)
          correct_text = q["answers"][q["correct"]]
          if chosen == correct_text:
            total_score += 1

      if not st.session_state.get("result_saved", False):
        history = load_results_history()
        new_result = {
            "username": st.session_state.username,
            "name": st.session_state.full_name,
            "combination": comb_name,
            "score": total_score,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        history.append(new_result)
        save_results_history(history)
        st.session_state.result_saved = True

      st.markdown('<div class="card">', unsafe_allow_html=True)
      st.markdown(
          f"### 🎉 Тест аяқталды! Жинаған ұпайыңыз: **{total_score}**"
      )
      st.info("Нәтижеңіз администратор базасына автоматты түрде сақталды.")
      st.markdown("</div>", unsafe_allow_html=True)

      st.markdown('<div class="card">', unsafe_allow_html=True)
      st.markdown("### 📝 Қателермен жұмыс (Талдау)")
      
      has_mistakes = False
      for subject in subj_list:
        sub_questions = st.session_state.shuffled_test_data.get(subject, [])
        user_sub_ans = st.session_state.test_answers.get(subject, {})
        
        sub_mistakes = []
        for q_idx, q in enumerate(sub_questions):
          chosen = user_sub_ans.get(q_idx)
          correct_text = q["answers"][q["correct"]]
          if chosen != correct_text:
            sub_mistakes.append((q, chosen, correct_text))

        if sub_mistakes:
          has_mistakes = True
          st.markdown(f"#### 📚 Пән: {subject}")
          for idx, (q, chosen, correct_text) in enumerate(sub_mistakes, 1):
            st.markdown(f"**{idx}. {q['question']}**")
            st.markdown(f"❌ Сіздің жауабыңыз: `{chosen if chosen else 'Жауап берілмеді'}`")
            st.markdown(f"✅ Дұрыс жауап: `{correct_text}`")
            st.markdown("---")

      if not has_mistakes:
        st.success("🌟 Керемет! Барлық сұраққа дұрыс жауап бердіңіз!")

      st.markdown("</div>", unsafe_allow_html=True)

      if st.button("🔄 Жаңа тест бастау", use_container_width=True):
        st.session_state.test_started = False
        st.session_state.current_subject_index = 0
        st.session_state.current_question_index = 0
        st.session_state.test_answers = {}
        st.session_state.shuffled_test_data = {}
        st.session_state.result_saved = False
        st.rerun()


# =========================================================
# 11. РОУТЕР
# =========================================================
def main():
  if not st.session_state.logged_in:
    login_page()
  else:
    role = st.session_state.get("role", "user")

    if role == "admin":
      admin_page()
    elif role == "moderator":
      moderator_page()
    elif role == "user":
      user_page()
    else:
      st.warning(f"⚠️ Белгісіз рөл анықталды: {role}")
      if st.button("🚪 Шығу және қайта кіру"):
        logout()


if __name__ == "__main__":
  main()
