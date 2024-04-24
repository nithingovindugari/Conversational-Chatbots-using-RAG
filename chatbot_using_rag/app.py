import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import create_retrieval_chain
import pickle
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetching the API key from the environment variable
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Loading the document using the PyPDFLoader
loader = PyPDFLoader('1706.03762.pdf')
docs = loader.load()

# Splitting the document into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = splitter.split_documents(docs)

# Chroma Vector Embedding or FAISS Vector Embedding
chroma_flag = False

# Load or create the database
File = "Transformer"
if os.path.exists(File):
    database = FAISS.load_local(File, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
else:
    if chroma_flag:
        database = Chroma.from_documents(documents, OpenAIEmbeddings())
    else:
        database = FAISS.from_documents(documents, OpenAIEmbeddings())
    database.save_local(folder_path=File)

# Choose the LLM model
open_source = False
if open_source:
    llm = Ollama(model="llama2")
else:
    llm = ChatOpenAI(model="gpt-3.5-turbo")

# Prompt for the chatbot
prompt = ChatPromptTemplate.from_template("""
    You are an First principles AI assistant and  help users answer their questions in first principles
    and with analogy if needed. I will tip you $1000 if the user is satisfied and dont forget to answer briefly and clearly.
    <context>{context}</context>
    Question: {input}
""")


# Creating the document chain
document_chain = create_stuff_documents_chain(llm, prompt)

# Create the retriever
retriever = database.as_retriever()

# Create the retrieval chain
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Streamlit UI
st.title("First Principle Chatbot")


# Initializing the chat history if not already present
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there, how can I help you"}
    ]

# Displaying the chat history
if "messages" in st.session_state.keys():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Getting user input
user_prompt = st.chat_input()
if user_prompt is not None:
    # Appending the user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    # Triggering the AI response if the last message is from the user
    if st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                # Retrieving the full chat history to maintain context
                chat_history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
                # Invoking the AI with the full chat history
                ai_response = retrieval_chain.invoke({"input": user_prompt, "chat_history": chat_history})["answer"]
                st.write(ai_response)
                # Appending the AI's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

