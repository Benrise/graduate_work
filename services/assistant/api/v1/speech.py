from fastapi import APIRouter, Request


router = APIRouter()


@router.post("/speech-to-text")
async def speech_to_text(
    request: Request,
):

    return {
        "detail": "ok",
    }


@router.post("/text-to-speech")
async def text_to_speech(
    request: Request,
):

    return {
        "detail": "ok",
    }