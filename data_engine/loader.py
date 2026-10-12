
from pathlib import Path

import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """Load a CSV or Excel file into a Pandas DataFrame."""
    path = Path(file_path)
    extension = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if extension == ".csv":
        return pd.read_csv(path)

    if extension in (".xlsx", ".xls"):
        return pd.read_excel(path)

    raise ValueError(
        "Unsupported file type. Please use CSV, XLSX, or XLS."
    )
