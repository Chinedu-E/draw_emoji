import pyperclip
import streamlit as st

from src.emoji_text import get_emoji_text



st.title("Emoji Writer")


# Input box for the text
text_input = st.text_input("Enter your text:", "")

# Select an emoji 
emoji_selection = st.text_input("Enter an emoji:", "")

# Submit button
if st.button("Submit"):
    if text_input:
        # Convert text to emoji form
        emoji_text_output = get_emoji_text(text_input.upper(), emoji_selection)
        text = '\n\n'.join(emoji_text_output)
        cols = st.columns(2)
        with cols[0]:
            st.write("Here's your emoji text:")
        with cols[1]:
            if st.button("Copy"):
                pyperclip.copy(text)
        st.text(text)
    else:
        st.write("Please enter some text.")
        