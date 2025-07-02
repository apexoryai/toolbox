import sys
import json
import subprocess
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import requests

def extract_text_with_agent(file_path):
    url = "http://127.0.0.1:8000/extract-text"  # Your FastAPI Textract server
    response = requests.post(url, json={"file_path": file_path})
    if response.status_code != 200:
        print("Error extracting text:", response.text)
        exit(1)
    data = response.json()
    return data.get("text", "")

def summarize_text(text):
    if not text.strip():
        print("No text to summarize.")
        sys.exit(1)
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    prompt = f"Summarize the following document:\n\n{text}"
    response = model.invoke(prompt)
    if hasattr(response, 'content'):
        print("Summary:\n" + response.content)
    else:
        print("Summary:\n" + str(response))

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/agents/orchestrator_extract_and_summarize.py /path/to/file.pdf")
        sys.exit(1)
    file_path = sys.argv[1]
    text = extract_text_with_agent(file_path)
    summarize_text(text)

if __name__ == "__main__":
    main()
