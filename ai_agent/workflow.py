

import pandas as pd
from data_engine.analyzer import analyze_dataframe
from ai_agent.llm import explain_results


def run_agent(question: str, df: pd.DataFrame) -> dict:
    if not question or not question.strip():
        return {
            "success": False,
            "error": "Please enter a question."
        }

    if df is None or df.empty:
        return {
            "success": False,
            "error": "Please provide a non-empty dataset."
        }

    try:
        # Step 1: Analyze the dataset
        analysis_results = analyze_dataframe(df)

        # Step 2: Ask Gemini to explain the results
        explanation = explain_results(question, analysis_results)

        # Step 3: Return both results and explanation
        return {
            "success": True,
            "question": question,
            "analysis_results": analysis_results,
            "explanation": explanation
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Analysis failed: {error}"
        }
