import sqlite3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, render_template
from pipeline.scorer import calculates_scores

app = Flask(__name__)

@app.route("/")
def index():
    with sqlite3.connect("data/iave.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, code FROM subjects")
        subjects = cursor.fetchall()
    return render_template("index.html", subjects=subjects)

@app.route("/<subject_code>")
def subject(subject_code):
    scores = calculates_scores(subject_code, "data/iave.db")
    return render_template("subject.html", scores=scores)

if __name__ == "__main__":
    app.run(debug=True)