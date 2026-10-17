
import pandas as pd


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Generate a profile and summary of a dataset."""

    numeric_insights = {}
    outliers = {}

    # Calculate statistics for numeric columns
    numeric_df = df.select_dtypes(include="number")

    for column in numeric_df.columns:
        numeric_insights[column] = {
            key: float(value)
            for key, value in df[column].describe().items()
        }

    # Count missing values
    missing_values = {
        column: int(count)
        for column, count in df.isnull().sum().items()
    }

    # Calculate missing-value percentages
    total_rows = len(df)

    if total_rows > 0:
        missing_percentage = {
            column: round((count / total_rows) * 100, 2)
            for column, count in missing_values.items()
        }
    else:
        missing_percentage = {
            column: 0.0 for column in df.columns
        }

    # Calculate correlations between numeric columns
    correlations = numeric_df.corr().fillna(0).to_dict()

    # Detect outliers using the IQR method
    for column in numeric_df.columns:
        values = numeric_df[column].dropna()

        if values.empty:
            outliers[column] = []
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        unusual_values = values[
            (values < lower_bound) | (values > upper_bound)
        ]

        outliers[column] = [
            float(value) for value in unusual_values.tolist()
        ]

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),

               "data_types": {
            col: (
                "str" if dtype == object
                else str(dtype)
            )
            for col, dtype in df.dtypes.items()
        },
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_insights": numeric_insights,
        "correlations": correlations,
        "outliers": outliers,

        "summary_statistics": (
            df.describe(include="all")
            .fillna("")
            .to_dict()
        ),
    }
