
import pandas as pd
from data_engine import analyze_dataframe

df = pd.DataFrame({
    "Name": ["Anu", "Bala", "Charan"],
    "Marks": [85, 90, 78],
})

result = analyze_dataframe(df)

print("Rows:", result["rows"])
print("Columns:", result["columns"])
print("Missing values:", result["missing_values"])
print("Analysis successful!")
