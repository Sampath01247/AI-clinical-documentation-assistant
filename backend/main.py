from fastapi import FastAPI
from app.database.init_db import create_tables
from app.routers import auth, soap_notes, transcripts, users
from app.services.openai_service import test_openai_connection
from app.services.soap_service import generate_soap_from_transcript

app = FastAPI(
    title="AI Clinical Documentation Assistant",
    version="1.0.0"
)

create_tables()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transcripts.router)
app.include_router(soap_notes.router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test-openai")
def test_openai():
    try:
        result = test_openai_connection()

        return {
            "status": "success",
            "response": result
        }

    except Exception as error:
        return {
            "status": "error",
            "detail": str(error)
        }
    
@app.get("/test-soap")
def test_soap():
    sample_transcript = """
    Doctor: What brings you in today?

    Patient: I have had a sore throat and fever for three days.

    Doctor: Do you have difficulty breathing?

    Patient: No, but I have a mild cough and feel tired.

    Doctor: Your temperature is 101 degrees Fahrenheit.
    Please drink fluids, rest, and take acetaminophen as needed.
    Return if your symptoms worsen.
    """

    try:
        soap_note = generate_soap_from_transcript(sample_transcript)

        return {
            "status": "success",
            "soap_note": soap_note,
        }

    except Exception as error:
        return {
            "status": "error",
            "detail": str(error),
        }