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

    # transcript = await speech_service.transcribe_audio(audio_file)

    embedding_vectors = intent_service.get_sentence_embeddings(transcript)

    query = {
        "query": {
            "bool": {
                "must": []
            }
        },
        "knn": {
            "field": "embedding_vectors",
            "query_vector": embedding_vectors,
            "k": 10,
            "num_candidates": 100
        }
    }

    result = await search_service.search(request, index=Indecies.MOVIES.value, query=query)

    print("RESULT:", result)

    output_list = []

    if result:
        for hit in result['hits']['hits']:
            keyphrases = intent_service.extractor_model(transcript)

            output_json = {
                "title": hit["_source"]["title"],
                "score": hit["_score"],
                "extract": intent_service.get_key_location(
                    hit["_source"]["description"],
                    keyphrases,
                    hit["_source"]["title"]
                ),
                "genres": hit["_source"]["genres"],
                "actors": hit["_source"]["actors"],
                "writers": hit["_source"]["writers"],
                "directors": hit["_source"]["directors"],
            }

            output_list.append(output_json)

    return {
        "context_fragments": output_list,
        "total_matches": len(output_list)
    }
