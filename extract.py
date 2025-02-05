from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_information(note):
    #print("HERE", note)
    prompt = f"""
    Extract the following fields from the clinical note and return JSON:
    - Patient Name
    - Age
    - Diagnoses
    - Medications
    - Procedures

    Clinical Note:
    {note}

    JSON Output:
    """

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role": "system", "content": "You are a medical data extraction assistant."},
              {"role": "user", "content": prompt}],
    temperature=0)

    return response.choices[0].message.content


# def extract_information(note):
#     #print("HERE", note)
#     prompt = f"""
#     Extract the following fields from the clinical note and return JSON:
#     - Patient Name
#     - Age
#     - Diagnoses
#     - Medications
#     - Procedures

#     Clinical Note:
#     {note}

#     JSON output:
#     """

#     response = client.chat.completions.create(model="gpt-4o-mini",
#     messages=[{"role": "system", "content": "You are a medical data extraction assistant."},
#               {"role": "user", "content": prompt}],
#     temperature=0)

#     return response.choices[0].message.content

