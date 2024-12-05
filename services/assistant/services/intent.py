import regex as re


class IntentClassifierService():

    def __init__(self, extractor_model, embedding_model):
        self.extractor_model = extractor_model
        self.embedding_model = embedding_model

    def get_key_location(self, text, keyphrases, title):
        num_chars = 300
        if not keyphrases:
            return text[:num_chars] + "..."

        for keyphrase in keyphrases:
            compiled = re.compile(re.escape(keyphrase), re.IGNORECASE)
            text = compiled.sub(keyphrase, text)

        if not re.search(compiled, text):
            new_keys = self.extractor_model(title)
            return self.get_key_location(self.extractor_model, text, list(new_keys), "")

        start, end = re.search(compiled, text).span()
        start_pt = [i.end() for i in re.finditer("\n", text[:start])] or [0]
        end_pt = re.search("\n", text[end:]).start()

        if (start - start_pt[-1] + end_pt) > num_chars:
            if (start - start_pt[-1]) < end_pt:
                return "..." + text[end + end_pt - num_chars:end + end_pt]
            return text[start_pt[-1]:start_pt[-1] + num_chars] + "..."

        return text[start_pt[-1]:end + end_pt]

    def get_sentence_embeddings(self, text: str) -> list:
        """
        Generate sentence embeddings using the configured model.
        """
        sentence_embeddings = self.embedding_model.encode(text).tolist()
        return sentence_embeddings
