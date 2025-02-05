from flask import Flask, request, jsonify, render_template
import json
import re
from extract import extract_information
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

app = Flask(__name__, template_folder="templates")

#Launch basic front end
@app.route("/")
def index():
    return render_template("index.html")

#Upon press "Extract", return formatted JSON to front end
@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input. Expecting plain text in request body."}), 400
    note = data["text"]

    #Clean OpenAI Output
    extracted_text = extract_information(note)
    cleaned_text = re.sub(r"```json\n|\n```", "", extracted_text)
    data = json.loads(cleaned_text)
    formatted_json = json.dumps(data, indent=4)

    #Write to a .json file
    with open("result_test.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    return formatted_json

if __name__ == "__main__":
    app.run(debug=True)



