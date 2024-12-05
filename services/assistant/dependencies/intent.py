from services.intent import IntentClassifierService
from sentence_transformers import SentenceTransformer
from pipelines.keyphrase_extraction import KeyphraseExtractionPipeline

EMBEDDING_MODEL = "sentence-transformers/sentence-t5-base"
EXTRACTOR_MODEL = "ml6team/keyphrase-extraction-kbir-inspec"


def get_intent_classifier_service():
    return IntentClassifierService(
        extractor_model=KeyphraseExtractionPipeline(EXTRACTOR_MODEL),
        embedding_model=SentenceTransformer(EMBEDDING_MODEL),
    )
