from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.core.config import settings
from app.schemas.audio import TranscriptionResponse, AcousticMetricsResponse, AudioPipelineResponse
from app.services.transcription import transcription_service
from app.services.acoustic import acoustic_service

router = APIRouter()

def validate_audio_file(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '{ext}'. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    return ext

@router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model": settings.WHISPER_MODEL
    }

@router.post("/transcribe", response_model=TranscriptionResponse, tags=["AI Speech"])
async def transcribe_audio(file: UploadFile = File(...)):
    # Transcribe spoken audio to text with timestamps using OpenAI Whisper
    validate_audio_file(file)
    content = await file.read()
    
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File size exceeds maximum allowed limit.")

    result = transcription_service.transcribe(content, file.filename)
    return result

@router.post("/analyze", response_model=AcousticMetricsResponse, tags=["Acoustic DSP"])
async def analyze_acoustics(file: UploadFile = File(...)):
    # Extract acoustic metrics (pitch, tempo, silence, spectral centroid) with Librosa
    validate_audio_file(file)
    content = await file.read()
    
    try:
        metrics = acoustic_service.analyze(content)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing error: {str(e)}")

@router.post("/pipeline", response_model=AudioPipelineResponse, tags=["Unified Pipeline"])
async def full_pipeline(file: UploadFile = File(...)):
    # Execute end-to-end processing: Transcription + Acoustic Digital Signal Analysis
    validate_audio_file(file)
    content = await file.read()
    
    transcription = transcription_service.transcribe(content, file.filename)
    metrics = acoustic_service.analyze(content)

    return {
        "filename": file.filename,
        "file_size_bytes": len(content),
        "transcription": transcription,
        "acoustic_metrics": metrics
    }
