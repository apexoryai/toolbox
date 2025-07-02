import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = FastAPI()

class FilePathRequest(BaseModel):
    file_path: str

def extract_text_from_file(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        return {"error": f"File not found: {file_path}"}
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    is_pdf = ext == ".pdf"
    try:
        region = os.getenv("AWS_REGION", "us-east-1")
        textract = boto3.client("textract", region_name=region)
        with open(file_path, "rb") as f:
            document_bytes = f.read()
        if is_pdf:
            response = textract.analyze_document(
                Document={"Bytes": document_bytes},
                FeatureTypes=["TABLES", "FORMS"]
            )
        else:
            response = textract.detect_document_text(
                Document={"Bytes": document_bytes}
            )
        blocks = response.get("Blocks", [])
        lines = [b["Text"] for b in blocks if b["BlockType"] == "LINE"]
        text = "\n".join(lines)
        return {"text": text, "blocks": blocks}
    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

@app.post("/extract-text")
async def extract_text(request: FilePathRequest):
    result = extract_text_from_file(request.file_path)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return JSONResponse(content=result) 