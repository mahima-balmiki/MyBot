import streamlit as st
from rag import generate_answer, process_urls
import html  # to escape text content safely
import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

# Page configuration
st.set_page_config(page_title="WebGenie 🔗", page_icon="🧞", layout="centered")

# Inject full-page background + styles
st.markdown("""
<style>
/* Entire App Background */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #e3f2fd !important;
    background-image: linear-gradient(to right, #e3f2fd, #fce4ec);
    background-attachment: fixed;
    background-size: cover;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #e1f5fe !important;
    padding-top: 2rem;
}

/* Input Fields */
.stTextInput>div>div>input {
    border: 2px solid #64b5f6 !important;
    background-color: #ffffff !important;
    border-radius: 10px !important;
    padding: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #43a047 !important;
    color: white !important;
    border-radius: 10px !important;
    height: 3em;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #388e3c !important;
    transform: scale(1.02);
}

/* Card Layout */
.card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    font-size: 16px;
    line-height: 1.6;
}

/* Section Headings */
.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-top: 30px;
    color: #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("## 🧞‍♂️ Welcome to **WebGenie**")
st.markdown("Your magical assistant to answer questions from any web content! 🌐💬")

# Sidebar
st.sidebar.header("📥 Enter URLs to Process")
url1 = st.sidebar.text_input("🔗 URL 1")
url2 = st.sidebar.text_input("🔗 URL 2")
url3 = st.sidebar.text_input("🔗 URL 3")

status_placeholder = st.sidebar.empty()

# Button to process URLs
if st.sidebar.button("🚀 Process URLs"):
    urls = [url for url in (url1, url2, url3) if url.strip()]
    if not urls:
        status_placeholder.error("⚠️ Please enter at least one valid URL.")
    else:
        for status in process_urls(urls):
            status_placeholder.info(f"🔄 {status}")

# Divider
st.markdown("<hr style='border-top: 2px solid #64b5f6;'>", unsafe_allow_html=True)

# Ask question
st.markdown("### 💬 Ask Me Anything About the URLs")
query = st.text_input("📝 Type your question here:")
ask_button = st.button("💬 Ask WebGenie")

if ask_button and query.strip():
    with st.spinner("🔍 WebGenie is thinking..."):
        try:
            answer, sources = generate_answer(query)
            st.success("✅ Here's what I found!")

            # Display the Answer
            st.markdown("<div class='section-title'>🧠 Answer</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>{html.escape(answer)}</div>", unsafe_allow_html=True)

            # Display the Sources
            if sources:
                st.markdown("<div class='section-title'>📚 Sources</div>", unsafe_allow_html=True)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                for source in sources.strip().split("\n"):
                    if source.strip():
                        st.markdown(f"🔗 [{source}]({source})")
                st.markdown("</div>", unsafe_allow_html=True)

        except RuntimeError:
            st.error("⚠️ Please process the URLs before asking a question.")
