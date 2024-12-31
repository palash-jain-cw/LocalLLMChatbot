import streamlit as st
import ollama
from localllmchatbot.logger_setup import loguru_setup
from localllmchatbot.LocalModelChat.LocalModelChat import LocalModelChat
from localllmchatbot.LocalModelChat.utils import stream_parser

# Initialize logger setup
logger = loguru_setup()

st.set_page_config(page_title="Local Model Chat")

if "models" not in st.session_state:
    models = [m.model.replace(":latest", "") for m in ollama.list().models]


with st.sidebar:
    with st.form("Setup Chatbot"):
        model_select = st.selectbox(
            "Select Model",
            models,
        )

        system_prompt = st.text_area(
            "System Prompt",
            placeholder="You are a helpful assistant. Respond to the user queries in less than 50 words",
            height=150
        )
        col1, col2 = st.columns(2)
        with col1:
            update_chatbot = st.form_submit_button("Setup Bot")
        with col2:
            clear_memory = st.form_submit_button("Clear Memory")


if ("llm" not in st.session_state) or update_chatbot:
    st.session_state.llm = LocalModelChat(
        model=model_select,
        base_url="",
        system_prompt=system_prompt,
        tools=[],
    )

if clear_memory:
    st.session_state.llm._clear_message_history()
# Display chat messages from history on app rerun
for message in st.session_state.llm.message_history:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner(text="Thinking..."):
        response = st.session_state.llm._generate_chat_response(prompt=prompt,stream=True)
        with st.chat_message("assistant"):
            response = st.write_stream(stream=stream_parser(response)) 
        st.session_state.llm.message_history.append(
            {"role": "assistant", "content": response}
        )
        # with st.chat_message("assistant"):
        #     st.markdown(response)
