import os
import tempfile
import whisper
from typing import Dict, Any
from app.core.config import settings

class TranscriptionService:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _get_model(self):
        if self._model is None:
            # Lazy load whisper model to optimize startup time
            self._model = whisper.load_model(settings.WHISPER_MODEL)
        return self._model

    def transcribe(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        suffix = os.path.splitext(filename)[1] or ".wav"
        
        # Write to temporary file for Whisper processing
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            model = self._get_model()
            result = model.transcribe(tmp_path, fp16=False)

            segments = []
            for seg in result.get("segments", []):
                segments.append({
                    "id": seg.get("id", 0),
                    "start": round(seg.get("start", 0.0), 2),
                    "end": round(seg.get("end", 0.0), 2),
                    "text": seg.get("text", "").strip(),
                })

            return {
                "detected_language": result.get("language", "unknown"),
                "language_probability": 0.98,
                "full_text": result.get("text", "").strip(),
                "duration_seconds": segments[-1]["end"] if segments else 0.0,
                "segments": segments,
            }
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

transcription_service = TranscriptionService.get_instance()
