import io
import soundfile as sf
import librosa
import numpy as np
from typing import Dict, Any

class AcousticService:
    @staticmethod
    def analyze(file_bytes: bytes) -> Dict[str, Any]:
        # Load audio from memory buffer
        data, sr = sf.read(io.BytesIO(file_bytes))
        
        # Convert stereo to mono if necessary
        if data.ndim > 1:
            y = np.mean(data, axis=1)
        else:
            y = data

        duration = float(librosa.get_duration(y=y, sr=sr))

        # 1. Pitch estimation (Fundamental frequency F0 using YIN algorithm)
        f0 = librosa.yin(y, fmin=50, fmax=400, sr=sr)
        valid_f0 = f0[~np.isnan(f0)]
        pitch_mean = float(np.mean(valid_f0)) if len(valid_f0) > 0 else 0.0

        # 2. Spectral Centroid (indicates brightness/timbre of audio)
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        centroid_mean = float(np.mean(spec_centroid))

        # 3. RMS Energy & Silence percentage
        rms = librosa.feature.rms(y=y)
        rms_mean = float(np.mean(rms))
        silence_threshold = 0.01
        silence_frames = np.sum(rms < silence_threshold)
        total_frames = max(len(rms[0]), 1)
        silence_ratio = float((silence_frames / total_frames) * 100)

        # 4. Tempo estimation (beats per minute)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

        return {
            "duration_seconds": round(duration, 2),
            "sample_rate": sr,
            "tempo_bpm": round(tempo_bpm, 1),
            "pitch_mean_hz": round(pitch_mean, 1),
            "spectral_centroid_hz": round(centroid_mean, 1),
            "silence_percentage": round(silence_ratio, 1),
            "rms_energy_mean": round(rms_mean, 4),
        }

acoustic_service = AcousticService()
