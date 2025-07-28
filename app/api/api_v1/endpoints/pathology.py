# routes/pathology.py

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from datetime import datetime
import pytesseract
from PIL import Image
from io import BytesIO

from app.database.mongodb import db
from app.core.config import settings
from app.core.user_client import get_ai_response


router = APIRouter()

@router.post("/pathologyFiles")
async def upload_pathology_file(
    promptText: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        ocr_text = pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    final_prompt = f"{promptText.strip()}\n\nExtracted pathology report text:\n{ocr_text.strip()}"

    ai_message = await get_ai_response(final_prompt)

    report = {
        "promptText": promptText,
        "ocrText": ocr_text,
        "aiResponse": ai_message,
        "type": "pathology",
        "createdAt": datetime.utcnow()
    }

    try:
        result = await db["pathologys"].insert_one(report)
        report_id = str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database save failed: {str(e)}")

    return {
        "id": report_id,
        "ocr_text": ocr_text,
        "ai_response": ai_message,
        "message": "✅ OCR extracted, AI response generated, and stored successfully!"
    }
