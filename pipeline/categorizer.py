from dotenv import load_dotenv
import os
import anthropic
import json
import re

def extract_groups(text):
    text = text.split("COTAÇÕES")[0]
    keys = re.findall(r'GRUPO [IVX]+', text)
    parts = re.split(r'GRUPO [IVX]+', text)
    return dict(zip(keys,parts[1:]))

load_dotenv()
client = anthropic.Anthropic()

def categorize_text(text, subject, existing_topics):
    system = (
        "You are a JSON-only API. Return ONLY JSON, no text before or after.\n"
        "Pick a maximum of 4 topics per group.\n"
        "Return ONLY JSON in this format, NO markdown, NO backticks:\n"
        "Wrap the JSON in <json></json> tags. Example: <json>{\"topics\": [{\"name\": \"topic name\", \"confidence\": 0.9}]}</json>\n"
    )
    prompt = (
        f"Analyze the following {subject} exam text and identify the topics covered.\n"
        f"Here are topics already identified in other exams for reference: {existing_topics}\n"
        f"Use similar naming when the subject is the same, but don't feel constrained by this list.\n"
        f"Text:\n{text}"
    )
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        system=system,
        messages=[
        {"role": "user", "content": prompt} 
        ]
    )
    print(response.content[0].text) 
    raw = response.content[0].text
    match = re.search(r'<json>(.*?)</json>', raw, re.DOTALL)
    clean = match.group(1).strip() if match else raw
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"topics": []}   