from ai_agent.llm import explain_results

result = explain_results(
    "What is the average salary?",
    {"average_salary": 45000, "total_employees": 100}
)

print(result)