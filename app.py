import streamlit as st
from webscraper import scrape_text_from_url  # type: ignore
from pdf_handler import extract_text_from_pdf # type: ignore
from coding_helper import get_coding_help # type: ignore
from math_helper import solve_math_problem # type: ignore
from agent import ask_model # type: ignore


# Modernes Layout
st.set_page_config(page_title="📘 StudyBot", layout="wide")

st.markdown("""
    <style>
        .big-font {
            font-size: 30px !important;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
        }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            border-radius: 6px;
            padding: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialisiere Chat-Verlauf
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<div class='big-font'>📘 StudyBot – Dein smarter Studienbegleiter</div>", unsafe_allow_html=True)
st.markdown("Wähle eine Funktion in der Seitenleiste aus, lade deine Inhalte hoch oder stelle deine Frage.")

mode = st.sidebar.radio("🔧 Modus auswählen", ["Webseite", "PDF", "Coding", "Mathe"])

# Webseite analysieren
if mode == "Webseite":
    st.header("🌐 Webseiten-Analyse")
    url = st.text_input("🔗 Website-Link:")
    question = st.text_input("❓ Frage zur Website:")
    if st.button("Frage stellen"):
        content = scrape_text_from_url(url)
        answer = ask_model(f"{content}\n\nFrage: {question}")
        st.session_state.chat_history.append(("🌐 Du", question))
        st.session_state.chat_history.append(("🤖 Bot", answer))
        st.write(answer)

# PDF analysieren
elif mode == "PDF":
    st.header("📄 Frage zu einem PDF stellen")
    file = st.file_uploader("PDF hochladen", type="pdf")
    question = st.text_input("❓ Frage zum PDF:")
    if st.button("Frage stellen") and file:
        text = extract_text_from_pdf(file)
        answer = ask_model(f"{text}\n\nFrage: {question}")
        st.session_state.chat_history.append(("📄 Du", question))
        st.session_state.chat_history.append(("🤖 Bot", answer))
        st.write(answer)

# Coding
elif mode == "Coding":
    st.header("💻 Hilfe zu Programmierung")
    code = st.text_area("Beschreibe dein Problem oder gib Code ein:")
    if st.button("Antwort erhalten"):
        answer = get_coding_help(code)
        st.session_state.chat_history.append(("💻 Du", code))
        st.session_state.chat_history.append(("🤖 Bot", answer))
        st.code(answer)

# Mathe
elif mode == "Mathe":
    st.header("📐 Mathe-Fragen lösen")
    problem = st.text_area("🧮 Matheproblem eingeben (z.B. Gleichung, Term):")
    if st.button("Antwort erhalten"):
        answer = solve_math_problem(problem)
        st.session_state.chat_history.append(("📐 Du", problem))
        st.session_state.chat_history.append(("🤖 Bot", answer))
        st.write(answer)

# Chat-Verlauf anzeigen
st.divider()
st.markdown("### 💬 Verlauf")
for sender, msg in st.session_state.chat_history:
    st.markdown(f"{sender}:** {msg}")

if st.button("🔁 Verlauf löschen"):
    st.session_state.chat_history = []
    st.success("Verlauf wurde gelöscht.")
