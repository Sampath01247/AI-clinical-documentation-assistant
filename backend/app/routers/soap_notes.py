from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.soap_note import SoapNote
from app.models.transcript import Transcript
from app.models.user import User
from app.schemas.soap_note import SoapNoteResponse
from app.services.soap_service import generate_soap_from_transcript


router = APIRouter(
    prefix="/soap-notes",
    tags=["SOAP Notes"],
)


@router.post(
    "/generate/{transcript_id}",
    response_model=SoapNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_soap_note(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Find the transcript and ensure it belongs to the logged-in doctor
    transcript = (
        db.query(Transcript)
        .filter(
            Transcript.id == transcript_id,
            Transcript.doctor_id == current_user.id,
        )
        .first()
    )

    if transcript is None:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found.",
        )

    # Prevent duplicate SOAP notes
    existing_note = (
        db.query(SoapNote)
        .filter(SoapNote.transcript_id == transcript_id)
        .first()
    )

    if existing_note:
        raise HTTPException(
            status_code=409,
            detail="A SOAP note already exists for this transcript.",
        )

    try:
        soap_data = generate_soap_from_transcript(
            transcript.transcript_text
        )
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"SOAP note generation failed: {str(error)}",
        ) from error

    soap_note = SoapNote(
        transcript_id=transcript.id,
        subjective=soap_data["subjective"],
        objective=soap_data["objective"],
        assessment=soap_data["assessment"],
        plan=soap_data["plan"],
    )

    db.add(soap_note)
    db.commit()
    db.refresh(soap_note)

    return soap_note