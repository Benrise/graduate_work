# import wave
# import os
# import json
# import pyttsx3

# from pathlib import Path
# from fastapi import UploadFile
# from vosk import Model, KaldiRecognizer

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATA_DIR = BASE_DIR / "data"

# DATA_DIR.mkdir(parents=True, exist_ok=True)


# class SpeechService:
#     def __init__(self, recognize_model_path: str, language: str):
#         self.recognizer = Model(recognize_model_path)

#         self.engine = pyttsx3.init()
#         self.engine.setProperty('rate', 150)
#         self.engine.setProperty('volume', 1)
#         self.engine.setProperty('voice', language)

#     async def transcribe_audio(self, file: UploadFile) -> str:
#         file_location = DATA_DIR / f"temp_{file.filename}"

#         with open(file_location, "wb") as f:
#             f.write(await file.read())

#         wf = wave.open(str(file_location), "rb")
#         if wf.getsampwidth() != 2:
#             raise ValueError("Audio file must be 16-bit mono")

#         os.remove(str(file_location))

#         recognizer = KaldiRecognizer(self.recognizer, wf.getframerate())

#         while True:
#             data = wf.readframes(4000)
#             if len(data) == 0:
#                 break
#             recognizer.AcceptWaveform(data)

#         final_result = json.loads(recognizer.FinalResult())
#         return final_result.get("text", "")

#     async def text_to_speech(self, text: str, filename: str) -> str:
#         path_to_file = DATA_DIR / filename

#         self.engine.save_to_file(text, str(path_to_file))
#         self.engine.runAndWait()

#         return str(path_to_file)
