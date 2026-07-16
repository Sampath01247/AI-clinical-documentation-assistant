from app.database.database import Base, engine
from app.models.soap_note import SoapNote
from app.models.transcript import Transcript
from app.models.user import User


def create_tables():
    Base.metadata.create_all(bind=engine)