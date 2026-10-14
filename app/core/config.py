from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AudioSense AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Model Configuration
    WHISPER_MODEL: str = "base"  # Options: tiny, base, small, medium
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: List[str] = ["wav", "mp3", "m4a", "ogg", "flac"]
    
    # Audio DSP Defaults
    DEFAULT_SAMPLE_RATE: int = 16000
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
