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
        f"You are a JSON-only API. Never explain your reasoning. Never write text before or after the JSON.\n"
        f"If an existing topic covers the exact same subject, you MUST use its exact name.\n"
        f"If no existing topic is similar enough (CONFIDENCE BELOW 70 CREATE TOPIC), you MUST create a new one — never ignore a topic just because it's not in the list.\n"
        f"Pick a maximum of 4 topics per group.\n"
        f"Return ONLY JSON in this format,NO markdown, NO backticks:\n"
        f'{{\"topics\": [{{\"name\": \"topic name\", \"confidence\": 0.9}}]}}\n\n'
    )

    prompt = (
        f"Analyze the following {subject} exam text and identify the topics covered.\n"
        f"Existing topics: {existing_topics}\n\n"
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
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    clean = match.group(0) if match else raw
    print(repr(clean))
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        print("Not valid fomat")
        return {"topics":[]}