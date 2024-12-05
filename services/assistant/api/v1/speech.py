from pathlib import Path

from fastapi import APIRouter, Request, Depends, File, UploadFile
from fastapi.responses import FileResponse

from services.speech import SpeechService
from dependencies.speech import get_speech_service


router = APIRouter()


@router.post("/speech-to-text")
async def speech_to_text(
    request: Request,
    file: UploadFile = File(...),
    speech_service: SpeechService = Depends(get_speech_service),
):
    transcript = await speech_service.transcribe_audio(file)
    return {
        "transcript": transcript
    }


@router.post("/text-to-speech")
async def text_to_speech(
    request: Request,
    text: str,
    speech_service: SpeechService = Depends(get_speech_service),
):

    output_file = speech_service.text_to_speech(text)
    return FileResponse(
        path=str(output_file),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=answer.mp3"}
    )
