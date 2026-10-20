import sys
from pathlib import Path
from uuid import uuid4
from io import BytesIO
from typing import Optional, List

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

from .database import SessionLocal
from .models import Dataset
from backend.data_engine.analyzer import analyze_dataframe
from ai_agent.llm import explain_results


app = FastAPI(title="AI Data Analyst Agent")

# Store uploaded datasets in memory while the server runs
uploaded_datasets = {}


# Home endpoint
@app.get("/")
def home():
    return {"message": "AI Data Analyst Agent is running!"}


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}


# Upload CSV and save metadata to PostgreSQL
@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The file is empty."
            )

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File must be under 10 MB."
            )

        df = pd.read_csv(BytesIO(content))
        dataset_id = str(uuid4())

        # Save dataset metadata to PostgreSQL
        db = SessionLocal()
        try:
            dataset = Dataset(
                filename=file.filename,
                row_count=len(df),
                column_count=len(df.columns)
            )
            db.add(dataset)
            db.commit()

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Could not save dataset information to the database."
            )

        finally:
            db.close()

        # Store the dataframe for other endpoints
        uploaded_datasets[dataset_id] = df.copy()

        return {
            "dataset_id": dataset_id,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "missing_values": {
                col: int(count)
                for col, count in df.isnull().sum().items()
            },
            "preview": df.head(5).fillna("").to_dict(orient="records"),
            "numeric_statistics": df.describe().round(2).to_dict()
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the CSV file. Check its format."
        )

    finally:
        await file.close()


# Request model for asking questions
class QuestionRequest(BaseModel):
    question: str
    dataset_id: str


# Ask questions about the uploaded dataset
@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.lower().strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    if request.dataset_id not in uploaded_datasets:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Please upload the CSV again."
        )

    df = uploaded_datasets[request.dataset_id].copy()

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded dataset is empty."
        )

    # Find the highest-priced product
    if "highest" in question or "maximum" in question:
        if "Price" in df.columns:
            prices = pd.to_numeric(df["Price"], errors="coerce")
            valid_prices = prices.dropna()

            if valid_prices.empty:
                answer = "No valid price values were found."
            else:
                index = valid_prices.idxmax()
                answer = (
                    f"The product with the highest price is "
                    f"{df.loc[index].get('Product', 'Unknown')} "
                    f"with price {valid_prices.loc[index]}."
                )
        else:
            answer = "The dataset does not contain a Price column."

    # Calculate total quantity
    elif (
        "total quantity" in question
        or "sum of quantity" in question
    ):
        if "Quantity" in df.columns:
            quantity = pd.to_numeric(
                df["Quantity"], errors="coerce"
            )
            answer = f"The total quantity is {quantity.sum()}."
        else:
            answer = "The dataset does not contain a Quantity column."

    # Calculate average price
    elif "average price" in question or "mean price" in question:
        if "Price" in df.columns:
            prices = pd.to_numeric(
                df["Price"], errors="coerce"
            ).dropna()

            if prices.empty:
                answer = "No valid price values were found."
            else:
                answer = f"The average price is {prices.mean():.2f}."
        else:
            answer = "The dataset does not contain a Price column."

    # Calculate minimum price
    elif (
        "minimum price" in question
        or "lowest price" in question
        or "lowest" in question
    ):
        if "Price" in df.columns:
            prices = pd.to_numeric(
                df["Price"], errors="coerce"
            ).dropna()

            if prices.empty:
                answer = "No valid price values were found."
            else:
                answer = f"The minimum price is {prices.min():.2f}."
        else:
            answer = "The dataset does not contain a Price column."

    # Count total rows
    elif "number of rows" in question or "how many rows" in question:
        answer = f"The dataset contains {len(df)} rows."

    else:
        answer = (
            "I cannot answer that question yet. Try asking "
            "about the highest price, total quantity, "
            "average price, minimum price, or number of rows."
        )

    return {
        "question": request.question,
        "answer": answer
    }


