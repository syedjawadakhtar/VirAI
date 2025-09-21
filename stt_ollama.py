import tempfile
from pathlib import Path
import io

import numpy as np
import soundfile as sf
import whisper
from flask import Flask, request, jsonify
from flask_cors import CORS

# ----------- Configuration -----------
WHISPER_MODEL = "small"  # Default model
SAMPLE_RATE = 16000
LANGUAGE = "en"

# ----------- Flask App Setup -----------
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# ----------- Load Whisper once -----------
print(f"[init] Loading Whisper model: {WHISPER_MODEL}")
whisper_model = whisper.load_model(WHISPER_MODEL)

def transcribe_audio_data(audio_data: bytes) -> str:
    """
    Transcribe audio data using Whisper.
    """
    try:
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            wav_path = Path(tf.name)
            tf.write(audio_data)

        print(f"[stt] Transcribing audio data, saved to: {wav_path}")
        result = whisper_model.transcribe(
            str(wav_path),
            language=LANGUAGE
        )
        text = (result.get("text") or "").strip()
        print(f"[stt] => {text}")

        # Clean up temp file
        try:
            wav_path.unlink(missing_ok=True)
        except Exception:
            pass

        return text
    except Exception as e:
        print(f"[stt] Error during transcription: {e}")
        raise

# ----------- Flask Routes -----------

@app.route('/')
def index():
    """Basic index route to confirm the server is running."""
    return f"STT Flask Server is running. Use POST /transcribe to upload audio."

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Speech-to-Text endpoint that accepts audio data."""
    print("Request received for /transcribe")
    try:
        # Check if audio file is in request
        if 'audio' not in request.files:
            print("Error: No audio file provided", flush=True)
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        if audio_file.filename == '':
            print("Error: Empty filename", flush=True)
            return jsonify({'error': 'No audio file selected'}), 400

        print(f"Processing audio file: {audio_file.filename}")

        # Read audio data
        audio_data = audio_file.read()

        if not audio_data:
            print("Error: Empty audio data", flush=True)
            return jsonify({'error': 'Empty audio data received'}), 400

        print(f"Received {len(audio_data)} bytes of audio data")

        # Transcribe the audio
        transcribed_text = transcribe_audio_data(audio_data)

        if not transcribed_text:
            print("Warning: Empty transcription result", flush=True)
            return jsonify({'error': 'No speech detected in audio'}), 400

        print(f"Transcription successful: {transcribed_text}")

        return jsonify({
            'success': True,
            'transcription': transcribed_text
        })

    except Exception as e:
        error_message = f'Failed to transcribe audio: {str(e)}'
        print(error_message, flush=True)
        return jsonify({'error': error_message}), 500

# ----------- Run the App -----------
if __name__ == '__main__':
    print("Starting STT Flask server...")
    print(f"Using Whisper model: {WHISPER_MODEL}")
    print("Available endpoints:")
    print("  GET  /")
    print("  POST /transcribe  (multipart/form-data with 'audio' file)")
    # Use port 5002 to avoid conflicts with TTS server on 5001
    app.run(debug=True, host='0.0.0.0', port=5002)
