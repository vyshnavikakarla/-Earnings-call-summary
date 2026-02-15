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

    result = None

    if request.method == "POST":

        file = request.files.get["file"]

        if file and file.filename != "":

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = extract_text(filepath)


            if not text.strip():
                 result = "Error: Could not extract text from PDF."
            else:
                  result = summarize_text(text)


    return render_template("index.html", result=result)




if __name__ == "__main__":
    app.run()
