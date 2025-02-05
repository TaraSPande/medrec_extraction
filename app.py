from flask import Flask, request, jsonify
#import os
import json
from extract import extract_information
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    
    if not data or "note" not in data:
        return jsonify({"error": "Invalid input. Expecting JSON with 'note' field."}), 400

    note = data["note"]
    extracted_text = extract_information(note)
    print("RESPONSE", extracted_text)
    data = json.loads(extracted_text)
    print(type(data))
    
    with open("result_test.json", "w") as json_file:
        #print("HERE")
        json.dump(data, json_file, indent=4)
    
    return extracted_text

# @app.route("/extract", methods=["POST"])
# def extract():
#     data = request.get_json()
    
#     if not data or "note" not in data:
#         return jsonify({"error": "Invalid input. Expecting JSON with 'note' field."}), 400

#     note = data["note"]
#     extracted_text = extract_information(note)
    
#     with open("result_test.json", "w") as json_file:
#         print("HERE")
#         json.dump(extracted_text, json_file, indent=4)
    
#     return jsonify(extracted_text)

if __name__ == "__main__":
    app.run(debug=True)



