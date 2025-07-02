import requests
import sys

if len(sys.argv) != 2:
    print("Usage: python tests/test_hotel_agent_textract.py /path/to/file.pdf")
    sys.exit(1)

file_path = sys.argv[1]
url = "http://127.0.0.1:8000/extract-text"
payload = {"file_path": file_path}
response = requests.post(url, json=payload)
print("Status code:", 
response.status_code)
print(response.json())