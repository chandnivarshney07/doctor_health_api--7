# utils/user_client.py

import requests
from fastapi import HTTPException
from app.core.config import settings # ✅ Import from config
api_key = settings.AIML_API_KEY
api_url = settings.AIML_API_URL
async def get_ai_response(prompt: str) -> str:
    try:
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemma-3n-e4b-it",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "top_p": 0.7,
                "frequency_penalty": 1,
                "max_tokens": 512,
                "top_k": 50,
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"AI API call failed: {str(e)}")

