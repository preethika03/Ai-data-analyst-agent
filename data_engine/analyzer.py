
import pandas as pd


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Return basic statistics and data-quality information."""

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },
        "summary_statistics": df.describe(
            include="all"
        ).fillna("").to_dict(),
    }
