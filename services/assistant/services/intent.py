import joblib


class IntentClassifierService:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    async def predict_intent(self, text: str) -> str:
        text_tfidf = self.vectorizer.transform([text])
        intent = self.model.predict(text_tfidf)[0]
        return intent
