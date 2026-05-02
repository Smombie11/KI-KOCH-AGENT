from flask import Flask, render_template_string, request, jsonify
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

app = Flask(__name__)

# ========== GROQ API ==========
# Versuche zuerst Streamlit Secrets (für Cloud-Deployment)
# Falls nicht vorhanden, nutze Umgebungsvariablen (lokal)
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY nicht gesetzt! Lokal: Bitte .env Datei aktualisieren. Cloud: Secrets hinzufügen.")
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# ========== CHAT HISTORY ==========
chat_history = []

SYSTEM_PROMPT = """
Du bist eine autonome KI-Koch-Assistenz auf Chef-Niveau.

Deine Aufgaben:
1. Rezepte erstellen basierend auf Zutaten
2. Zutaten ersetzen
3. Kochschritte detailliert erklären
4. Sicherheitshinweise geben

Antworte immer strukturiert und präzise auf Deutsch.
"""

def get_ai_response(user_input):
    """Holt Antwort von Groq API"""
    global chat_history
    
    chat_history.append({"role": "user", "content": user_input})
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history[-10:]
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )
        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        return f"⚠️ Fehler: {str(e)}"

# ========== HTML TEMPLATE ==========
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>KI-Koch-Assistent</title>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: #4CAF50;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px;
            font-size: 50px;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        h1 {
            font-size: 2rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .chat-container {
            background: #2d2d2d;
            border-radius: 15px;
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.assistant {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
            word-wrap: break-word;
            line-height: 1.6;
        }
        
        .message-content h1,
        .message-content h2,
        .message-content h3,
        .message-content h4,
        .message-content h5,
        .message-content h6 {
            margin-top: 15px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .message-content p {
            margin-bottom: 10px;
        }
        
        .message-content ul,
        .message-content ol {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .message-content li {
            margin-bottom: 5px;
        }
        
        .message-content strong {
            font-weight: bold;
            color: #4CAF50;
        }
        
        .message-content em {
            font-style: italic;
        }
        
        .message-content code {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 3px;
        }
        
        .message.user .message-content {
            background: #4CAF50;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .message.assistant .message-content {
            background: #3a3a3a;
            color: white;
            border-bottom-left-radius: 5px;
        }
        
        .mic-container {
            background: #2d2d2d;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .mic-btn {
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 60px;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }
        
        .mic-btn.recording {
            background: #f44336;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .status {
            text-align: center;
            margin-top: 15px;
            color: #aaa;
            font-size: 14px;
        }
        
        .voice-text {
            background: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
            display: none;
        }
        
        .voice-text.show {
            display: block;
        }
        
        .voice-text-label {
            color: #4CAF50;
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .voice-text-content {
            background: #2d2d2d;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
            word-wrap: break-word;
        }
        
        .send-btn {
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
        }
        
        .input-container {
            background: #2d2d2d;
            border-radius: 15px;
            padding: 20px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
        }
        
        .text-input {
            flex: 1;
            padding: 12px;
            background: #1e1e1e;
            border: 1px solid #4CAF50;
            border-radius: 30px;
            color: white;
            font-size: 14px;
        }
        
        .text-input:focus {
            outline: none;
            border-color: #2196F3;
        }
        
        .send-text-btn {
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 30px;
            padding: 12px 24px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .send-text-btn:hover {
            background: #45a049;
        }
        
        .clear-btn {
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 30px;
            padding: 12px 24px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .clear-btn:hover {
            background: #c82333;
        }
        
        .speech-controls {
            display: flex;
            gap: 10px;
        }
        
        .speech-btn {
            flex: 1;
            padding: 10px 15px;
            border: none;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .pause-btn {
            background: #FFA500;
        }
        
        .pause-btn:hover {
            background: #FF8C00;
        }
        
        .resume-btn {
            background: #2196F3;
        }
        
        .resume-btn:hover {
            background: #1976D2;
        }
        
        .stop-btn {
            background: #f44336;
        }
        
        .stop-btn:hover {
            background: #da190b;
        }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="avatar">🧑‍🍳</div>
            <h1>KI-Koch-Assistent</h1>
            <p>🚀 Powered by Groq API</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message assistant">
                <div class="message-content">
                    Hallo! Ich bin Chef Antonio. Was darf ich heute für dich kochen? 🍳
                </div>
            </div>
        </div>
        
        <div class="mic-container">
            <button class="mic-btn" id="micBtn">🎤 Hier klicken und sprechen</button>
            <div class="status" id="status">⚡ Bereit zum Sprechen</div>
            <div class="voice-text" id="voiceText">
                <div class="voice-text-label">🎤 Erkannt:</div>
                <div class="voice-text-content" id="recognizedText"></div>
                <button class="send-btn" id="sendVoiceBtn">📤 Diesen Text an KI senden</button>
            </div>
        </div>
        
        <div class="input-container">
            <div class="input-group">
                <input type="text" class="text-input" id="textInput" placeholder="📝 Schreibe deine Frage hier...">
                <button class="send-text-btn" id="sendTextBtn">📤 Senden</button>
                <button class="clear-btn" id="clearBtn">🗑️ Chat löschen</button>
            </div>
            <div class="speech-controls" id="speechControls" style="margin-top: 15px; display: none;">
                <button class="speech-btn pause-btn" id="pauseBtn" onclick="pauseSpeech()" style="display: none;">⏸️ Pause</button>
                <button class="speech-btn resume-btn" id="resumeBtn" onclick="resumeSpeech()" style="display: none;">▶️ Fortsetzen</button>
                <button class="speech-btn stop-btn" id="stopBtn" onclick="stopSpeech()" style="display: none;">⏹️ Stop</button>
            </div>
        </div>
        
        <div class="footer">
            🎤 1. Mikrofon klicken → 2. Sprechen → 3. Pausieren → 4. Auf "Senden" klicken
        </div>
    </div>
    
    <script>
        let recognition = null;
        let isRecording = false;
        let finalTranscript = "";
        let silenceTimeout = null;
        let isSpeaking = false;
        let isPaused = false;
        
        const micBtn = document.getElementById('micBtn');
        const statusDiv = document.getElementById('status');
        const voiceTextDiv = document.getElementById('voiceText');
        const recognizedTextDiv = document.getElementById('recognizedText');
        const sendVoiceBtn = document.getElementById('sendVoiceBtn');
        const textInput = document.getElementById('textInput');
        const sendTextBtn = document.getElementById('sendTextBtn');
        const clearBtn = document.getElementById('clearBtn');
        const chatContainer = document.getElementById('chatContainer');
        
        // Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            statusDiv.innerHTML = '❌ Browser unterstützt kein Mikrofon';
            micBtn.disabled = true;
        }
        
        // API calls
        async function sendMessage(message, isVoice = false) {
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                addMessage(message, 'user');
                addMessage(data.response, 'assistant');
                
                // Text-to-Speech
                speak(data.response);
                document.getElementById('speechControls').style.display = 'flex';
                
                if (isVoice) {
                    voiceTextDiv.classList.remove('show');
                    finalTranscript = "";
                }
                
                textInput.value = '';
            } catch (error) {
                console.error('Error:', error);
                addMessage('Fehler bei der Kommunikation mit der KI', 'assistant');
            }
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            let content = text;
            if (sender === 'assistant') {
                // Markdown rendering für Assistent-Nachrichten
                content = marked.parse(text);
            } else {
                content = escapeHtml(text);
            }
            
            messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Text-to-Speech
        function speak(text) {
            if (!window.speechSynthesis) return;
            isSpeaking = true;
            isPaused = false;
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'de-DE';
            utterance.rate = 0.85;
            utterance.onend = () => {
                isSpeaking = false;
                isPaused = false;
                updateSpeechButtons();
            };
            window.speechSynthesis.speak(utterance);
            updateSpeechButtons();
        }
        
        function pauseSpeech() {
            if (window.speechSynthesis && window.speechSynthesis.speaking && !isPaused) {
                window.speechSynthesis.pause();
                isPaused = true;
                updateSpeechButtons();
            }
        }
        
        function resumeSpeech() {
            if (window.speechSynthesis && isPaused) {
                window.speechSynthesis.resume();
                isPaused = false;
                updateSpeechButtons();
            }
        }
        
        function stopSpeech() {
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
                isSpeaking = false;
                isPaused = false;
                updateSpeechButtons();
            }
        }
        
        function updateSpeechButtons() {
            const pauseBtn = document.getElementById('pauseBtn');
            const resumeBtn = document.getElementById('resumeBtn');
            const stopBtn = document.getElementById('stopBtn');
            
            if (isSpeaking && !isPaused) {
                pauseBtn.style.display = 'inline-block';
                resumeBtn.style.display = 'none';
                stopBtn.style.display = 'inline-block';
            } else if (isPaused) {
                pauseBtn.style.display = 'none';
                resumeBtn.style.display = 'inline-block';
                stopBtn.style.display = 'inline-block';
            } else {
                pauseBtn.style.display = 'none';
                resumeBtn.style.display = 'none';
                stopBtn.style.display = 'none';
            }
        }
        
        // Voice recognition
        function startRecording() {
            if (recognition) {
                try { recognition.stop(); } catch(e) {}
            }
            
            recognition = new SpeechRecognition();
            recognition.lang = 'de-DE';
            recognition.interimResults = true;
            recognition.continuous = true;
            
            recognition.onstart = () => {
                isRecording = true;
                finalTranscript = "";
                voiceTextDiv.classList.remove('show');
                micBtn.classList.add('recording');
                micBtn.innerHTML = '🔴 Aufnahme läuft... (Pause zum Stoppen)';
                statusDiv.innerHTML = '🎤 Sprich jetzt...';
            };
            
            recognition.onresult = (event) => {
                startSilenceTimer();
                let interim = "";
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + " ";
                    } else {
                        interim += transcript;
                    }
                }
                
                if (finalTranscript) {
                    statusDiv.innerHTML = '🎤 ' + finalTranscript.substring(0, 60);
                } else if (interim) {
                    statusDiv.innerHTML = '🎤 <i>' + interim.substring(0, 60) + '</i>';
                }
            };
            
            recognition.onend = () => {
                isRecording = false;
                micBtn.classList.remove('recording');
                micBtn.innerHTML = '🎤 Hier klicken und sprechen';
                
                if (finalTranscript.trim().length > 0) {
                    recognizedTextDiv.innerHTML = finalTranscript.trim();
                    voiceTextDiv.classList.add('show');
                    statusDiv.innerHTML = '✅ Text erkannt! Klicke auf "Senden"';
                } else {
                    statusDiv.innerHTML = '⚡ Bereit zum Sprechen';
                }
            };
            
            recognition.onerror = (event) => {
                console.error('Error:', event.error);
                statusDiv.innerHTML = '❌ Fehler: ' + event.error;
                isRecording = false;
                micBtn.classList.remove('recording');
                micBtn.innerHTML = '🎤 Hier klicken und sprechen';
            };
            
            recognition.start();
        }
        
        function startSilenceTimer() {
            if (silenceTimeout) clearTimeout(silenceTimeout);
            silenceTimeout = setTimeout(() => {
                if (isRecording && recognition) {
                    recognition.stop();
                }
            }, 1500);
        }
        
        // Event Listeners
        micBtn.onclick = () => {
            if (isRecording) {
                if (recognition) recognition.stop();
            } else {
                startRecording();
            }
        };
        
        sendVoiceBtn.onclick = () => {
            if (finalTranscript.trim()) {
                sendMessage(finalTranscript.trim(), true);
            }
        };
        
        sendTextBtn.onclick = () => {
            const message = textInput.value.trim();
            if (message) {
                sendMessage(message);
            }
        };
        
        textInput.onkeypress = (e) => {
            if (e.key === 'Enter') {
                sendTextBtn.click();
            }
        };
        
        clearBtn.onclick = async () => {
            await fetch('/api/clear', { method: 'POST' });
            chatContainer.innerHTML = '';
            addMessage('Hallo! Ich bin Chef Antonio. Was darf ich heute für dich kochen? 🍳', 'assistant');
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    response = get_ai_response(message)
    return jsonify({'response': response})

@app.route('/api/clear', methods=['POST'])
def clear():
    global chat_history
    chat_history = []
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
