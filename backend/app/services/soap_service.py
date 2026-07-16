import json

from app.services.openai_service import client, OPENAI_MODEL


def generate_soap_from_transcript(transcript_text: str) -> dict:
    if not transcript_text.strip():
        raise ValueError("Transcript cannot be empty.")

    instructions = """
You are a clinical documentation assistant.

Convert the doctor-patient consultation transcript into a structured SOAP note.

Return valid JSON only in this exact format:

{
  "subjective": "Information reported by the patient",
  "objective": "Observed or measurable clinical information",
  "assessment": "Possible clinical assessment based only on the transcript",
  "plan": "Treatment, testing, follow-up, or next steps mentioned"
}

Rules:
- Use only information contained in the transcript.
- Do not invent symptoms, vital signs, examination findings, medications, or diagnoses.
- If objective information is unavailable, clearly state that.
- The output is a documentation suggestion and requires physician review.
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=instructions,
        input=transcript_text,
    )

    output_text = response.output_text.strip()

    # Remove Markdown code fences if the model includes them
    if output_text.startswith("```json"):
        output_text = output_text.removeprefix("```json")
        output_text = output_text.removesuffix("```").strip()
    elif output_text.startswith("```"):
        output_text = output_text.removeprefix("```")
        output_text = output_text.removesuffix("```").strip()

    try:
        soap_data = json.loads(output_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"OpenAI returned an invalid JSON response: {output_text}"
        ) from error

    required_fields = {
        "subjective",
        "objective",
        "assessment",
        "plan",
    }

    missing_fields = required_fields - soap_data.keys()

    if missing_fields:
        raise ValueError(
            f"SOAP response is missing fields: {', '.join(missing_fields)}"
        )

    return soap_data