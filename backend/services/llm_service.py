from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, context: str):
    prompt = f"""
    
You are a helpful assistant.

Answer the question ONLY using the provided context below.

Context:{context}

Question:{question}
"""
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = prompt
    )

    return response.output_text