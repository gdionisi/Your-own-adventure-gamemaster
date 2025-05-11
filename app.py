import random
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

# Initialize session state for chat history and current choices
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_choices" not in st.session_state:
    st.session_state.current_choices = None

# API configuration
API_KEY = os.getenv("MISTRAL_API_KEY")
STORY_AGENT_ID = os.getenv("STORY_AGENT_ID")
CHOICES_AGENT_ID = os.getenv("CHOICES_AGENT_ID")

client = Mistral(api_key=API_KEY)

SUGGESTED_THEMES = [
    "fantasy",
    "sci-fi",
    "cyberpunk",
    "mystery",
    "horror",
    "romance",
    "adventure",
    "comedy",
    "drama",
    "thriller",
    "western",
    "historical",
    "steampunk",
    "superhero",
    "poetic",
    "slice of life",
]

def get_random_theme():
    return random.choice(SUGGESTED_THEMES)

def extract_choices(text):
    # Find all numbered choices in the text
    choices = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', text, re.DOTALL)
    # Remove the choices from the main text
    main_text = re.sub(r'\n\d+\.\s*.*?(?=\n\d+\.|$)', '', text, flags=re.DOTALL).strip()
    return main_text, choices

def main():
    if not API_KEY or not STORY_AGENT_ID or not CHOICES_AGENT_ID:
        st.error("Please set your MISTRAL_API_KEY, STORY_AGENT_ID, and CHOICES_AGENT_ID in the .env file")
        st.stop()

    # Title and description
    st.title("📖 Your own adventure")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display current choices if they exist
    if st.session_state.current_choices:
        st.markdown("What would you like to do?")
        for idx, choice in enumerate(st.session_state.current_choices):
            if st.button(choice.strip(), key=f"choice_{idx}"):
                # Add user's choice to chat history
                st.session_state.messages.append({"role": "user", "content": choice.strip()})
                st.session_state.current_choices = None
                st.rerun()

    # Initial chat input
    if not st.session_state.messages:
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        with col1:
            st.text("Start a")
        with col2:
            story_type = st.text_input(value=st.session_state.get("story_type", ""), label="Story type", placeholder="fantasy, sci-fi, cyberpunk...", label_visibility="collapsed")
        with col3:
            st.text("story")
        with col4:
            col41, col42 = st.columns([1, 1])
            with col41:
                if st.button("▶️", help="Start the adventure"):
                    if story_type:
                        st.session_state.messages.append({"role": "user", "content": f"Start a {story_type} story"})
                    st.rerun()
            with col42:
                if st.button("🔄", help="Random story"):
                    st.session_state.story_type = get_random_theme()
                    st.rerun()

    # Generate response if there's a new user message
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # First, get the story continuation from the story agent
                    story_response = client.agents.complete(
                        agent_id=STORY_AGENT_ID,
                        messages=[{"role": message["role"], "content": message["content"]} for message in st.session_state.messages],
                    )
                    
                    if not story_response or not story_response.choices:
                        st.error("Failed to get story response")
                        st.stop()
                        
                    story_content = story_response.choices[0].message.content
                    
                    # Add the story content to the chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": story_content}
                    )
                    
                    # Then, get the choices from the choices agent
                    choices_prompt = f"Based on this story segment, suggest 3-4 possible choices for the player:\n\n{story_content}"
                    choices_response = client.agents.complete(
                        agent_id=CHOICES_AGENT_ID,
                        messages=[{"role": "user", "content": choices_prompt}],
                    )
                    
                    if not choices_response or not choices_response.choices:
                        st.error("Failed to get choices response")
                        st.stop()
                        
                    choices_content = choices_response.choices[0].message.content
                    _, choices = extract_choices(choices_content)
                    
                    # Store the choices in session state
                    st.session_state.current_choices = choices
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.stop()

if __name__ == "__main__":
    main()
