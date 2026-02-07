import asyncio
import streamlit as st
from music_assistant import MusicAssistant  # import your class
import subprocess
import os

st.set_page_config(page_title="Music Assistant", page_icon="🎧")



# Global variable to hold the process
if "process" not in st.session_state:
    st.session_state.process = None

st.title("Toggle music sync")

# Path to your Python file
script_path = r"C:\Users\amita\PycharmProjects\music_assistant\music_sync.py"

# Button to start/stop
if st.button("Start / Stop Script"):
    if st.session_state.process is None or st.session_state.process.poll() is not None:
        # Start the script
        st.session_state.process = subprocess.Popen(["python", script_path])
        st.success("Music sync started!")
    else:
        # Stop the script
        st.session_state.process.terminate()
        st.session_state.process = None
        st.warning("Music sync stopped!")


st.title("🎧 Music Assistant")
st.markdown(
    "Type a song name, movie name, or anything you remember about the track.<br>"
    "Please be as specific as possible for better results. For example, you can include the artist's name, "
    "the year it was released, or any distinctive lyrics you remember.<br>"
    "The more details you provide, the better I can assist you in finding the right song!",
    unsafe_allow_html=True  # Required to render <br>
)

# Input box
query = st.text_input("Enter your song query")

# Initialize assistant
assistant = MusicAssistant(query)

# Button
if st.button("Search & Play"):
    if not query.strip():
        st.error("Please enter a song query.")
    else:
        with st.spinner("Thinking..."):
            try:
                result = asyncio.run(assistant.search_music_with_ollama())
                st.success("Done")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")