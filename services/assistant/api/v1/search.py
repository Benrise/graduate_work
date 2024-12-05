from fastapi import APIRouter, Request, Depends, File, UploadFile
from fastapi.responses import FileResponse

from services.speech import SpeechService
from services.intent import IntentClassifierService
from services.search import SearchService

from dependencies.speech import get_speech_service
from dependencies.intent import get_intent_classifier_service
from dependencies.search import get_search_service

from utils.enums import Indecies


router = APIRouter()


@router.post("/")
async def search(
    request: Request,
    # audio_file: UploadFile = File(...),
    transcript: str,
    # speech_service: SpeechService = Depends(get_speech_service),
    intent_service: IntentClassifierService = Depends(get_intent_classifier_service),
    search_service: SearchService = Depends(get_search_service),
):

    pass
