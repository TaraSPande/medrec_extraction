from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Call OpenAI API gpt-4o-mini
def extract_information(note: str) -> str:
    prompt = f"""
    Extract the following fields from the clinical note and return JSON:
    1. Patient Name
    2. Age
    3. Diagnoses (nouns)
    4. Medications
    5. Procedures (nouns)

    Important Extraction Reminders: 
    - Only include the medications and procedures that the patient uses
    - Only include correct patient diagnoses

    Clinical Note:
    {note}

    JSON Output:
    """

    response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a medical data extraction assistant."},
                {"role": "user", "content": prompt}],
        temperature=0)

    return response.choices[0].message.content