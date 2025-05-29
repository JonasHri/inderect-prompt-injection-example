# %%
from dotenv import load_dotenv
import requests
import json
import fitz
import os

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

# %%

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

pdf_text = extract_text_from_pdf("./The History of Airplanes.pdf")

# %%

api_url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def make_message(text:str):
    return {"role": "user", "content": text}


# Chat history format
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    make_message(f"Tell me what is written inside the following text:\n {pdf_text}")
]

data = {
    "model": "gpt-3.5-turbo",
    "messages": messages,
    "temperature": 0.7
}

response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Parse and print the assistant's reply
if response.status_code == 200:
    reply = response.json()["choices"][0]["message"]["content"]
    print("Assistant:", reply)
else:
    print("Error:", response.status_code, response.text)
# %%

print(messages[-1]["content"])