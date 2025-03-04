import datetime
from Exceptions import DateError
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from main_web import interface
from dateutil import parser
import os
import uuid


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for sessions

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global dictionary to hold per-user data (keyed by user_id)
user_data = {}


def get_user_id():
    """
    Retrieve a unique user_id from the session. If none exists, create one.
    """
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    return session["user_id"]

def detect_language(text):
    hebrew_count = sum(1 for c in text if "\u0590" <= c <= "\u05FF")  # אותיות עבריות
    english_count = sum(1 for c in text if "A" <= c <= "Z" or "a" <= c <= "z")  # אותיות באנגלית

    return "rtl" if hebrew_count > english_count else "ltr"


@app.route("/", methods=["GET"])
def home():
    # דף הבית: מציג את הקובץ "zip extract.html" עם אפשרות העלאת קובץ ZIP.
    return render_template("zip extract.html")


@app.route("/process_text", methods=["POST"])
def process_text():
    """
    ראוט שמקבל את המחרוזת שהופקה מהקובץ (באמצעות JSZip בצד הלקוח)
    ויוצר ממנה את text_processor עבור המשתמש.
    """
    user_id = get_user_id()
    data = request.json
    extracted_text = data.get("text", "")
    if not extracted_text:
        return jsonify({"error": "No text received"}), 400

    # ייצור מעבד הטקסט בעזרת הפונקציה interface, שמקבלת את המחרוזת
    user_data[user_id] = {
        "text_processor": interface(ready_str=extracted_text),
        "sum_res": None,
        "arg_res": None,
        "start_date": None,
        "end_date": None
    }

    return jsonify({"message": "Processor created", "text": extracted_text})

@app.route('/menu')
def menu():
    user_id = get_user_id()
    # Reset previous results and date selections for a fresh start.
    if user_id in user_data:
        user_data[user_id]["sum_res"] = None
        user_data[user_id]["arg_res"] = None
        user_data[user_id]["start_date"] = None
        user_data[user_id]["end_date"] = None
    return render_template('menu.html')



@app.route('/sum_eng')
def sum_eng():
    # try:
    user_id = get_user_id()
    if user_id not in user_data or user_data[user_id].get("text_processor") is None:
        return render_template('error.html', message="No ZIP file was uploaded.")

    if user_data[user_id].get("start_date") is None or user_data[user_id].get("end_date") is None:
        return redirect(url_for('select_dates', next_action='sum_eng'))

    tp = user_data[user_id]["text_processor"]
    sum_res = tp.sum_chat(lang='1', start_time=user_data[user_id]["start_date"], end_time=user_data[user_id]["end_date"])
    user_data[user_id]["sum_res"] = sum_res
    if sum_res == '':
        return render_template('error.html', message="No messages in time range.")
    text_direction = detect_language(sum_res)
    return render_template('text_template.html', page_title='AI Summary of Chat', page_content=sum_res, direction=text_direction)
    # except DateError as e:
    #     return render_template('error.html', message="No Message since: " + str(user_data[user_id]["start_date"]))

@app.route('/arg_eng')
def arg_eng():
    user_id = get_user_id()
    if user_id not in user_data or user_data[user_id].get("text_processor") is None:
        return render_template('error.html', message="No ZIP file was uploaded.")

    if user_data[user_id].get("start_date") is None or user_data[user_id].get("end_date") is None:
        return redirect(url_for('select_dates', next_action='arg_eng'))

    tp = user_data[user_id]["text_processor"]
    arg_res = tp.arg_chat(lang='1', start_time=user_data[user_id]["start_date"], end_time=user_data[user_id]["end_date"])
    user_data[user_id]["arg_res"] = arg_res

    return render_template('text_template.html', page_title='Who is Right?', page_content=arg_res)

@app.route("/week_count")
def week_count():
    user_id = get_user_id()
    if user_id not in user_data or user_data[user_id].get("text_processor") is None:
        return render_template('error.html', message="No ZIP file has been uploaded yet!")

    result = user_data[user_id]["text_processor"].df.count_by_week().split("\n")

    return render_template("message count.html", result=result)

@app.route("/name_count")
def name_count():
    user_id = get_user_id()
    if user_id not in user_data or user_data[user_id].get("text_processor") is None:
        return render_template('error.html', message="No ZIP file has been uploaded yet!")
    sum, count = user_data[user_id]["text_processor"].df.count_per_author()
    count = count.items()
    result = [f'There was total of: {sum} messages.']
    for name, count in count:
        result += [f'{name}:  {count} messages.']
    return render_template("name count.html", result=result)


@app.route("/select_dates")
def select_dates():
    next_action = request.args.get("next_action", "sum_eng")  # Default to sum_eng if missing
    return render_template("date_time_picker.html", next_action=next_action)

@app.route("/process_dates", methods=["POST"])
def process_dates():
    user_id = get_user_id()
    start_datetime = request.form["start_datetime"]
    end_datetime = request.form["end_datetime"]
    next_action = request.form["next_action"]

    start_dt = parser.parse(start_datetime)
    end_dt = datetime.datetime.now()  # Default to now if no end date is given

    if end_datetime != '':
        end_dt = parser.parse(end_datetime)

    user_data[user_id]["start_date"] = (start_dt.hour, start_dt.minute, start_dt.day, start_dt.month, start_dt.year)
    user_data[user_id]["end_date"] = (end_dt.hour, end_dt.minute, end_dt.day, end_dt.month, end_dt.year)

    return redirect(url_for(next_action))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)