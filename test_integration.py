
import pandas as pd

from data_engine.analyzer import analyze_dataframe
from ai_agent.llm import explain_results

df = pd.DataFrame({
    "Salary": [30000, 45000, 60000, 50000],
    "Experience": [1, 3, 6, 4]
})

results = analyze_dataframe(df)

print("Analysis completed.")
print("Rows:", results["rows"])
print("Numeric insights:", results["numeric_insights"])

try:
    answer = explain_results(
        "Explain the salary statistics in this dataset.",
        results["numeric_insights"]
    )
    print("\nAI Explanation:")
    print(answer)

except Exception as error:
    print("\nGemini explanation is temporarily unavailable.")
    print("Error:", error)
    print("\nThe calculated analysis results are still available.")
