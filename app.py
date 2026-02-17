from flask import Flask, render_template, request
import os
from utils.extractor import extract_text
from utils.summarizer import summarize_text
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 4MB file size limit
MAX_FILE_SIZE = 4 * 1024 * 1024  

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    print("Route accessed")

    result = None

    if request.method == "POST":
        print("POST request received")

        file = request.files.get("file")

        if not file or file.filename == "":
            result = "Please upload a PDF file."
            return render_template("index.html", result=result)

        #  FILE SIZE CHECK
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE:
            result = "File too large. Please upload PDF under 4MB."
            return render_template("index.html", result=result)

        print("File name:", file.filename)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        print("File saved at:", filepath)

        # Extract text
        text = extract_text(filepath)
        print("Extracted text length:", len(text))

        if not text.strip():
            result = "Error: Could not extract text from PDF."
        else:
            #  LIMIT TEXT TO PREVENT TIMEOUT
            text = text[:3000]
            print("Text truncated to 3000 characters")

            print("Calling summarizer...")
            result = summarize_text(text)
            print("Summary generated successfully")

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
