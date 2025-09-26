import streamlit as st
from app.chat import ChatManager
from app.utils import format_response, log_error
from logger import CustomLogger

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Custom GPT Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ----------------------------
# Logger Setup
# ----------------------------
logger = CustomLogger().get_logger()

# ----------------------------
# Initialize ChatManager
# ----------------------------
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

chat_manager = st.session_state.chat_manager

# ----------------------------
# Initialize messages
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# UI Title
# ----------------------------
st.title("Custom GPT Chatbot")
st.write("Ask me anything — concise answers or detailed explanations!")

# ----------------------------
# Chat Input
# ----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    try:
        # Log and store user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        logger.info(f"User: {user_input}")

        # Get AI response
        ai_response = chat_manager.get_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        logger.info(f"Assistant: {ai_response}")

    except Exception as e:
        log_error(f"Error during chat: {e}")
        st.error("Something went wrong while processing your request.")

# ----------------------------
# Display chat messages with clear distinction
# ----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#cce5ff;  /* light blue background */
                color:#000000;             /* black text */
                padding:10px;
                border-radius:8px;
                margin-bottom:8px;
            ">
                <strong>You:</strong> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#f2f2f2;  /* light gray background */
                color:#000000;             /* black text */
                padding:10px;
                border-radius:8px;
                margin-bottom:8px;
            ">
                <strong>Assistant:</strong> {format_response(msg['content'])}
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------
# Sidebar: Conversation History
# ----------------------------
with st.sidebar:
    st.subheader("Conversation History")
    for msg in st.session_state.messages:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# ----------------------------
# Sidebar: Quick Prompt Buttons
# ----------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Prompts")

# -----------------------------
# Explain Code Button
# -----------------------------
def handle_explain_code():
    prompt = "Explain this code"
    st.session_state.messages.append({"role": "user", "content": prompt})
    ai_response = chat_manager.get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    logger.info(f"Quick Prompt: {prompt}")
    logger.info(f"Assistant: {ai_response}")

if st.sidebar.button("Explain code", key="btn_explain_code"):
    handle_explain_code()

# -----------------------------
# Define Term Button
# -----------------------------
def handle_define_term():
    prompt = "Define this term"
    st.session_state.messages.append({"role": "user", "content": prompt})
    ai_response = chat_manager.get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    logger.info(f"Quick Prompt: {prompt}")
    logger.info(f"Assistant: {ai_response}")

if st.sidebar.button("Define term", key="btn_define_term"):
    handle_define_term()

# -----------------------------
# Give Concise Answer Button
# -----------------------------
def handle_concise_answer():
    last_user_msg = next(
        (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), ""
    )
    if last_user_msg:
        prompt = f"Answer concisely: {last_user_msg}"
        st.session_state.messages.append({"role": "user", "content": prompt})
        ai_response = chat_manager.get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        logger.info(f"Quick Prompt: {prompt}")
        logger.info(f"Assistant: {ai_response}")

if st.sidebar.button("Give concise answer", key="btn_concise_answer"):
    handle_concise_answer()


