# =============================
# api/voice.py
# =============================
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ask", tags=["Voice / STT"])


class VoiceResponse(BaseModel):
    transcribed_text: str
    detected_language: str
    answer: str
    sources: list
    grounded: bool


@router.post("/voice", response_model=VoiceResponse)
async def ask_voice(audio: UploadFile = File(...)):
    """
    Accept a WAV/MP3 audio file, transcribe it via SpeechRecognition,
    then route to the same QA pipeline as /ask.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="SpeechRecognition not installed. Run: pip install SpeechRecognition"
        )

    # Save upload to temp file
    suffix = os.path.splitext(audio.filename)[-1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)

        # Try Tunisian-relevant languages; fall back to English
        transcribed_text = None
        for lang_code in ["fr-FR", "ar-TN", "en-US"]:
            try:
                transcribed_text = recognizer.recognize_google(
                    audio_data, language=lang_code
                )
                break
            except sr.UnknownValueError:
                continue

        if not transcribed_text:
            raise HTTPException(status_code=422, detail="Could not transcribe audio.")

    finally:
        os.unlink(tmp_path)

    # Reuse text QA pipeline
    from api.ask import ask_question, QueryRequest
    result = ask_question(QueryRequest(question=transcribed_text, lang="auto"))

    return VoiceResponse(
        transcribed_text=transcribed_text,
        **result,
    )