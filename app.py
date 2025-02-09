from flask import Flask, request, jsonify, render_template, Response
import json
import re
import fitz  # PyMuPDF for PDF text extraction
from extract import extract_information
from dotenv import load_dotenv
import logging

# Load API key from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file
    filemode='w'          # Overwrite the log file each time; use 'a' for append mode
    )
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates")

# Launch front end
@app.route("/")
def index() -> str:
    logger.info("Rendering the front-end index page.")
    return render_template("index.html")

# Upon pressing "Extract", return formatted JSON to front end
@app.route("/extract", methods=["POST"])
def extract() -> Response:
    logger.info("Received request to extract information.")
    
    # IF PDF
    if "file" in request.files:
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            logger.info(f"Extracting text from PDF file: {file.filename}")
            doc = fitz.open(stream=file.read(), filetype="pdf")
            note = "\n".join([page.get_text() for page in doc])
        else:
            logger.error(f"Unsupported file format: {file.filename}")
            return jsonify({"error": "Unsupported file format"}), 400
    # IF RAW TEXT
    else:
        data = request.get_json()
        if not data or "text" not in data:
            logger.error("Invalid input: No 'text' field in request body.")
            return jsonify({"error": "Invalid input. Expecting plain text in request body."}), 400
        note = data["text"]
    
    # Extract & Clean OpenAI Output
    logger.debug("Starting extraction process.")
    extracted_text = extract_information(note)
    cleaned_text = re.sub(r"```json\n|\n```", "", extracted_text)
    
    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        logger.error("Failed to parse extracted data.")
        return jsonify({"error": "Failed to parse extracted data."}), 500
    
    logger.info("Extraction completed successfully.")
    return jsonify(data)

if __name__ == "__main__":
    logger.info("Starting Flask app.")
    app.run(debug=True)