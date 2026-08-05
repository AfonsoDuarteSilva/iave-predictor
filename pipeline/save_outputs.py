import json
import os

def save_topics_txt(topics, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf_8") as file:
        file.write(json.dumps(topics, indent=4, ensure_ascii=False))