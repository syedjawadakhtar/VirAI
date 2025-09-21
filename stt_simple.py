from flask import Flask, request, jsonify
from flask_cors import CORS
import time

# Simple STT server for MVP testing
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Simple STT Server for MVP Testing"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Mock STT endpoint for testing - returns simulated transcription"""
    print("Request received for /transcribe")
    try:
        # Check if audio file is in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400

        # Read audio data to verify it was sent
        audio_data = audio_file.read()
        print(f"Received {len(audio_data)} bytes of audio data")

        # Simulate processing time
        time.sleep(1)

        # Mock transcription - in a real implementation, this would use Whisper
        mock_transcription = "Hello, I would like to order a poke bowl please"

        print(f"Mock transcription: {mock_transcription}")

        return jsonify({
            'success': True,
            'transcription': mock_transcription
        })

    except Exception as e:
        error_message = f'Failed to transcribe audio: {str(e)}'
        print(error_message)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    print("Starting Simple STT Flask server for MVP...")
    print("Available endpoints:")
    print("  GET  /")
    print("  POST /transcribe  (multipart/form-data with 'audio' file)")
    app.run(debug=True, host='0.0.0.0', port=5002)