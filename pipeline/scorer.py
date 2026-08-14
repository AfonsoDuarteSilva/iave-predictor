import sqlite3
import math
from datetime import datetime

ALPHA = 0.5

def calculates_scores(subject_id, db_path, target_year=None, phase=None):
    current_year = target_year if target_year else datetime.now().year

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM exams WHERE subject_id = ?", (subject_id,))
        total_exams = cursor.fetchone()[0]

        if total_exams == 0:
            return {}

        cursor.execute("SELECT id, name FROM topics WHERE subject_id = ?", (subject_id,))
        topics = cursor.fetchall()

        scores = {}

        for topic_id, topic_name in topics:
            cursor.execute("""
                SELECT e.year FROM exams e
                JOIN exam_topics et ON et.exam_id = e.id
                WHERE et.topic_id = ?
            """, (topic_id,))
            years = [row[0] for row in cursor.fetchall()]

            if not years:
                scores[topic_name] = 0.0
                continue

            lam = len(years) / total_exams
            x = current_year - max(years)
            score = ALPHA * lam + (1 - ALPHA) * (1 - math.exp(-lam * x))
            scores[topic_name] = round(score, 4)

    return scores