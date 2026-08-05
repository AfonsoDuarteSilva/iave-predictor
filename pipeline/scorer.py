import sqlite3
import math


LAMBDA = 0.3
current_year = 2026

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculates_scores(subject_id, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM topics WHERE subject_id = ?", (subject_id,))
        topics = cursor.fetchall()
        scores = {} 
        # For each topic, get all years in which it appeared across exams
        for topic_id, topic_name in topics:
            cursor.execute("""
            SELECT DISTINCT e.year FROM exams e
            JOIN exam_topics et ON et.exam_id = e.id
            WHERE et.topic_id = ?
            """, (topic_id,))
            years = cursor.fetchall()
            score = 0
            for(year,) in years:
                score += math.exp(-LAMBDA * (current_year - year))
            scores[topic_name] = sigmoid(score) 
    return scores
        