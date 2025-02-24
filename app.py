import streamlit as st
from rag import process_query  # Importing the function

# ✅ Streamlit UI Config
st.set_page_config(page_title="AgentPilot - AI Framework Explorer", layout="wide")

# ✅ Custom CSS for Enhanced UI & Attractiveness
st.markdown("""
    <style>
        /* Background Gradient */
        html, body, [class*="st-"] { 
            font-family: 'Arial', sans-serif; 
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }
        /* Title */
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #00eaff;
            text-shadow: 3px 3px 10px rgba(0, 234, 255, 0.7);
        }
        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #d4d4d4;
        }
        /* Description */
        .description {
            text-align: center;
            font-size: 18px;
            font-style: italic;
            color: #c2c2c2;
            margin-bottom: 20px;
        }
        /* Response Box */
        .response-container {
            background-color: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 2px 2px 15px rgba(0, 234, 255, 0.3);
            font-size: 18px;
            line-height: 1.6;
        }
        /* Sidebar */
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #00eaff;
        }
        /* Selection Box Effects */
        .stSelectbox, .stRadio {
            transition: 0.3s ease-in-out;
        }
        .stSelectbox:hover, .stRadio:hover {
            box-shadow: 0px 0px 10px rgba(0, 234, 255, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Page Title
st.markdown('<p class="title">🧭 AgentPilot - AI Framework Explorer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🚀 Navigate AI Agent Frameworks with Ease!</p>', unsafe_allow_html=True)

# ✅ Short Description
st.markdown('<p class="description">AgentPilot helps you explore AI agent frameworks like LangChain, CrewAI, and more. Choose your AI model and get expert answers instantly!</p>', unsafe_allow_html=True)

# ✅ Sidebar: AI Agent Framework & LLM Selection
st.sidebar.markdown('<p class="sidebar-title">⚙️ Configuration Panel</p>', unsafe_allow_html=True)

# ✅ Choose AI Agent Framework
source_option = st.sidebar.selectbox(
    "🕵️‍♂️ Select an AI Agent Framework:",
    ["LangChain", "CrewAI", "LangGraph", "PhiData"]
)

# ✅ Choose LLM Model
llm_option = st.sidebar.radio(
    "🤖 Select LLM Model:",
    ["Gemini 2.0", "Gemini 1.5"]
)

# ✅ User Input
user_query = st.text_input("🔍 Enter your question:", placeholder="Ask me anything about AI agent frameworks!")

# ✅ Processing & Displaying Response
if user_query:
    with st.spinner("🧠 Thinking... Please wait!"):
        result = process_query(user_query, source=source_option, llm=llm_option)  

    # ✅ Display AI Response
    st.subheader("📝 AgentPilot's Response:")
    st.markdown(f'<div class="response-container">{result.content}</div>', unsafe_allow_html=True)
