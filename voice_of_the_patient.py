import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve API Key
GROQ_API_KEY = "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"  #Replace with your API key


if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Please set it in the .env file or environment variables.")

# Define Whisper model
stt_model = "whisper-large-v3"

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """Record audio and save as MP3"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """Transcribe an audio file using Groq's Whisper model"""
    if not os.path.exists(audio_filepath):
        raise FileNotFoundError(f"Audio file '{audio_filepath}' not found.")
    
    client = Groq(api_key=GROQ_API_KEY)
    with open(audio_filepath, "rb") as audio_file:  # Ensures the file is closed properly
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

# Filepath for recorded audio
audio_filepath = "patient_voice_test_for_patient.mp3"

# Uncomment to record new audio
record_audio(audio_filepath)

# Transcribe the recorded audio
try:
    transcription_result = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
    print("Transcription:", transcription_result)
except Exception as e:
    logging.error(f"Error during transcription: {e}")
