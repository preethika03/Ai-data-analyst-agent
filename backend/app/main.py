from fastapi import FastAPI

app = FastAPI(title="AI Data Analyst Agent")


@app.get("/")
def home():
    return {"message": "AI Data Analyst Agent Backend is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}