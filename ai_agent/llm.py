
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from ai_agent.prompts import SYSTEM_PROMPT

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file")

client = genai.Client(api_key=api_key)


def explain_results(question, analysis_results, dataset_data=None):
    """
    Generate an explanation using the analysis results
    and, when provided, the original dataset information.
    """

    prompt = f"""
User question:
{question}

Analysis results:
{json.dumps(analysis_results, indent=2, default=str)}

Original dataset rows:
{json.dumps(dataset_data, indent=2, default=str)
 if dataset_data is not None else "Not provided"}

Instructions:
1. Explain the findings in simple English.
2. Use the original dataset rows to identify specific products
   and their values when those rows are provided.
3. Calculate totals from the original rows when available.
4. Do not invent statistics or product information.
5. If information is missing, clearly say it is unavailable.
6. Describe correlations carefully, especially for small datasets.
7. Keep the explanation clear and concise.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
    )

    if not response.text:
        raise ValueError("Gemini returned an empty explanation.")

    return response.text
