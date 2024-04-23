from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the required environment variables
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Define the system prompt and dynamic prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an advanced AI assistant. You are always polite, professional, and focused on providing the most accurate, concise, and helpful information possible."),
    ("user", "Question:{question}")
])

# Create a Streamlit app
st.set_page_config(page_title="Langchain Chatbot", page_icon=":robot_face:")

# Add a title and description to the app
st.title("Langchain Chatbot")
st.write("Welcome to the Langchain Chatbot! This chatbot is powered by advanced language models and can assist you with a wide range of tasks.")

# Add a dropdown to select the model type (open source or paid)
model_type = st.selectbox("Select Model Type", ("Open Source", "Paid"))

# Create an instance of the selected model type
if model_type == "Open Source":
    llm = Ollama(model="llama2")
else:
    llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create an output parser and chain
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Add a text input for the user's question
input_text = st.text_input("Enter your question here", key="question_input")

# Add a button to submit the question
if st.button("Submit"):
    # Get the response from the chatbot
    if input_text:
        response = chain.invoke({"question": input_text})
        
        # Display the response in a styled container
        with st.container():
            st.markdown(f"**Assistant:** {response}")
            st.markdown("---")