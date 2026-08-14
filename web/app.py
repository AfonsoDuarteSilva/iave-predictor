import sqlite3
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, render_template, request
from pipeline.scorer import calculates_scores

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "iave.db")

CURRENT_YEAR = datetime.now().year
PHASES = [
    {"value": "1", "label": "1.ª Fase"},
    {"value": "2", "label": "2.ª Fase"},
    {"value": "e", "label": "Época Especial"},
]

@app.route("/")
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, code FROM subjects")
        subjects = cursor.fetchall()
    return render_template("index.html", subjects=subjects)

@app.route("/<subject_code>")
def subject(subject_code):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM subjects WHERE code = ?", (subject_code,))
        row = cursor.fetchone()
    if not row:
        return "Disciplina não encontrada", 404

    subject_id, subject_name = row
    selected_phase = request.args.get("phase", "1")
    scores = calculates_scores(subject_id, DB_PATH, target_year=CURRENT_YEAR + 1)
    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])

    return render_template(
        "subject.html",
        subject_name=subject_name,
        subject_code=subject_code,
        scores=sorted_scores,
        phases=PHASES,
        selected_phase=selected_phase,
    )

if __name__ == "__main__":
    app.run(debug=True)