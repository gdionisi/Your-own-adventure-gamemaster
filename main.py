import streamlit as st
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Mistral Chat Interface", page_icon="🤖", layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# API configuration
API_KEY = os.getenv("MISTRAL_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

client = Mistral(api_key=API_KEY)

if not API_KEY or not AGENT_ID:
    st.error("Please set your MISTRAL_API_KEY and AGENT_ID in the .env file")
    st.stop()

# Title and description
st.title("🤖 Mistral Chat Interface")
st.markdown("Chat with your fine-tuned Mistral model!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_response = client.agents.complete(
                    agent_id=AGENT_ID,
                    messages=[{"role": "user", "content": prompt}],
                )

                # Extract and display the response
                assistant_response = chat_response.choices[0].message.content
                st.markdown(assistant_response)

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()
