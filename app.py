import streamlit as st
import os
import re
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Your own adventure", page_icon="🤖", layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# API configuration
API_KEY = os.getenv("MISTRAL_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

client = Mistral(api_key=API_KEY)

def extract_choices(text):
    # Find all numbered choices in the text
    choices = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', text, re.DOTALL)
    # Remove the choices from the main text
    main_text = re.sub(r'\n\d+\.\s*.*?(?=\n\d+\.|$)', '', text, flags=re.DOTALL).strip()
    return main_text, choices

def main():
    if not API_KEY or not AGENT_ID:
        st.error("Please set your MISTRAL_API_KEY and AGENT_ID in the .env file")
        st.stop()

    # Title and description
    st.title("📖 Your own adventure")

    last_user_choice = ""

    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Split the message into main text and choices
                main_text, choices = extract_choices(message["content"])
                st.markdown(main_text)
                if choices:
                    # Create a unique key for this message's buttons
                    button_key = f"choice_{idx}"
                    # Display buttons for choices vertically
                    for idx, choice in enumerate(choices):
                        if st.button(choice.strip(), key=f"{button_key}_{idx}"):
                            # Add user's choice to chat history
                            last_user_choice = {"role": "user", "content": choice.strip()}
                            st.session_state.messages.append(last_user_choice)
                            st.rerun()
            else:
                st.markdown(message["content"])

    # Initial chat input
    if not st.session_state.messages:
        if st.button("Start the game"):
            st.session_state.messages.append({"role": "user", "content": "Start the game"})
            st.rerun()

    # Generate response if there's a new user message
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat_response = client.agents.complete(
                        agent_id=AGENT_ID,
                        messages=[{"role": message["role"], "content": message["content"]} for message in st.session_state.messages],
                    )

                    # Extract and display the response
                    assistant_response = chat_response.choices[0].message.content
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.stop()

if __name__ == "__main__":
    main()
