from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.transcript import Transcript
from app.models.user import User
from app.schemas.transcript import TranscriptCreate, TranscriptResponse
from app.core.security import get_current_user

router = APIRouter(
    prefix="/transcripts",
    tags=["Transcripts"]
)

@router.post("/", response_model=TranscriptResponse)
def create_transcript(
    transcript: TranscriptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_transcript = Transcript(
        patient_name=transcript.patient_name,
        transcript_text=transcript.transcript_text,
        doctor_id=current_user.id
    )

    db.add(new_transcript)
    db.commit()
    db.refresh(new_transcript)

    return new_transcript