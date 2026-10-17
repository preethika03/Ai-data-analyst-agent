
import pandas as pd
from ai_agent.workflow import run_agent

df = pd.DataFrame({
    "name": ["A", "B", "C"],
    "salary": [30000, 45000, 60000]
})

result = run_agent("Summarize this dataset", df)
print(result)
