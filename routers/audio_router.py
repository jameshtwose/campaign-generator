from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import shutil
import os
from utils import convert_webm_to_mp3, transcribe_audio

router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_file_path = f"/tmp/{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Call the transcribe_audio function from utils
        content = transcribe_audio(temp_file_path)
        print(content)
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return {"content": content}


@router.post("/record")
async def record_audio(
    file: UploadFile = File(...),
    save_dir: str = Query(default="~/Desktop", description="Directory to save the audio file")
):
    save_dir = os.path.expanduser(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    webm_path = os.path.join(save_dir, file.filename)
    mp3_filename = os.path.splitext(file.filename)[0] + ".mp3"
    mp3_path = os.path.join(save_dir, mp3_filename)
    try:
        with open(webm_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Convert WebM to MP3
        convert_webm_to_mp3(webm_path, mp3_path)
        # Optionally, remove the original WebM file
        os.remove(webm_path)
        return {"message": "Audio recorded and converted to MP3 successfully", "file_path": mp3_path}
    except Exception as e:
        if os.path.exists(webm_path):
            os.remove(webm_path)
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        raise HTTPException(status_code=500, detail=str(e))