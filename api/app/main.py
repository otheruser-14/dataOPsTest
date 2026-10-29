from fastapi import FastAPI

app = FastAPI(
    title="DataOps Air Quality API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "DataOps API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
