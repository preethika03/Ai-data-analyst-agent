import pandas as pd
def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Generate a basic profile and summary of a dataset."""
    numeric_insights = {}
    for column in df.select_dtypes(include="number").columns:
        numeric_insights[column] = {
            key: float(value)
            for key, value in df[column].describe().items()
        }
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum()),

        "numeric_insights": numeric_insights,

        "summary_statistics": (
            df.describe(include="all")
            .fillna("")
            .to_dict()
        ),
    }
