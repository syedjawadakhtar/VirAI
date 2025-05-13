# --- Edge TTS Flask App (Fixed Voice) ---

import edge_tts
import asyncio
import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import sys
import nest_asyncio # Required to run asyncio within Flask's sync context smoothly

# Apply nest_asyncio to allow running asyncio event loops within another
nest_asyncio.apply()

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Configuration ---
# Hardcode the desired "smoothing" female English voice
# Options like en-US-AriaNeural, en-US-JennyNeural, en-GB-SoniaNeural are good candidates.
FIXED_VOICE = "en-US-JennyNeural"
# Output format (MP3 is common and works well for streaming)
OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"
OUTPUT_MIMETYPE = "audio/mpeg"
OUTPUT_EXTENSION = "mp3"
# --- End Configuration ---


# --- Helper function to run async code from sync Flask route ---
async def generate_speech_data(text: str, voice: str):
    """
    Asynchronously generates speech data using edge-tts for a fixed voice.
    """
    # Use the globally defined FIXED_VOICE
    communicate = edge_tts.Communicate(text=text, voice=voice, rate='+0%', volume='+0%')
    audio_data = b""
    try:
        # Use stream() to get audio chunks and concatenate them
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
            elif chunk["type"] == "WordBoundary":
                pass # Word boundary info ignored for basic audio generation
    except Exception as e:
        print(f"Error during edge-tts streaming: {e}", file=sys.stderr)
        raise # Re-raise to be caught by the Flask route handler
    return audio_data

# --- Flask Routes ---

@app.route('/')
def index():
    """Basic index route to confirm the server is running."""
    return f"Edge TTS Flask Server is running. Use POST /tts. Voice is fixed to {FIXED_VOICE}."

# Removed the /voices endpoint as voice selection is disabled

@app.route('/tts', methods=['POST'])
def tts():
    """Text-to-Speech endpoint using a fixed voice."""
    print("Request received for /tts")
    try:
        data = request.json
        text = data.get('text', '')

        if not text or not text.strip():
            print("Error: No text provided", file=sys.stderr)
            return jsonify({'error': 'No text provided'}), 400

        print(f"Generating speech using FIXED voice: {FIXED_VOICE}")

        # Run the async speech generation function using the fixed voice
        # This blocks the current Flask worker until completion
        audio_bytes = asyncio.run(generate_speech_data(text, FIXED_VOICE))

        if not audio_bytes:
             print("Error: Audio generation failed (empty result)", file=sys.stderr)
             return jsonify({'error': 'Audio generation failed (empty result)'}), 500

        # Create an in-memory buffer
        buffer = io.BytesIO(audio_bytes)
        buffer.seek(0)

        print(f"Successfully generated {len(audio_bytes)} bytes of audio.")

        return send_file(
            buffer,
            mimetype=OUTPUT_MIMETYPE,
            as_attachment=False, # Try to play in browser
            download_name=f'speech.{OUTPUT_EXTENSION}' # Filename for download
        )

    except Exception as e:
        error_message = f'Failed to generate speech: {str(e)}'
        print(error_message, file=sys.stderr)
        # Specific error handling can still be useful even without voice selection
        return jsonify({'error': error_message}), 500

# --- Run the App ---
if __name__ == '__main__':
    print("Starting Edge TTS Flask server...")
    print(f"Using fixed voice: {FIXED_VOICE}")
    print("Available endpoints:")
    print("  GET  /")
    print("  POST /tts  (Body: {'text': '...'})")
    # Use a different port if running simultaneously with other apps
    app.run(debug=True, host='0.0.0.0', port=5001)