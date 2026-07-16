from pydantic import BaseModel

class TranscriptCreate(BaseModel):
    patient_name: str
    transcript_text: str

class TranscriptResponse(BaseModel):
    id: int
    patient_name: str
    transcript_text: str
    doctor_id: int

    class Config:
        from_attributes = True