from pydantic import BaseModel, ConfigDict


class SoapNoteResponse(BaseModel):
    id: int
    transcript_id: int
    subjective: str
    objective: str
    assessment: str
    plan: str

    model_config = ConfigDict(from_attributes=True)