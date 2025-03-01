from flask import Flask, request, render_template, redirect, url_for
from main_web import interface
import os

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
text_processor = interface('')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "zip_file" in request.files:
            file = request.files["zip_file"]
            if file.filename.endswith(".zip"):
                zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(zip_path)

                # Process the ZIP file using textdf class
                text_processor = interface(zip_path)
                extracted_files = text_processor.df.extract_zip(zip_path)

                return f"Extracted Files: {extracted_files}"
            else:
                return "Please upload a valid ZIP file."

    return render_template("Home.html")

# @app.route('/sum')
# def sum():
#     return inter.sum_chat(lang= '1')

@app.route("/week_count")
def week_count():
    result = text_processor.df.count_by_week().split("\n")  # Convert text into a list
    return render_template("message count.html", result=result)

# @app.route('/enter_date')
# def enter_date

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)