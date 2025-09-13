from fastapi import APIRouter, Response
import os
router = APIRouter(prefix="/frontend", tags=["frontend"])

@router.get("")
async def serve_audio_recorder():
	template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "home.html")
	try:
		with open(template_path, "r", encoding="utf-8") as f:
			html_content = f.read()
		return Response(content=html_content, media_type="text/html")
	except Exception as e:
		return Response(content=f"Error loading template: {e}", media_type="text/plain", status_code=500)
