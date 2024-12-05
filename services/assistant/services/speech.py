import wave
import os
import json

from pathlib import Path
from speakerpy.lib_speak import Speaker
from fastapi import UploadFile
from vosk import Model, KaldiRecognizer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)


class SpeechService:
    def __init__(self, recognize_model_path: str, speaker_model_id: str, language: str, speaker: str, device: str):
        self.recognizer = Model(recognize_model_path)
        self.speaker = Speaker(model_id=speaker_model_id, language=language, speaker=speaker, device=device)

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
        return final_result.get("text", "")

    def text_to_speech(self, text: str,) -> str:

        result = self.speaker.to_mp3(
            text=text,
            name_text='answer',
            sample_rate=48000,
            audio_dir="./data",
            speed=1.0
        )

        return result[0]
