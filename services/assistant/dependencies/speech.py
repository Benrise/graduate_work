from pathlib import Path

from services.speech import SpeechService

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "vosk" / "vosk-model-small-ru-0.22"
TTS_MODEL_NAME = 'TeraTTS/natasha-g2p-vits'


def get_speech_service():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at path: {MODEL_PATH}")
    return SpeechService(
        recognize_model_path=str(MODEL_PATH),
        tts_model_name=TTS_MODEL_NAME,
    )
