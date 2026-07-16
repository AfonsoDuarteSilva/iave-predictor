import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.database import get_subject_id
from pipeline.extractor import extract_pdf, save_raw_text
from pipeline.categorizer import categorize_text
from pipeline.scorer import calculates_scores

def main():
    if len(sys.argv) != 2:
        print("Pass only one argument!")
        sys.exit(1)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = sys.argv[1]
    pdf = extract_pdf(path)
    filename, ext = os.path.splitext(os.path.basename(path))
    output_path = os.path.join(project_root, "data", "raw", filename + ".txt")
    save_raw_text(pdf, output_path)
    subject = os.path.basename(os.path.dirname(path))
    categorize_text(pdf, subject)
    db_path = os.path.join(project_root, "data", "iave.db")
    subject_id = get_subject_id(subject, db_path)
    calculates_scores(subject_id, db_path)

if __name__ == "__main__":
    main()
