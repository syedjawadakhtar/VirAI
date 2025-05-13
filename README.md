<div align="center">
  
# HanaVerse 🌸

  
![HanaVerse Banner](https://via.placeholder.com/800x200?text=HanaVerse+-+Chat+with+Ollama)

**An interactive web UI for chatting with Ollama, featuring Hana - a lively 2D anime character**

[![GitHub stars](https://img.shields.io/github/stars/Ashish-Patnaik/HanaVerse?style=social)](https://github.com/Ashish-Patnaik/HanaVerse)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Live2D](https://img.shields.io/badge/Made%20with-Live2D-ff69b4.svg)](https://www.live2d.com/)
[![Made with Ollama](https://img.shields.io/badge/Made%20with-Ollama-blue.svg)](https://ollama.ai/)

• [Features](#features) 
• [Installation](#installation) 
• [Usage](#usage) 
• [Screenshots](#screenshots) 
• [Configuration](#configuration) 
• [Contributing](#contributing)

</div>

## 🌟 Features

- **Interactive Chat Interface**: Talk with Ollama's powerful language models in a friendly web UI
- **Live 2D Animation**: Chat with Hana, an expressive anime character that responds to your interactions
- **Markdown Support**: View beautifully formatted responses with syntax highlighting
- **LaTeX Math Rendering**: Display mathematical equations properly with KaTeX
- **Customizable Settings**: Choose your Ollama model and configure system prompts
- **Responsive Design**: Enjoy HanaVerse on desktop and mobile devices
- **Real-time Response**: Stream responses as they're generated

## 🚀 Installation

### Prerequisites

- Python 3.8+ installed
- [Ollama](https://ollama.ai/) installed and running on your system
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/Ashish-Patnaik/HanaVerse.git
cd HanaVerse
```
### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```
### Step 3: Start the Flask server
```bash
python server.py
```
The server will start running at http://localhost:5000 by default.

### Step 4: Access HanaVerse in your browser
After running the server open index.html in your web browser and accese **HanaVerse**

### 💬 Usage

1. **Start Chatting:** Type your message in the input box and press Send or hit Enter
2. **Change Settings:** Click the hamburger menu (☰) to access settings
3. **Configure Ollama:**

  - Set your Ollama server URL (default: http://localhost:11434)
  - Choose your preferred model (e.g., llama3:8b, codellama:7b, mistral:latest)
  - Customize the system prompt for specialized responses

4. **Stop Generation:** Click the Stop button anytime to halt response generation


## 📸 Screenshots
<div align="center">
  <img src="https://via.placeholder.com/400x300?text=HanaVerse+Screenshot+1" alt="HanaVerse Chat Interface" width="45%">
</div>

## ⚙️ Configuration
### Ollama Models
HanaVerse works with any model available in your Ollama installation. Some recommended models:

- ```llama3:8b``` - Great general purpose assistant (default)
- ```codellama:7b``` - Specialized for coding tasks
- ```mistral:latest``` - Alternative high-quality model
- ```phi3:latest``` - Microsoft's compact but powerful model

## System Prompts
Customize the system prompt to get specialized responses:

1. **Math Helper:** "Format math using LaTeX. Show step-by-step solutions."
2. **Coding Assistant:** "Provide code examples with detailed explanations. Use appropriate syntax highlighting."
3. **Recipe Generator:** "Present ingredients as bullet points and steps as numbered lists."

🔧 Project Structure
```
HanaVerse/
├── server.py              # Flask server for handling API requests
├── index.html          # Main web interface
├── style.css           # CSS styling for the UI
├── script.js           # Core functionality for Live2D character
├── chat.js             # Chat interaction logic
├── sdk/                # Live2D SDK components
├── prism/              # Syntax highlighting library
├── katex/              # Math rendering library
├── models/             # Live2D model files for Hana
└── requirements.txt    # Python dependencies
```

### 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. **Fork the repository**
2. Create your feature branch (```git checkout -b feature/amazing-feature```)
3. Commit your changes (```git commit -m 'Add some amazing feature'```)
4. Push to the branch (```git push origin feature/amazing-feature```)
5. Open a Pull Request

### 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

### 🙏 Acknowledgements

1. Ollama for the local LLM runtime
2. Live2D for the Cubism SDK
3. pixi-live2d-display for the WebGL rendering
4. KaTeX for math rendering
5. Prism for syntax highlighting


<div align="center">
Made with ♥️ by Ashish Patnaik
</div>
