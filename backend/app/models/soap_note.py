from sqlalchemy import Column, ForeignKey, Integer, Text

from app.database.database import Base


class SoapNote(Base):
    __tablename__ = "soap_notes"

    id = Column(Integer, primary_key=True, index=True)

    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id"),
        nullable=False,
        unique=True,
    )

    subjective = Column(Text, nullable=False)
    objective = Column(Text, nullable=False)
    assessment = Column(Text, nullable=False)
    plan = Column(Text, nullable=False)