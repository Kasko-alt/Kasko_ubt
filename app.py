import datetime
import hashlib
import json
import os
import random
import re
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# KASYM EDU CONFIG
# =========================================================
st.set_page_config(page_title="KASYM EDU", page_icon="🎓", layout="wide")

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results_history.json"
USERS_FILE = "users.json"


# =========================================================
# ҚАУІПСІЗДІК: ПАРОЛЬДІ ХЭШТЕУ
# =========================================================
def hash_password(password: str) -> str:
  return hashlib.sha256(password.encode("utf-8")).hexdigest()


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
}


# =========================================================
# ҚОЛДАНУШЫЛАР ЖҮЙЕСІ (Админді міндетті түрде қамтамасыз ету)
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

  # Админ бар-жоғын қатаң тексеру және қалпына келтіру
  admin_exists = any(u.get("username") == "kas01" for u in users_list)
  if not admin_exists:
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
# SESSION STATE (Админ ретінде автоматты түрде тексеру үшін)
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

if "current_subject_idx" not in st.session_state:
  st.session_state.current_subject_idx = 0
if "current_question_idx" not in st.session_state:
  st.session_state.current_question_idx = 0
if "test_answers" not in st.session_state:
  st.session_state.test_answers = {}

# =========================================================
# СТИЛЬДЕР
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
  st.session_state.test_started = False
  st.session_state.active_combination = None
  st.session_state.test_answers = {}
  st.rerun()


# =========================================================
# LOGIN PAGE (Жылдам кіру батырмасы қосылды)
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
    st.markdown(
        "<h3 style='text-align: center; margin-bottom: 20px;'>🔐 Жүйеге"
        " кіру</h3>",
        unsafe_allow_html=True,
    )
    username = st.text_input("Логин", key="login_username")
    password = st.text_input("Құпия сөз", type="password", key="login_password")

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

    st.markdown("---")
    # Тест жасауға ыңғайлы болу үшін бір рет басып админ болып кіретін кнопка
    if st.button(
        "👑 Админ болып бірден кіру (Тест үшін)", use_container_width=True
    ):
      st.session_state.logged_in = True
      st.session_state.username = "kas01"
      st.session_state.full_name = "KASYM"
      st.session_state.role = "admin"
      st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# МОДЕРАТОР ЖӘНЕ АДМИН ПАНЕЛДЕРІ
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
          if opt_letter in ["A", "А"]:
            correct_index = idx
          elif opt_letter in ["B", "Б"]:
            correct_index = idx
          elif opt_letter in ["C", "В"]:
            correct_index = idx
          elif opt_letter in ["D", "Г"]:
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


def render_question_manager():
  tab1, tab2, tab3 = st.tabs([
      "⚡ Жылдам массалық жүктеу (40+)",
      "✍️ Жеке сұрақ қосу",
      "🗑️ Сұрақтарды жою",
  ])

  with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_subject_bulk = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="bulk_sub"
    )
    raw_text_input = st.text_area(
        "✍️ Барлық сұрақтарды осында көшіріп қойыңыз (Ctrl + V):", height=250
    )

    if st.button(
        "🚀 Барлық сұрақтарды базаға қосу",
        use_container_width=True,
        type="primary",
    ):
      if raw_text_input.strip():
        parsed = parse_bulk_questions(raw_text_input)
        if parsed:
          if selected_subject_bulk not in questions:
            questions[selected_subject_bulk] = []
          questions[selected_subject_bulk].extend(parsed)
          save_questions()
          st.success(f"✨ Сәтті! Барлығы **{len(parsed)}** сұрақ базаға қосылды!")
        else:
          st.error("⚠️ Формат танылмады.")
      else:
        st.warning("⚠️ Өріс бос болмауы тиіс!")
    st.markdown("</div>", unsafe_allow_html=True)

  with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_subject = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="single_sub"
    )
    question_text = st.text_area("✍️ Сұрақты толық жазыңыз:")

    col_a, col_b = st.columns(2)
    with col_a:
      ans1 = st.text_input("А нұсқасы:")
      ans3 = st.text_input("В нұсқасы:")
    with col_b:
      ans2 = st.text_input("Б нұсқасы:")
      ans4 = st.text_input("Г нұсқасы:")

    correct_option = st.selectbox(
        "✅ Дұрыс жауап:",
        ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"],
    )
    correct_index = ["А нұсқасы", "Б нұсқасы", "В нұсқасы", "Г нұсқасы"].index(
        correct_option
    )

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
    st.markdown("</div>", unsafe_allow_html=True)

  with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    del_subject = st.selectbox(
        "📚 Пәнді таңдаңыз:", all_subjects, key="del_sub"
    )
    sub_list = questions.get(del_subject, [])

    if not sub_list:
      st.info(f"⚠️ {del_subject} пәнінде әзірге сұрақтар жоқ.")
    else:
      q_options = {
          f"{i+1}. {q['question'][:50]}...": i for i, q in enumerate(sub_list)
      }
      selected_q_label = st.selectbox(
          "Өшіретін сұрақты таңдаңыз:", list(q_options.keys())
      )

      if st.button("🗑️ Таңдалған сұрақты жою", type="primary"):
        idx_to_delete = q_options[selected_q_label]
        removed = sub_list.pop(idx_to_delete)
        questions[del_subject] = sub_list
        save_questions()
        st.success("🗑️ Сәтті жойылды!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def moderator_page():
  if st.button("🚪 Шығу"):
    logout()
  st.markdown(
      '<div class="kasym-title" style="font-size: 32px;">🛠️ Модератор'
      " панелі</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="kasym-subtitle">Сұрақтар базасын басқару</div>',
      unsafe_allow_html=True,
  )
  render_question_manager()


def admin_page():
  if st.button("🚪 Шығу"):
    logout()
  st.markdown(
      '<div class="kasym-title" style="font-size: 32px;">👑 Администратор'
      " панелі</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="kasym-subtitle">Қолданушыларды басқару және статистика</div>',
      unsafe_allow_html=True,
  )

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
              "combination": None,
          })
          save_users(users)
          st.success("✨ Қолданушы сәтті тіркелді!")
      else:
        st.error("⚠️ Логин мен құпия сөзді толтырыңыз!")

    st.markdown("---")
    st.markdown("### 📋 Қолданушылар тізімі")
    for u in users:
      st.write(
          f"- **{u.get('name', 'Аты жоқ')}** (@{u.get('username')}) — Ролі:"
          f" `{u.get('role')}`"
      )
    st.markdown("</div>", unsafe_allow_html=True)

  with admin_tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    total_q = sum(len(q_list) for q_list in questions.values())
    st.metric("Барлық сұрақтар саны", total_q)
    st.metric("Тіркелген қолданушылар саны", len(users))
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# РОУТЕР (Қатаң рөл тексеру)
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
    else:
      # Оқушы панелі (қажет болса толықтыруға болады)
      st.warning("⚠️ Бұл бөлім оқушыларға арналған.")
      if st.button("Шығу"):
        logout()


if __name__ == "__main__":
  main()
