from typing import List, Optional
from pydantic import BaseModel, Field

class WordTimestamp(BaseModel):
    word: str
    start: float
    end: float

class Segment(BaseModel):
    id: int
    start: float
    end: float
    text: str
    words: Optional[List[WordTimestamp]] = None

class TranscriptionResponse(BaseModel):
    detected_language: str
    language_probability: float
    full_text: str
    duration_seconds: float
    segments: List[Segment]

class AcousticMetricsResponse(BaseModel):
    duration_seconds: float
    sample_rate: int
    tempo_bpm: float
    pitch_mean_hz: float
    spectral_centroid_hz: float
    silence_percentage: float
    rms_energy_mean: float

class AudioPipelineResponse(BaseModel):
    filename: str
    file_size_bytes: int
    transcription: TranscriptionResponse
    acoustic_metrics: AcousticMetricsResponse
