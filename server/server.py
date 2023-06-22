from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from extract_text import extract_text_from_pdf, extract_text_from_docx
from resume_processor import process_resume
from keyword_matching import keyword_match
import pymongo
import pandas as pd

app = Flask(__name__)
CORS(app)

# Configure the upload folder
DEF_UPLOAD = "uploads/"
app.config["UPLOAD_FOLDER"] = DEF_UPLOAD

# Connect to MongoDB
client = pymongo.MongoClient("mongodb-service")
db = client["jobs_database"]
collection = db["jobs_collection"]

pd.options.display.max_columns = None
pd.options.display.max_rows = None


# File upload endpoint
@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    resume = request.files["resume"]

    if resume.filename == "":
        return jsonify({"error": "Invalid file name."}), 400
    elif resume.filename.rsplit(".", 1)[1].lower() not in ["pdf", "docx"]:
        return (
            jsonify(
                {"error": "Invalid file type. Only PDF and DOCX files are allowed."}
            ),
            400,
        )

    # Save the uploaded file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
    resume.save(file_path)

    # Determine file extension
    file_extension = resume.filename.rsplit(".", 1)[1].lower()

    # Perform text extraction from the resume
    parsed_text = ""
    if file_extension == "pdf":
        parsed_text = extract_text_from_pdf(file_path)
    elif file_extension == "docx":
        parsed_text = extract_text_from_docx(file_path)

    # Perform keyword extraction from the extracted text
    parsed_resume = process_resume(parsed_text)

    # Perform keyword matching from extracted resume and extracted job descriptions
    jobs = pd.DataFrame(list(collection.find()))
    matched_jobs = keyword_match(parsed_resume, jobs)

    matched_jobs = matched_jobs.drop(
        columns=["_id", "cleaned", "selective", "selective_reduced", "tf_based"]
    )

    matched_jobs = matched_jobs.to_json(orient="records")

    # Send the response back to the client-side
    return jsonify(matched_jobs)


# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
