from flask import Flask, request, render_template, redirect, url_for
from main_web import interface
import os

app = Flask(__name__)

text_processor = None
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/", methods=["GET", "POST"])
def home():
    global text_processor

    if request.method == "POST":
        if "zip_file" in request.files:
            file = request.files["zip_file"]
            if file.filename.endswith(".zip"):
                zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(zip_path)

                text_processor = interface(zip_path)
                return redirect(url_for("menu"))
            else:
                return render_template('error.html', message="Please upload a valid ZIP file.")
    return render_template("Home.html")

@app.route('/menu')
def menu():
    global sum_res, arg_res
    sum_res,arg_res = None, None
    return render_template('menu.html')

@app.route('/sum_eng')
def sum():
    global sum_res
    if text_processor is None:
        return render_template('error.html', message="No ZIP file was uploaded.")
    if sum_res is None:
        sum_res = text_processor.sum_chat(lang='1')
    return render_template('text_template.html', page_title = 'AI Summary of Chat', page_content = sum_res)

@app.route('/arg_eng')
def arg():
    global arg_res
    if text_processor is None:
        return render_template('error.html', message="No ZIP file was uploaded.")
    if arg_res is None:
        arg_res = text_processor.arg_chat(lang='1')
    return render_template('text_template.html', page_title = 'Who is Right?', page_content = arg_res)

@app.route("/week_count")
def week_count():
    if text_processor is None:
        return "No ZIP file has been uploaded yet!"

    result = text_processor.df.count_by_week().split("\n")  # Convert text into a list
    return render_template("message count.html", result=result)

# @app.route('/enter_date')
# def enter_date

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)