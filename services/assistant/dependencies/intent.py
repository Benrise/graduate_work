from services.intent import IntentClassifierService

CLISSIFIER_MODEL_PATH = "./models/intent_model.pkl"
VECTORIZER_MODEL_PATH = "./models/vectorizer.pkl"


def get_intent_classifier_service():
    return IntentClassifierService(
        model_path=CLISSIFIER_MODEL_PATH,
        vectorizer_path=VECTORIZER_MODEL_PATH
    )
