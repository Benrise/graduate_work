import wave
import os
import json

from RUTTS import TTS
from ruaccent import RUAccent

from pathlib import Path
from fastapi import UploadFile
from vosk import Model, KaldiRecognizer

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class SpeechService:
    def __init__(self, recognize_model_path: str, tts_model_name: str):
        self.recognizer = Model(recognize_model_path)
        self.tts = TTS(tts_model_name, save_path=MODELS_DIR)

        self.accentizer = RUAccent()
        self.accentizer.load(
            omograph_model_size='medium_poetry',
            use_dictionary=True,
            workdir=MODELS_DIR
        )

    async def transcribe_audio(self, file: UploadFile) -> str:

        file_location = DATA_DIR / f"temp_{file.filename}"

        with open(file_location, "wb") as f:
            f.write(await file.read())

        wf = wave.open(str(file_location), "rb")
        if wf.getsampwidth() != 2:
            raise ValueError("Audio file must be 16-bit mono")

        os.remove(str(file_location))

        recognizer = KaldiRecognizer(self.recognizer, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

        final_result = json.loads(recognizer.FinalResult())
        return str(final_result.get("text", ""))

    async def text_to_speech(self, text: str, filename: str) -> str:
        text = self.accentizer.process_all(text)

        audio = self.tts(text)

        path_to_file = DATA_DIR / filename
        self.tts.save_wav(audio, str(path_to_file))

        return str(path_to_file)
