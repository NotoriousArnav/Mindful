from langchain_groq import ChatGroq
from langchain_ollama.llms import OllamaLLM
import os

from dotenv import load_dotenv
load_dotenv()


groq_llm = ChatGroq(
        model="llama-3.2-90b-vision-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

ollama_llm = OllamaLLM(
        model="llama-3.2-8b"
    )


llm = groq_llm
