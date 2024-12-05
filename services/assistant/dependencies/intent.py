from services.intent import IntentClassifierService


def get_intent_classifier_service():
    return IntentClassifierService(
        model=str('services/assistant/models/intent/model'),
    )
