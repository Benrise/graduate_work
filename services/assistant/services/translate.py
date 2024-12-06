from transformers import MarianMTModel, MarianTokenizer


class TranslationService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)

    async def translate(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        translated = self.model.generate(**inputs)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)
