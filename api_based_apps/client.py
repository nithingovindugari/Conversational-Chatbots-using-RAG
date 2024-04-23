import requests
import streamlit as st

# Here we define a function that will make a request to the API ( /openai endpoint) and return the response
def get_paid_response(input_text):
    response = requests.post("http://localhost:8000/essay/invoke", json={"input": { "concept": input_text}})
    return response.json()['output']["content"]

# Here we define a function that will make a request to the Ollama/llama2 and return the response
def get_free_response(input_text):
    response = requests.post("http://localhost:8000/poem/invoke", json={"input": { "concept": input_text}})
    return response.json()['output']


# Here we define the Streamlit app that will allow us to interact with the API
st.title("Langchain  API Interaction")
input_text1 = st.text_input("Write an explanation in first principles on ")
input_text2 = st.text_input("Write a poem on ")

# If the user has entered some text in the first box , we will call the get_response function and display the response
if input_text1:
    response1 = get_paid_response(input_text1)
    st.write(response1)

# If the user has entered some text in the second box , we will call the get_response function and display the response
if input_text2:
    response2 = get_free_response(input_text2)
    st.write(response2)