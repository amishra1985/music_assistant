import streamlit as st
from music_assistant import MusicAssistant  # import your class


st.set_page_config(page_title="Music Assistant", page_icon="🎧")

st.title("🎧 Music Assistant")
st.write("Type a song name, movie name, or anything you remember about the track.")

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
                result = assistant.search_music_with_ollama()
                st.success("Done")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")