import sqlite3
def init_db(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL
                )
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams(
                -- exams
                id INTEGER PRIMARY KEY,
                subject_id INTEGER REFERENCES subjects(id),
                year INTEGER NOT NULL,
                phase INTEGER NOT NULL,
                pdf_path TEXT,
                processed_at TIMESTAMP
            )
        """)


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics(
                -- topics
                id INTEGER PRIMARY KEY,
                subject_id INTEGER REFERENCES subjects(id),
                name TEXT NOT NULL,
                description TEXT,
                UNIQUE(subject_id, name) 
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_topics(
                -- exam_topics
                exam_id REFERENCES exams(id),
                topic_id REFERENCES topics(id),
                confidence REAL,
                PRIMARY KEY (exam_id, topic_id)
            )
        """)

        conn.commit()

def get_subject_id(subject_code, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id FROM subjects WHERE code = ?""", (subject_code, ))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("""INSERT INTO subjects (name, code) VALUES (?,?)""", (subject_code, subject_code))
            conn.commit()
            return cursor.lastrowid
    return result[0] 

def add_topic(topic_name, confidence, exam_id, subject_id, db_path):
    topic_name = topic_name.strip().capitalize()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT OR IGNORE INTO topics (name, subject_id) VALUES (?, ?)""", (topic_name, subject_id))
        cursor.execute("""SELECT id FROM topics WHERE name = ? AND subject_id = ?""", (topic_name, subject_id))
        topic_id = cursor.fetchone()[0]
        cursor.execute("""INSERT OR IGNORE INTO exam_topics (topic_id, confidence, exam_id) VALUES (?,?,?)""", (topic_id, confidence, exam_id))
        conn.commit()

def add_exam(year, phase, subject_id, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT OR IGNORE INTO exams (year, phase, subject_id) VALUES (?,?,?)""", (year, phase, subject_id))
        cursor.execute("""SELECT id FROM exams WHERE (year, subject_id, phase) = (?, ?, ?)""", (year, phase, subject_id))
        exam_id = cursor.fetchone()[0]
        conn.commit()
        return exam_id

def get_topics(subject_id, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM topics WHERE subject_id = ?""", (subject_id, ))
        t = cursor.fetchall()
    return  [row[0] for row in t]