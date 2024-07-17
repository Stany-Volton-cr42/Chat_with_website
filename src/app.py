# import the streamlit

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()

def get_response(user_query):
    return "First, please build me"

# This function takes a URL as input, uses the WebBaseLoader to load the content from the URL,
# and returns the loaded documents.
def get_vectorstore_from_url(url):
    loader = WebBaseLoader(url)
    document = loader.load()

    # Split the document into chunks using the RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    # create a vectorstore from the chunks
    vectorstore = Chroma.from_documents(document_chunks,OpenAIEmbeddings())

    return vectorstore


def get_context_retriever_chains(vectorstore):
    llm = ChatOpenAI()

    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.format_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever,prompt)

    return retriever_chain


def get_conversational_rag_chain(retriever_chain):

    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.format_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}\n"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
        
        ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

# For the interface
st.set_page_config(page_title="Chat-with-website",page_icon="💬")
st.title("Chat with website")

    


# app Sidebar
with st.sidebar:
    st.header("Settings")
    website_URL = st.text_input("Website url")

# Check if the website URL is provided
if website_URL is None or website_URL == "":
    st.info("Please enter a website url")

# Load documents from the provided URL using the WebBaseLoader

else:
    # Session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history =[
            AIMessage(content= "Hello, I am a bot. How can I help you"),
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(website_URL)

    # document_chunks = get_vectorstore_from_url(website_URL)

    # create_document_chunks
    # vector_store = get_vectorstore_from_url(website_URL)

    retriever_chain = get_context_retriever_chains(st.session_state.vector_store)

    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)


    #   CHAT HISTORY / AI response to User Input
    user_query = st.chat_input("Type your message here... ")
    if user_query is not None and user_query != "":
        # response = get_response(user_query)
        response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
        st.write(response)
        # st.session_state.chat_history.append(HumanMessage(content=user_query))
        # st.session_state.chat_history.append(AIMessage(content=response))



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
                