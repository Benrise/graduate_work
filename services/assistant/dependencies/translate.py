from services.translate import TranslationService

MODEL_NAME = 'Helsinki-NLP/opus-mt-ru-en'


def get_translation_service():
    return TranslationService(MODEL_NAME)
