from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

app = FastAPI(title="AI Data Analyst Agent")
uploaded_datasets = {}


@app.get("/")
def home():
    return {"message": "AI Data Analyst Agent is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    try:
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="The file is empty.")

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File must be under 10 MB.")

        df = pd.read_csv(BytesIO(content))
        dataset_id = str(uuid4())
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

from pydantic import BaseModel



class QuestionRequest(BaseModel):
    question: str
    dataset_id: str




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
    elif "total quantity" in question or "sum of quantity" in question:
        if "Quantity" in df.columns:
            quantity = pd.to_numeric(df["Quantity"], errors="coerce")
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