# Analyze a dataset
@app.get("/analyze/{dataset_id}")
def analyze_dataset(dataset_id: str):
    if dataset_id not in uploaded_datasets:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Please upload the CSV again."
        )

    df = uploaded_datasets[dataset_id].copy()

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded dataset is empty."
        )

    try:
        analysis_results = analyze_dataframe(df)

        return {
            "dataset_id": dataset_id,
            **analysis_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


# Get a detailed numerical summary
@app.get("/summary/{dataset_id}")
def get_dataset_summary(dataset_id: str):
    if dataset_id not in uploaded_datasets:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Please upload the CSV again."
        )

    df = uploaded_datasets[dataset_id].copy()
    numeric_summary = {}

    for column in df.select_dtypes(include="number").columns:
        numeric_summary[column] = {
            "sum": float(df[column].sum()),
            "average": round(float(df[column].mean()), 2),
            "minimum": float(df[column].min()),
            "maximum": float(df[column].max())
        }

    return {
        "dataset_id": dataset_id,
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_summary": numeric_summary
    }


# Request model for data operations
class DataOperationRequest(BaseModel):
    dataset_id: str
    operation: str
    column: Optional[str] = None
    value: Optional[float] = None
    sort_order: str = "ascending"
    columns: Optional[List[str]] = None


# Filter, sort, or select columns
@app.post("/data-operations")
def data_operations(request: DataOperationRequest):
    if request.dataset_id not in uploaded_datasets:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Please upload the CSV again."
        )

    df = uploaded_datasets[request.dataset_id].copy()
    operation = request.operation.lower().strip()

    # FILTER
    if operation == "filter":
        if not request.column or request.column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Please provide a valid column name."
            )

        if request.value is None:
            raise HTTPException(
                status_code=400,
                detail="Please provide a numeric filter value."
            )

        # Keep rows where the numeric column is greater than the value
        numeric_values = pd.to_numeric(
            df[request.column], errors="coerce"
        )
        result = df[numeric_values > request.value]

    # SORT
    elif operation == "sort":
        if not request.column or request.column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Please provide a valid column name."
            )

        if request.sort_order not in ["ascending", "descending"]:
            raise HTTPException(
                status_code=400,
                detail="sort_order must be ascending or descending."
            )

        result = df.sort_values(
            by=request.column,
            ascending=(request.sort_order == "ascending"),
            na_position="last"
        )

    # SELECT COLUMNS
    elif operation == "select_columns":
        if not request.columns:
            raise HTTPException(
                status_code=400,
                detail="Please provide the columns to select."
            )

        invalid_columns = [
            col for col in request.columns
            if col not in df.columns
        ]

        if invalid_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown columns: {invalid_columns}"
            )

        result = df[request.columns]

    else:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported operation. Use filter, sort, "
                "or select_columns."
            )
        )

    return {
        "operation": operation,
        "total_rows": int(len(result)),
        "columns": list(result.columns),
        "results": result.fillna("").to_dict(orient="records")
    }


# Request model for AI insights
class InsightsRequest(BaseModel):
    question: str = "Explain the key findings in this dataset."


# Generate AI insights using the analyzer and LLM
@app.post("/insights/{dataset_id}")
def get_ai_insights(dataset_id: str, request: InsightsRequest):
    if dataset_id not in uploaded_datasets:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Please upload the CSV again."
        )

    df = uploaded_datasets[dataset_id].copy()

    try:
        # Get analysis results from the analyzer
        analysis_results = analyze_dataframe(df)

        # Send analysis results and original rows to the LLM
        explanation = explain_results(
            request.question,
            analysis_results,
            df.fillna("").to_dict(orient="records")
        )

        return {
            "dataset_id": dataset_id,
            "analysis_results": analysis_results,
            "ai_explanation": explanation
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI insights failed: {str(e)}"
        )