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
TARGET_YEAR = CURRENT_YEAR + 1

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

    scores_next = calculates_scores(subject_id, DB_PATH, target_year=TARGET_YEAR)
    scores_curr = calculates_scores(subject_id, DB_PATH, target_year=CURRENT_YEAR)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.name, GROUP_CONCAT(e.year ORDER BY e.year)
            FROM topics t
            JOIN exam_topics et ON et.topic_id = t.id
            JOIN exams e ON e.id = et.exam_id
            WHERE t.subject_id = ?
            GROUP BY t.id
        """, (subject_id,))
        topic_years = {row[0]: row[1] for row in cursor.fetchall()}

    sorted_scores = sorted(scores_next.items(), key=lambda x: -x[1])

    enriched = []
    for topic, score in sorted_scores:
        prev = scores_curr.get(topic, score)
        diff = score - prev
        if diff > 0.01:
            trend = "up"
        elif diff < -0.01:
            trend = "down"
        else:
            trend = "neutral"

        years_str = topic_years.get(topic, "")
        enriched.append({
            "name": topic,
            "score": score,
            "trend": trend,
            "years": years_str.replace(",", " · ") if years_str else "",
        })

    return render_template(
        "subject.html",
        subject_name=subject_name,
        subject_code=subject_code,
        scores=enriched,
        phases=PHASES,
        selected_phase=selected_phase,
        target_year=TARGET_YEAR,
    )

if __name__ == "__main__":
    app.run(debug=True)