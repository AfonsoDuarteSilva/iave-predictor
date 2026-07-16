import anthropic

client = anthropic.Anthropic()

def categorize_text(text, subject):
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
        {"role": "user", "content": f"Analyze the following {subject} exam text and identify the historical topics covered.\nReturn ONLY JSON in this format:\n{{\"topics\": [{{\"name\": \"topic name\", \"confidence\": 0.9}}]}}\n\nText:\n{text}"}
        ]
    )
    return response.content[0].text