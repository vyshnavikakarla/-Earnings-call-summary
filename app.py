from flask import Flask, render_template, request
import os
from utils.extractor import extract_text
from utils.summarizer import summarize_text
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)


UPLOAD_FOLDER = "/tmp"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Route accessed")

    result = None

    if request.method == "POST":
        print("POST request received")

        file = request.files.get("file")
        print("File object:", file)

        if file and file.filename != "":
            print("File name:", file.filename)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            print("File saved at:", filepath)

            text = extract_text(filepath)
            print("Extracted text length:", len(text))

            if not text.strip():
                print("No text extracted")
                result = "Error: Could not extract text from PDF."
            else:
                print("Calling summarizer...")
                result = summarize_text(text)
                print("Summary generated successfully")

    return render_template("index.html", result=result)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

