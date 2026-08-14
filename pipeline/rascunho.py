import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
from pipeline.database import get_subject_id, add_topic, add_exam, get_topics, init_db
from pipeline.extractor import extract_pdf, save_raw_text
from pipeline.categorizer import categorize_text, extract_groups
from pipeline.scorer import calculates_scores
from pipeline.save_outputs import save_topics_txt
from pipeline.normalize import normalize_topics, match_to_existing

def main():
    if len(sys.argv) != 2:
        print("Pass only one argument!")
        sys.exit(1)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = sys.argv[1]
    text = extract_pdf(path)
    db_path = os.path.join(project_root, "data", "iave.db")
    init_db(db_path)
    filename, ext = os.path.splitext(os.path.basename(path))
    subject = os.path.basename(os.path.dirname(path))
    subject_id = get_subject_id(subject, db_path)
    info = filename.split("-")
    exam_year = int((info[3]))
    exam_phase = int(info[2][1:])
    exam_id = add_exam(exam_year, exam_phase, subject_id, db_path)
    output_path = os.path.join(project_root, "data", "raw", filename + ".txt")
    save_raw_text(text, output_path)

    existing_topics = get_topics(subject_id, db_path)
    raw_exam_topics = []

    groups = extract_groups(text)
    print(groups.keys())
    
    for group_name, group_text in groups.items():
        topics = categorize_text(group_text, subject, existing_topics)
        group_topics = topics.get("topics", [])
        raw_exam_topics.extend(group_topics)

    filtered_topics = [t for t in raw_exam_topics if t["confidence"] >= 0.75]
    norm_exam = normalize_topics(filtered_topics, 0.65)

    all_topics = []
    for topic in norm_exam:
        topic["name"] = match_to_existing(topic["name"], existing_topics, 0.65)
        
        add_topic(topic["name"], topic["confidence"], exam_id, subject_id, db_path)
        
        if topic["name"] not in existing_topics:
            existing_topics.append(topic["name"])
            
        all_topics.append(topic)

    output_path = os.path.join(project_root, "data", "outputs", f"{exam_year}_{exam_phase}.txt")
    save_topics_txt(all_topics, output_path)

    calculates_scores(subject_id, db_path)

if __name__ == "__main__":
    main()