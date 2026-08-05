from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, context: str, history: str = ""):
    history_block = f"\nRecent conversation (for resolving follow-up questions):\n{history}\n" if history else ""

    prompt = f"""
You are a helpful assistant.

Answer the question ONLY using the provided context below. If the recent
conversation is relevant to understanding what the user means (for example,
a follow-up question like "what about the second one?"), use it to
interpret the question - but still answer only using facts from the context.

Context:{context}

Question:{question}
"""
    response = client.responses.create(
        model = "gpt-4.1-mini",
        input = prompt
    )

    return response.output_text