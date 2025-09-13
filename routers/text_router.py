from fastapi import APIRouter, HTTPException

# local imports
from schemas import TextRequest
from utils import get_ollama_summary, get_ollama_questions

router = APIRouter(prefix="/text", tags=["text"])

@router.post("/summarize")
async def summarize_text(request: TextRequest):
    try:
        summary = get_ollama_summary(text=request.text, model=request.model)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/questions")
async def generate_questions(request: TextRequest):
    try:
        questions = get_ollama_questions(text=request.text, model=request.model)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))