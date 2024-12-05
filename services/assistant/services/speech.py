import wave
import os
import json

from pathlib import Path

from fastapi import UploadFile

from vosk import Model, KaldiRecognizer


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)


class SpeechService:
    def __init__(self, model_path: str):
        self.model = Model(model_path)

    async def transcribe_audio(self, file: UploadFile) -> str:
        file_location = DATA_DIR / f"temp_{file.filename}"

        with open(file_location, "wb") as f:
            f.write(await file.read())

        wf = wave.open(str(file_location), "rb")
        if wf.getsampwidth() != 2:
            raise ValueError("Audio file must be 16-bit mono")

        os.remove(file_location)

        recognizer = KaldiRecognizer(self.model, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

        final_result = json.loads(recognizer.FinalResult())
        return final_result.get("text", "")
