import pandas as pd


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Generate a basic profile and summary of a dataset."""

    numeric_insights = {}

    # Calculate statistics for numeric columns
    for column in df.select_dtypes(include="number").columns:
        numeric_insights[column] = {
            key: float(value)
            for key, value in df[column].describe().items()
        }

    # Count missing values in each column
    missing_values = {
        column: int(count)
        for column, count in df.isnull().sum().items()
    }

    # Calculate percentage of missing values in each column
    total_rows = len(df)

    if total_rows > 0:
        missing_percentage = {
            column: round((count / total_rows) * 100, 2)
            for column, count in missing_values.items()
        }
    else:
        missing_percentage = {
            column: 0.0
            for column in df.columns
        }

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),

        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "missing_values": missing_values,

        "missing_percentage": missing_percentage,

        "duplicate_rows": int(df.duplicated().sum()),

        "numeric_insights": numeric_insights,

        "summary_statistics": (
            df.describe(include="all")
            .fillna("")
            .to_dict()
        ),
    }