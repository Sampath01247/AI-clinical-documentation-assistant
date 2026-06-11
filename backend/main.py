from fastapi import FastAPI

app = FastAPI(
    title="AI Clinical Documentation Assistant",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}