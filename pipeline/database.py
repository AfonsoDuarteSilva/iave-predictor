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
            CREATE TABLE IF NOT EXISTS questions(
                -- questions
                id INTEGER PRIMARY KEY,
                exam_id INTEGER REFERENCES exams(id),
                number TEXT NOT NULL,
                raw_text TEXT       
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
            CREATE TABLE IF NOT EXISTS question_topics(
                -- question_topics
                question_id INTEGER REFERENCES questions(id),
                topic_id INTEGER REFERENCES topics(id),
                confidence REAL,
                PRIMARY KEY (question_id, topic_id)
            )     
        """)

        conn.commit()

def get_subject_id(subject_code, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT id FROM subjects WHERE code = ?""", (subject_code, ))
        result = cursor.fetchone()
        return result[0]
