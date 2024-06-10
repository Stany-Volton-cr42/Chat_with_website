# import the streamlit

import streamlit as st
st.set_page_config(page_title="Chat-with-website",page_icon="💬")

# For the interface
st.title("Chat with website")
with st.sidebar:
    st.header("Settings")
    website_URL = st.text_input("Website url")

st.chat_input("Type your message here... ")

with st.chat_message("AI"):
    st.write("Hello! how can I help you ")

with st.chat_message("Human"):
    st.write("I want to know about the website")


