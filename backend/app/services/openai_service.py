import os

from dotenv import load_dotenv
from openai import OpenAI

# Load values from backend/.env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found. Add it to the backend/.env file."
    )

# Create one reusable OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def test_openai_connection() -> str:
    """
    Send a basic request to OpenAI and return the generated text.
    This function is used only to verify the API integration.
    """

    response = client.responses.create(
        model=OPENAI_MODEL,
        input="Reply with exactly: OpenAI connection successful."
    )

    return response.output_text