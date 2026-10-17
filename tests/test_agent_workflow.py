
import pandas as pd
from ai_agent.workflow import run_agent


def sample_dataframe():
    return pd.DataFrame({
        "Product": ["Laptop", "Tablet", "USB Cable"],
        "Price": [75000, 28000, 250],
        "Quantity": [5, 6, 50],
        "Rating": [4.7, 4.8, 4.0],
    })


def test_empty_question():
    result = run_agent("", sample_dataframe())
    assert result["success"] is False
    assert result["error"] == "Please enter a question."


def test_empty_dataset():
    result = run_agent("Summarize this dataset", pd.DataFrame())
    assert result["success"] is False
    assert result["error"] == "Please provide a non-empty dataset."


def test_successful_analysis(monkeypatch):
    def fake_explanation(question, results):
        return "Laptop is the highest-priced product."

    monkeypatch.setattr(
        "ai_agent.workflow.explain_results",
        fake_explanation,
    )

    result = run_agent(
        "Which product has the highest price?",
        sample_dataframe(),
    )

    assert result["success"] is True
    assert result["question"] == "Which product has the highest price?"
    assert result["explanation"] == "Laptop is the highest-priced product."
    assert "dataset_records" in result["analysis_results"]
