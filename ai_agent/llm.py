
import os
from dotenv import load_dotenv
from google import genai
from ai_agent.prompts import SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file")

client = genai.Client(api_key=api_key)


def explain_results(question, analysis_results):
    prompt = f"""
    User question: {question}

    Actual analysis results:
    {analysis_results}

    Explain these results in simple English.
    Do not invent statistics.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
    )

    return response.text
