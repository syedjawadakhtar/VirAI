// voice.js
let mediaRecorder;
let audioChunks = [];

const micButton = document.getElementById('mic-button');
const stopMicButton = document.getElementById('stop-mic-button');

micButton.addEventListener('click', async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Microphone not supported in this browser.');
        return;
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'speech.webm');

            try {
                const response = await fetch('http://localhost:5001/stt', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                console.log('Transcribed text:', result.text);

                // Send transcribed text to chat.js
                if (window.handleUserMessage) {
                    window.handleUserMessage(result.text);
                }
            } catch (err) {
                console.error('STT error:', err);
            }
        };

        mediaRecorder.start();
        micButton.style.display = 'none';
        stopMicButton.style.display = 'inline-block';
        console.log('Recording started...');
    } catch (err) {
        console.error('Error accessing mic:', err);
    }
});

stopMicButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        micButton.style.display = 'inline-block';
        stopMicButton.style.display = 'none';
        console.log('Recording stopped.');
    }
});
