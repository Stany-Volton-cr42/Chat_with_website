# import the streamlit

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader

def get_response(user_query):
    return "First, please build me"

# This function takes a URL as input, uses the WebBaseLoader to load the content from the URL,
# and returns the loaded documents.
def get_vectorstore_from_url(url):
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents


# For the interface
st.set_page_config(page_title="Chat-with-website",page_icon="💬")
st.title("Chat with website")
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[
    AIMessage(content= "Hello, I am a bot. How can I help you")

]
    


# app Sidebar
with st.sidebar:
    st.header("Settings")
    website_URL = st.text_input("Website url")

# Check if the website URL is provided
if website_URL is None or website_URL == "":
    st.info("Please enter a website url")

# Load documents from the provided URL using the WebBaseLoader

else:
    documents = get_vectorstore_from_url(website_URL)
    with st.sidebar:
        st.write(documents)

    #   CHAT HISTORY / AI response to User Input
    user_query = st.chat_input("Type your message here... ")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # with st.sidebar:
    #     st.write(st.session_state.chat_history)

    # conversation

    # Iterate through the chat history stored in the session state
    for message in st.session_state.chat_history:
        # Check if the message is an instance of AIMessage
        if isinstance(message, AIMessage):
            # Display the AI message in the chat interface
            with st.chat_message("AI"):
                st.write(message.content)
        # Check if the message is an instance of HumanMessage
        elif isinstance(message, HumanMessage):
            # Display the Human message in the chat interface
            with st.chat_message("Human"):
                st.write(message.content)

