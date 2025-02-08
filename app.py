from flask import Flask, request, jsonify, render_template
import json
import re
import fitz  # PyMuPDF for PDF text extraction
from extract import extract_information
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

app = Flask(__name__, template_folder="templates")

# Launch basic front end
@app.route("/")
def index():
    return render_template("index.html")

# Upon pressing "Extract", return formatted JSON to front end
@app.route("/extract", methods=["POST"])
def extract():
    if "file" in request.files:
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            note = "\n".join([page.get_text() for page in doc])
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    else:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Invalid input. Expecting plain text in request body."}), 400
        note = data["text"]
        print("NOTE", note)
    
    # Clean OpenAI Output
    extracted_text = extract_information(note)
    print(extracted_text)
    cleaned_text = re.sub(r"```json\n|\n```", "", extracted_text)
    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse extracted data."}), 500
    
    formatted_json = json.dumps(data, indent=4)

    # Write to a .json file
    # with open("result_test.json", "w") as json_file:
    #     json.dump(data, json_file, indent=4)
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
