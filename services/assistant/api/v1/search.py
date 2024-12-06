from fastapi import APIRouter, Request, Depends, File, UploadFile
from fastapi.responses import FileResponse

from services.speech import SpeechService
from services.intent import IntentClassifierService
from services.search import SearchService
from services.extractor import EntityExtractorService
from services.translate import TranslationService

from utils.logger import logger
from utils.enums import Intents
from mappers.intent import INTENT_TO_ACTION_MAPPING

from dependencies.speech import get_speech_service
from dependencies.intent import get_intent_classifier_service
from dependencies.search import get_search_service
from dependencies.extractor import get_entity_extractor_service
from dependencies.translate import get_translation_service

router = APIRouter()


@router.post("/")
async def search(
    request: Request,
    transcript: str,
    # audio_file: UploadFile = File(),
    speech_service: SpeechService = Depends(get_speech_service),
    intent_service: IntentClassifierService = Depends(get_intent_classifier_service),
    extractor_service: EntityExtractorService = Depends(get_entity_extractor_service),
    translate_service: TranslationService = Depends(get_translation_service),
    search_service: SearchService = Depends(get_search_service),
):
    logger.info("Transcribing...")
    # transcript = await speech_service.transcribe_audio(audio_file)
    logger.info(f"Transcribed: {transcript}")

    logger.info("Getting intent...")
    intent = await intent_service.predict_intent(transcript)
    logger.info(f"Got intent: {intent}")

    logger.info("Translating...")
    transcript_en = await translate_service.translate(transcript)
    logger.info(f"Translated: {transcript_en}")

    logger.info("Extracting persons...")
    persons = await extractor_service.extract_persons(transcript_en)
    logger.info(f"Got persons: {persons}")

    logger.info("Extracting genres...")
    genres = await extractor_service.extract_genres(transcript_en)
    logger.info(f"Got genres: {genres}")

    logger.info("Extracting films...")
    films = await extractor_service.extract_films(transcript_en)
    logger.info(f"Got films: {films}")

    logger.info("Searching...")
    if intent in INTENT_TO_ACTION_MAPPING:
        action = INTENT_TO_ACTION_MAPPING[intent]
        search_result = await action["method"](search_service, films)
        response_message = action["response"](search_result, films)
    else:
        raise Exception("Намерение не поддерживается.")

    return {
        "response": response_message,
        "transcript": transcript,
        "transcript_en": transcript_en,
        "intent": intent,
        "persons": persons,
        "genres": genres,
        "films": films
    }
