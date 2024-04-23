from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes
import uvicorn 
import os
from dotenv import load_dotenv

# Here we load the environment variables from the .env file
load_dotenv()

# Here we set the OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Here we define the FastAPI app that will serve the models
app = FastAPI( title="Langchain Server" , version = "0.1.0", description = "simple Langchain Server")

# Here we define the models that we will use in the app
paid_model = ChatOpenAI()
free_model = Ollama(model="llama2")

# Here we add the routes to the app
add_routes(app, paid_model, path = "/openai")

# Here we define the prompt templates that will be used to generate the prompts
prompt1 = ChatPromptTemplate.from_template(" Explain First principles of {concept} in 100 words")
prompt2 = ChatPromptTemplate.from_template(" write a poem related to {concept} in 100 words")

# Here we add the routes to the app
add_routes(app, prompt1|paid_model, path = "/essay")
add_routes(app, prompt2|free_model, path = "/poem")

# Here we define the main function that will run the app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)