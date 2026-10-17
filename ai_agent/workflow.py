


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
        # Analyze the dataset
        results = analyze_dataframe(df)

        # Include actual dataset records so the AI can identify
        # specific products and values, not only summary statistics.
        results["dataset_records"] = (
            df.head(100).fillna("").to_dict(orient="records")
        )
        results["records_note"] = (
            "These are the first 100 rows of the dataset. "
            "Use them to identify specific records when relevant. "
            "Do not assume they represent every row if the dataset is larger."
        )

        # Ask Gemini to explain the analysis
        explanation = explain_results(question.strip(), results)

        return {
            "success": True,
            "question": question.strip(),
            "analysis_results": results,
            "explanation": explanation
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Analysis failed: {error}"
        }
