import requests
import sys

# Usage: python examples/test_textract_http.py /path/to/file.pdf
if len(sys.argv) != 2:
    print("Usage: python examples/test_textract_http.py /path/to/file.pdf")
    sys.exit(1)

file_path = sys.argv[1]
url = "http://127.0.0.1:8000/extract-text"

payload = {"file_path": file_path}
response = requests.post(url, json=payload)

print(f"Status code: {response.status_code}")
try:
    print(response.json())
except Exception:
    print(response.text) 