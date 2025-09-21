# --- Edge TTS + Whisper Flask Server ---

import edge_tts
import asyncio
import io
import sys
import nest_asyncio
import tempfile
from pathlib import Path

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import whisper
import soundfile as sf
import numpy as np

# Apply nest_asyncio to allow running asyncio within Flask's sync context smoothly
nest_asyncio.apply()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- Configuration ---
FIXED_VOICE = "en-US-JennyNeural"
OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"
OUTPUT_MIMETYPE = "audio/mpeg"
OUTPUT_EXTENSION = "mp3"
# --- End Configuration ---

# --- Load Whisper model once at startup ---
print("[init] Loading Whisper model: small")
whisper_model = whisper.load_model("small")

# --- Helper: Edge TTS ---
async def generate_speech_data(text: str, voice: str):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate='+0%', volume='+0%')
    audio_data = b""
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
    except Exception as e:
        print(f"Error during edge-tts streaming: {e}", file=sys.stderr)
        raise
    return audio_data

# --- Routes ---
@app.route('/')
def index():
    return f"Flask Server running. Endpoints: /tts (TTS), /stt (STT). Fixed voice: {FIXED_VOICE}"

@app.route('/tts', methods=['POST'])
def tts():
    """Text-to-Speech endpoint using a fixed voice."""
    try:
        data = request.json
        text = data.get('text', '')

        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400

        audio_bytes = asyncio.run(generate_speech_data(text, FIXED_VOICE))
        if not audio_bytes:
            return jsonify({'error': 'Audio generation failed'}), 500

        buffer = io.BytesIO(audio_bytes)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype=OUTPUT_MIMETYPE,
            as_attachment=False,
            download_name=f'speech.{OUTPUT_EXTENSION}'
        )
    except Exception as e:
        return jsonify({'error': f'Failed to generate speech: {str(e)}'}), 500

@app.route('/stt', methods=['POST'])
def stt():
    """Speech-to-Text endpoint using Whisper."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        audio_file = request.files["file"]

        # Save to temp WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            wav_path = Path(tf.name)
            audio_file.save(wav_path)

        # Transcribe
        print(f"[stt] Transcribing {wav_path}")
        result = whisper_model.transcribe(str(wav_path), language="en")
        text = (result.get("text") or "").strip()

        try:
            wav_path.unlink(missing_ok=True)
        except Exception:
            pass

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": f"STT failed: {str(e)}"}), 500

# --- Run the App ---
if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Using fixed voice: {FIXED_VOICE}")
    print("Endpoints:")
    print("  GET  /")
    print("  POST /tts  (Body: {'text': '...'})")
    print("  POST /stt  (FormData: file=<audio>)")
    app.run(debug=True, host='0.0.0.0', port=5001)
