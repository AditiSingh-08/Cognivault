import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def load_llm():

    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing from .env")

    if not model_name:
        raise ValueError("GEMINI_MODEL is missing from .env")

    llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=api_key,
    streaming=False
)


    return llm



def generate_answer(llm, question, context):

    prompt = f"""
    You are Cognivault, an intelligent document assistant.

    Answer the question using ONLY the context provided below.

    If the answer is not available in the context,
    say that the document does not contain enough information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)

    return response.content