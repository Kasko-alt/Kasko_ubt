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
# 3. ПӘНДЕР МЕН КОМБИНАЦИЯЛАР
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
if "test_answers" not in st.session_state:
  st.session_state.test_answers = {}

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
  st.session_state.username = ""
  st.session_state.full_name = ""
  st.session_state.test_started = False
  st.session_state.active_combination = None
  st.session_state.current_subject_index = 0
  st.session_state.test_answers = {}
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
# СТАТИСТИКАНЫ КӨРСЕТУ ЖӘНЕ СҮЗГІЛЕУ ФУНКЦИЯСЫ (ОРТАҚ)
# =========================================================
def render_statistics_tab():
  st.markdown("### 📊 Оқушылардың тест нәтижелері мен статистикасы")
  history = load_results_history()

  if not history:
    st.info("⚠️ Әзірге ешбір оқушы тест тапсырған жоқ.")
    return

  # Іздеу және сүзу (Filter & Search) элементтері
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

  # Сүзгіні қолдану
  filtered_history = []
  for h in history:
    match_search = (
        search_query in h.get("name", "").lower()
        or search_query in h.get("username", "").lower()
    )
    match_comb = (
        comb_filter == "Барлығы" or h.get("combination") == comb_filter
    )
    if match_search and match_comb:
      filtered_history.append(h)

  st.caption(f"Табылған нәтижелер саны: {len(filtered_history)}")

  if not filtered_history:
    st.warning("⚠️ Іздеу шарттарына сәйкес ешбір нәтиже табылмады.")
  else:
    for idx, h in enumerate(reversed(filtered_history)):
      st.markdown(
          f"**{idx+1}. Оқушы:** {h.get('name')} (@{h.get('username')}) |"
          f" **Комбинация:** {h.get('combination')} | **Ұпай:**"
          f" `{h.get('score')}` | **Күні:** {h.get('date')}"
      )


# =========================================================
# 8. МОДЕРАТОР ПАНЕЛІ (Статистиканы көру мүмкіндігімен)
# =========================================================
def parse_bulk_questions(raw_text):
  questions_list = []
  blocks = re.split(r"\n\s*(?=\d+[\.\)])", raw_text)
  for block in blocks:
    if not block.strip():
      continue
    lines = [
        line.strip() for line in block.strip().split("\n") if line.strip()
    ]
    if len(lines) < 5:
      continue
    q_text = lines[0]
    q_text = re.sub(r"^\d+[\.\)]\s*", "", q_text)
    answers = []
    correct_index = 0
    for idx, line in enumerate(lines[1:5]):
      match = re.match(r"^([A-DА-Гa-dа-г])[\.\)]\s*(.*)", line, re.IGNORECASE)
      if match:
        opt_letter = match.group(1).upper()
        opt_text = match.group(2)
        answers.append(opt_text)
        if "*" in line or "(+)" in line or "Дұрыс" in line:
          if opt_letter in ["A", "А", "B", "Б", "C", "В", "D", "Г"]:
            correct_index = idx
      else:
        answers.append(line)
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
          st.error("⚠️ Формат қате.")
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
# 9. ӘКІМШІ (ADMIN) ПАНЕЛІ (Іздеу және сүзу мүмкіндігімен)
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
# 10. ОҚУШЫ (USER) ПАНЕЛІ
# =========================================================
def user_page():
  col1, col2 = st.columns([6, 1])
  with col1:
    st.markdown(
        f'<div class="kasym-title" style="font-size: 32px;">🎓 Қош келдіңіз,'
        f" {st.session_state.full_name}!</div>",
        unsafe_allow_html=True,
    )
  with col2:
    if st.button("🚪 Шығу", use_container_width=True):
      logout()

  st.markdown(
      '<div class="kasym-subtitle">Оқушы кабинеті және ҰБТ тест'
      " тапсыру</div>",
      unsafe_allow_html=True,
  )

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
      st.session_state.test_answers = {}
      st.session_state.result_saved = False
      st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
  else:
    comb_name = st.session_state.active_combination
    subj_list = combinations[comb_name]
    sub_idx = st.session_state.current_subject_index

    if sub_idx < len(subj_list):
      current_subject = subj_list[sub_idx]
      st.markdown(f"### 📚 Пән ({sub_idx + 1}/{len(subj_list)}): {current_subject}")
      st.markdown("---")

      sub_questions = questions.get(current_subject, [])
      if not sub_questions:
        st.info(f"Бұл пөнде ({current_subject}) әзірге сұрақтар жоқ.")
        if st.button("Келесі пәнге өту ➡"):
          st.session_state.current_subject_index += 1
          st.rerun()
      else:
        with st.form(key=f"subject_form_{sub_idx}"):
          subject_answers = {}
          for q_idx, q in enumerate(sub_questions):
            ans = st.radio(
                f"{q_idx + 1}. {q['question']}", q["answers"], key=f"q_{sub_idx}_{q_idx}"
            )
            subject_answers[q_idx] = ans
            st.markdown("")

          submitted = st.form_submit_button(
              "Келесі пәнге өту ➡"
              if sub_idx < len(subj_list) - 1
              else "Тестті аяқтау 🏁"
          )
          if submitted:
            st.session_state.test_answers[current_subject] = subject_answers
            st.session_state.current_subject_index += 1
            st.rerun()
    else:
      total_score = 0
      for subject in subj_list:
        sub_questions = questions.get(subject, [])
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

      if st.button("🔄 Жаңа тест бастау"):
        st.session_state.test_started = False
        st.session_state.current_subject_index = 0
        st.session_state.test_answers = {}
        st.session_state.result_saved = False
        st.rerun()
      st.markdown("</div>", unsafe_allow_html=True)


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
