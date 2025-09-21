// --- Chat Functions ---
async function handleUserMessage(userText) {
    const message = (userText || "").trim();
    if (!message) return;

    OLLAMA_API_BASE_URL = ollamaServerUrlInput.value.trim() || 'http://localhost:11434';
    OLLAMA_MODEL_NAME = ollamaModelInput.value.trim() || 'llama3:8b';

    // Show user message in chat
    addChatMessage(message, 'user');
    conversationHistory.push({ role: "user", content: message });

    if (sendButton) sendButton.style.display = 'none';
    if (stopButton) {
        stopButton.style.display = 'inline-block';
        stopButton.disabled = false;
    }
    if (userInput) userInput.disabled = true;
    if (typeof updateStatus === 'function') updateStatus('Asking Ollama...');

    // Build messages for Ollama
    let messagesForOllama = [];
    if (activeSystemPrompt && activeSystemPrompt.trim() !== "") {
        messagesForOllama.push({ role: "system", content: activeSystemPrompt });
    }
    messagesForOllama.push(...conversationHistory);

    // Start streaming response
    await streamOllamaResponse(messagesForOllama);
}

// Expose globally for voice.js
window.handleUserMessage = handleUserMessage;

async function sendMessageToOllama() {
    const userMessage = userInput.value.trim();
    userInput.value = "";
    await handleUserMessage(userMessage);
}

// --- Streaming logic split out ---
async function streamOllamaResponse(messagesForOllama) {
    abortController = new AbortController();
    let accumulatedResponse = "";
    let botMessageElement = null;
    let errorOccurred = null;

    try {
        const response = await fetch(`${OLLAMA_API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: OLLAMA_MODEL_NAME,
                messages: messagesForOllama,
                stream: true,
            }),
            signal: abortController.signal,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: "Unknown error" }));
            throw new Error(`Ollama API Error: ${response.status} - ${errorData.error || "No details"}`);
        }

        if (typeof updateStatus === 'function') updateStatus('Receiving response...');
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const jsonResponses = chunk.split('\n').filter(line => line.trim() !== '');

            for (const jsonResponse of jsonResponses) {
                try {
                    const parsed = JSON.parse(jsonResponse);
                    if (parsed.message && parsed.message.content) {
                        accumulatedResponse += parsed.message.content;
                        if (!botMessageElement) {
                            botMessageElement = addChatMessage(accumulatedResponse, 'bot', true);
                        } else {
                            const contentWrapper = botMessageElement.querySelector('.message-content-wrapper');
                            if (contentWrapper) {
                                contentWrapper.innerHTML = renderContentToHtml(accumulatedResponse);
                            }
                        }
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    }
                    if (parsed.done) {
                        await reader.cancel();
                    }
                } catch (e) {
                    console.warn("[Chat.js] Error parsing JSON chunk:", e, "Chunk:", jsonResponse);
                }
            }
        }

        if (botMessageElement) {
            botMessageElement.classList.remove('streaming');
        }
    } catch (error) {
        errorOccurred = error;
        addChatMessage(`Error: ${error.message}`, 'bot');
    } finally {
        abortController = null;
        if (accumulatedResponse || errorOccurred) {
            conversationHistory.push({
                role: "assistant",
                content: accumulatedResponse || `Error: ${errorOccurred.message}`
            });
        }

        if (sendButton) sendButton.style.display = 'inline-block';
        if (stopButton) {
            stopButton.style.display = 'none';
            stopButton.disabled = true;
        }
        if (userInput) userInput.disabled = false;

        if (typeof updateStatus === 'function') {
            updateStatus(errorOccurred ? 'Error with Ollama.' : 'Ready for input.');
        }
    }
}
