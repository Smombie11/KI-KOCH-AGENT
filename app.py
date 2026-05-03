from flask import Flask, render_template_string, request, jsonify
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing")
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

chat_history = []

SYSTEM_PROMPTS = {
    "de": "Du bist eine autonome KI-Koch-Assistenz auf Chef-Niveau.\n\nDeine Aufgaben:\n1. Rezepte erstellen basierend auf Zutaten\n2. Zutaten ersetzen\n3. Kochschritte detailliert erklären\n4. Sicherheitshinweise geben\n\nAntworte immer strukturiert und präzise auf Deutsch.",
    "en": "You are an autonomous AI cooking assistant at chef level.\n\nYour tasks:\n1. Create recipes based on ingredients\n2. Substitute ingredients\n3. Explain cooking steps in detail\n4. Give safety instructions\n\nAlways answer in a structured and precise manner in English.",
    "ar": "أنت مساعد طبخ ذكي بمستوى طاهٍ محترف.\n\nمهامك:\n1. إنشاء وصفات بناءً على المكونات\n2. استبدال المكونات\n3. شرح خطوات الطهي بالتفصيل\n4. تقديم إرشادات السلامة\n\nأجب دائمًا بطريقة منظمة ودقيقة باللغة العربية."
}

def get_ai_response(user_input, language="de"):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["de"])}] + chat_history[-10:]
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.7, max_tokens=2048)
        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Mehrsprachige UI-Texte
TEXTS = {
    "de": {
        "title": "KI-Koch-Assistent", "subtitle": "🚀 Powered by Gr API",
        "welcome": "Hallo! Ich bin Chef Anatanai. Was darf ich heute für dich kochen? 🍳",
        "micBtn": "🎤 Hier klicken und sprechen", "statusReady": "⚡ Bereit zum Sprechen",
        "voiceLabel": "🎤 Erkannt:", "sendVoice": "📤 Diesen Text an KI senden",
        "textPlaceholder": "📝 Schreibe deine Frage hier...", "sendText": "📤 Senden",
        "clearChat": "🗑️ Chat löschen", "footer": "🎤 1. Mikrofon klicken → 2. Sprechen → 3. Pausieren → 4. Auf \"Senden\" klicken",
        "recording": "🔴 Aufnahme läuft... (Pause zum Stoppen)", "speakNow": "🎤 Sprich jetzt...",
        "recognized": "✅ Text erkannt! Klicke auf \"Senden\"", "micError": "❌ Browser unterstützt kein Mikrofon",
        "errorComm": "Fehler bei der Kommunikation mit der KI"
    },
    "en": {
        "title": "AI Cooking Assistant", "subtitle": "🚀 Powered by Gr API",
        "welcome": "Hello! I'm Chef Anatanai. What would you like me to cook for you today? 🍳",
        "micBtn": "🎤 Click and speak", "statusReady": "⚡ Ready to speak",
        "voiceLabel": "🎤 Recognized:", "sendVoice": "📤 Send this text to AI",
        "textPlaceholder": "📝 Type your question here...", "sendText": "📤 Send",
        "clearChat": "🗑️ Clear chat", "footer": "🎤 1. Click mic → 2. Speak → 3. Pause → 4. Click \"Send\"",
        "recording": "🔴 Recording... (Pause to stop)", "speakNow": "🎤 Speak now...",
        "recognized": "✅ Text recognized! Click \"Send\"", "micError": "❌ Browser does not support microphone",
        "errorComm": "Error communicating with AI"
    },
    "ar": {
        "title": "مساعد الطبخ الذكي", "subtitle": "🚀 مدعوم من Gr API",
        "welcome": "مرحبًا! أنا الشيف اناطاليا. ماذا تحب أن أطبخ لك اليوم؟ 🍳",
        "micBtn": "🎤 انقر وتحدث", "statusReady": "⚡ جاهز للتحدث",
        "voiceLabel": "🎤 تم التعرف على:", "sendVoice": "📤 إرسال هذا النص إلى الذكاء الاصطناعي",
        "textPlaceholder": "📝 اكتب سؤالك هنا...", "sendText": "📤 إرسال",
        "clearChat": "🗑️ مسح المحادثة", "footer": "🎤 1. انقر على الميكروفون → 2. تحدث → 3. توقف مؤقت → 4. انقر على \"إرسال\"",
        "recording": "🔴 جاري التسجيل... (توقف مؤقت للإيقاف)", "speakNow": "🎤 تحدث الآن...",
        "recognized": "✅ تم التعرف على النص! انقر على \"إرسال\"", "micError": "❌ المتصفح لا يدعم الميكروفون",
        "errorComm": "خطأ في الاتصال بالذكاء الاصطناعي"
    }
}
TEXTS_JSON = json.dumps(TEXTS, ensure_ascii=False)

IMPORT_MAP = json.dumps({
    "imports": {
        "three": "https://unpkg.com/three@0.168.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.168.0/examples/jsm/",
        "@pixiv/three-vrm": "https://unpkg.com/@pixiv/three-vrm@3.3.4/lib/three-vrm.module.js"
    }
})

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KI-Koch-Assistent</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <!-- Import Map für Three.js + Addons + VRM -->
    <script type="importmap">
    {IMPORT_MAP}
    </script>

    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Segoe UI', 'Noto Sans Arabic', sans-serif; background: linear-gradient(135deg,#121212,#1e1e1e); color:#fff; padding:20px; }}
        .container {{ max-width:1000px; margin:0 auto; }}
        .header {{ text-align:center; margin-bottom:30px; position:relative; }}
        .language-selector {{ position:absolute; top:0; right:0; background:#2d2d2d; padding:8px 12px; border-radius:30px; }}
        .language-selector select {{ background:#1e1e1e; color:white; border:1px solid #4CAF50; border-radius:20px; padding:5px 10px; cursor:pointer; }}
        .avatar-3d {{
            width: 100%;
            max-width: 500px;
            height: 600px;
            margin: 0 auto 20px;
            border-radius: 25px;
            overflow: hidden;
            background: linear-gradient(135deg, #0a0a0a 0%, #1e1e1e 100%);
            box-shadow: 0 0 30px rgba(76,175,80,0.5), inset 0 0 20px rgba(0,0,0,0.5);
            border: 2px solid #4CAF50;
        }}
        #avatarCanvas {{
            width: 100%;
            height: 100%;
            display: block;
            image-rendering: crisp-edges;
        }}
        h1 {{ font-size:2rem; background:linear-gradient(135deg,#4CAF50,#2196F3); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        .chat-container {{ background:#2d2d2d; border-radius:15px; height:400px; overflow-y:auto; padding:20px; margin-bottom:20px; }}
        .message {{ margin-bottom:15px; display:flex; }}
        .message.user {{ justify-content:flex-end; }}
        .message.assistant {{ justify-content:flex-start; }}
        .message-content {{ max-width:70%; padding:12px 18px; border-radius:20px; line-height:1.6; }}
        .message.user .message-content {{ background:#4CAF50; color:white; border-bottom-right-radius:5px; }}
        .message.assistant .message-content {{ background:#3a3a3a; }}
        .rtl .message-content {{ direction:rtl; text-align:right; }}
        .mic-container, .input-container {{ background:#2d2d2d; border-radius:15px; padding:20px; margin-bottom:20px; }}
        .mic-btn {{ background:#4CAF50; color:white; border:none; border-radius:60px; padding:15px; font-size:18px; font-weight:bold; width:100%; cursor:pointer; transition:0.3s; }}
        .mic-btn.recording {{ background:#f44336; animation:pulse 1s infinite; }}
        @keyframes pulse {{ 0% {{ transform:scale(1); }} 50% {{ transform:scale(1.02); }} 100% {{ transform:scale(1); }} }}
        .status {{ text-align:center; margin-top:15px; color:#aaa; }}
        .voice-text {{ background:#1e1e1e; border-radius:10px; padding:15px; margin-top:15px; display:none; }}
        .voice-text.show {{ display:block; }}
        .voice-text-label {{ color:#4CAF50; margin-bottom:10px; }}
        .voice-text-content {{ background:#2d2d2d; padding:12px; border-radius:8px; margin-bottom:15px; }}
        .send-btn, .send-text-btn, .clear-btn {{ border:none; border-radius:30px; padding:12px 24px; font-weight:bold; cursor:pointer; }}
        .send-btn {{ background:#2196F3; color:white; width:100%; }}
        .send-text-btn {{ background:#4CAF50; color:white; }}
        .clear-btn {{ background:#dc3545; color:white; }}
        .input-group {{ display:flex; gap:10px; }}
        .text-input {{ flex:1; padding:12px; background:#1e1e1e; border:1px solid #4CAF50; border-radius:30px; color:white; }}
        .speech-controls {{ display:flex; gap:10px; margin-top:15px; }}
        .speech-btn {{ flex:1; padding:10px; border:none; border-radius:25px; color:white; font-weight:bold; cursor:pointer; }}
        .pause-btn {{ background:#FFA500; }}
        .resume-btn {{ background:#2196F3; }}
        .stop-btn {{ background:#f44336; }}
        .footer {{ text-align:center; margin-top:20px; color:#666; font-size:12px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="language-selector">
            <label>🌐 </label>
            <select id="langSelect">
                <option value="de">Deutsch</option>
                <option value="en">English</option>
                <option value="ar">العربية</option>
            </select>
        </div>
        <div class="avatar-3d">
            <canvas id="avatarCanvas"></canvas>
        </div>
        <h1 id="mainTitle">KI-Koch-Assistent</h1>
        <p id="subtitle">🚀 Powered by Groq API</p>
    </div>
    <div class="chat-container" id="chatContainer">
        <div class="message assistant"><div class="message-content" id="welcomeMsg">Hallo! Ich bin Chef Antonio. Was darf ich heute für dich kochen? 🍳</div></div>
    </div>
    <div class="mic-container">
        <button class="mic-btn" id="micBtn">🎤 Hier klicken und sprechen</button>
        <div class="status" id="status">⚡ Bereit zum Sprechen</div>
        <div class="voice-text" id="voiceText">
            <div class="voice-text-label" id="voiceLabel">🎤 Erkannt:</div>
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
        <div class="speech-controls" id="speechControls" style="display:none;">
            <button class="speech-btn pause-btn" onclick="pauseSpeech()">⏸️ Pause</button>
            <button class="speech-btn resume-btn" onclick="resumeSpeech()">▶️ Fortsetzen</button>
            <button class="speech-btn stop-btn" onclick="stopSpeech()">⏹️ Stop</button>
        </div>
    </div>
    <div class="footer" id="footer">🎤 1. Mikrofon klicken → 2. Sprechen → 3. Pausieren → 4. Auf "Senden" klicken</div>
</div>

<script>
    const texts = {TEXTS_JSON};
    let currentLang = "de";
    let recognition = null, isRecording = false, finalTranscript = "", silenceTimeout = null;
    let isSpeaking = false, isPaused = false;
    let currentUtterance = null;

    const langSelect = document.getElementById('langSelect');
    const mainTitle = document.getElementById('mainTitle');
    const subtitle = document.getElementById('subtitle');
    const welcomeMsgDiv = document.getElementById('welcomeMsg');
    const micBtn = document.getElementById('micBtn');
    const statusDiv = document.getElementById('status');
    const voiceTextDiv = document.getElementById('voiceText');
    const recognizedTextDiv = document.getElementById('recognizedText');
    const sendVoiceBtn = document.getElementById('sendVoiceBtn');
    const textInput = document.getElementById('textInput');
    const sendTextBtn = document.getElementById('sendTextBtn');
    const clearBtn = document.getElementById('clearBtn');
    const chatContainer = document.getElementById('chatContainer');
    const voiceLabel = document.getElementById('voiceLabel');
    const footer = document.getElementById('footer');

    function updateUILanguage() {{
        const t = texts[currentLang];
        if (!t) return;
        mainTitle.innerText = t.title;
        subtitle.innerText = t.subtitle;
        welcomeMsgDiv.innerText = t.welcome;
        micBtn.innerText = t.micBtn;
        statusDiv.innerText = t.statusReady;
        voiceLabel.innerText = t.voiceLabel;
        sendVoiceBtn.innerText = t.sendVoice;
        textInput.placeholder = t.textPlaceholder;
        sendTextBtn.innerText = t.sendText;
        clearBtn.innerText = t.clearChat;
        footer.innerText = t.footer;
        if (currentLang === 'ar') document.body.classList.add('rtl');
        else document.body.classList.remove('rtl');
    }}

    langSelect.addEventListener('change', (e) => {{
        currentLang = e.target.value;
        updateUILanguage();
        if (chatContainer.children.length === 1) welcomeMsgDiv.innerText = texts[currentLang].welcome;
        if (recognition) {{
            const langMap = {{"de":"de-DE","en":"en-US","ar":"ar-EG"}};
            recognition.lang = langMap[currentLang];
        }}
    }});

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {{
        statusDiv.innerText = texts[currentLang].micError;
        micBtn.disabled = true;
    }}

    async function sendMessage(message, isVoice = false) {{
        try {{
            const resp = await fetch('/api/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{message: message, language: currentLang}})
            }});
            const data = await resp.json();
            addMessage(message, 'user');
            addMessage(data.response, 'assistant');
            speak(data.response);
            document.getElementById('speechControls').style.display = 'flex';
            if (isVoice) {{
                voiceTextDiv.classList.remove('show');
                finalTranscript = "";
            }}
            textInput.value = '';
        }} catch(e) {{
            addMessage(texts[currentLang].errorComm, 'assistant');
        }}
    }}

    function addMessage(text, sender) {{
        const div = document.createElement('div');
        div.className = `message ${{sender}}`;
        let content = sender === 'assistant' ? marked.parse(text) : escapeHtml(text);
        div.innerHTML = `<div class="message-content">${{content}}</div>`;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }}

    function escapeHtml(str) {{
        return str.replace(/[&<>]/g, function(m) {{
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        }});
    }}

    function speak(text) {{
        if (!window.speechSynthesis) return;
        if (currentUtterance) {{
            window.speechSynthesis.cancel();
            currentUtterance = null;
        }}
        isSpeaking = true;
        isPaused = false;
        const langMap = {{"de":"de-DE","en":"en-US","ar":"ar-EG"}};
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = langMap[currentLang];
        utterance.rate = 0.85;
        utterance.onstart = () => {{
            if (window.startAvatarVideo) window.startAvatarVideo();
        }};
        utterance.onend = () => {{
            isSpeaking = false;
            isPaused = false;
            currentUtterance = null;
            if (window.stopAvatarVideo) window.stopAvatarVideo();
            updateSpeechButtons();
        }};
        currentUtterance = utterance;
        window.speechSynthesis.speak(utterance);
        updateSpeechButtons();
    }}

    window.pauseSpeech = function() {{
        if (window.speechSynthesis && window.speechSynthesis.speaking && !isPaused) {{
            window.speechSynthesis.pause();
            isPaused = true;
            if (window.pauseAvatarVideo) window.pauseAvatarVideo();
            updateSpeechButtons();
        }}
    }};

    window.resumeSpeech = function() {{
        if (window.speechSynthesis && isPaused) {{
            window.speechSynthesis.resume();
            isPaused = false;
            if (window.resumeAvatarVideo) window.resumeAvatarVideo();
            updateSpeechButtons();
        }}
    }};

    window.stopSpeech = function() {{
        if (window.speechSynthesis) {{
            window.speechSynthesis.cancel();
            isSpeaking = false;
            isPaused = false;
            currentUtterance = null;
            if (window.stopAvatarVideo) window.stopAvatarVideo();
            updateSpeechButtons();
        }}
    }};

    function updateSpeechButtons() {{
        const pauseBtn = document.getElementById('pauseBtn');
        const resumeBtn = document.getElementById('resumeBtn');
        const stopBtn = document.getElementById('stopBtn');
        if (pauseBtn && resumeBtn && stopBtn) {{
            if (isSpeaking && !isPaused) {{
                pauseBtn.style.display = 'inline-block';
                resumeBtn.style.display = 'none';
                stopBtn.style.display = 'inline-block';
            }} else if (isPaused) {{
                pauseBtn.style.display = 'none';
                resumeBtn.style.display = 'inline-block';
                stopBtn.style.display = 'inline-block';
            }} else {{
                pauseBtn.style.display = 'none';
                resumeBtn.style.display = 'none';
                stopBtn.style.display = 'none';
            }}
        }}
    }}

    function startRecording() {{
        if (recognition) try {{ recognition.stop(); }} catch(e) {{}}
        const langMap = {{"de":"de-DE","en":"en-US","ar":"ar-EG"}};
        recognition = new SpeechRecognition();
        recognition.lang = langMap[currentLang];
        recognition.interimResults = true;
        recognition.continuous = true;
        recognition.onstart = () => {{
            isRecording = true;
            finalTranscript = "";
            voiceTextDiv.classList.remove('show');
            micBtn.classList.add('recording');
            micBtn.innerText = texts[currentLang].recording;
            statusDiv.innerText = texts[currentLang].speakNow;
        }};
        recognition.onresult = (event) => {{
            if (silenceTimeout) clearTimeout(silenceTimeout);
            silenceTimeout = setTimeout(() => {{
                if (isRecording && recognition) recognition.stop();
            }}, 1500);
            let interim = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {{
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) finalTranscript += transcript + " ";
                else interim += transcript;
            }}
            if (finalTranscript) statusDiv.innerText = '🎤 ' + finalTranscript.substring(0,60);
            else if (interim) statusDiv.innerText = '🎤 ' + interim;
        }};
        recognition.onend = () => {{
            isRecording = false;
            micBtn.classList.remove('recording');
            micBtn.innerText = texts[currentLang].micBtn;
            if (finalTranscript.trim().length > 0) {{
                recognizedTextDiv.innerText = finalTranscript.trim();
                voiceTextDiv.classList.add('show');
                statusDiv.innerText = texts[currentLang].recognized;
            }} else {{
                statusDiv.innerText = texts[currentLang].statusReady;
            }}
        }};
        recognition.onerror = (e) => {{
            statusDiv.innerText = '❌ ' + e.error;
            isRecording = false;
            micBtn.classList.remove('recording');
            micBtn.innerText = texts[currentLang].micBtn;
        }};
        recognition.start();
    }}

    micBtn.onclick = () => {{
        if (isRecording) recognition?.stop();
        else startRecording();
    }};
    sendVoiceBtn.onclick = () => {{
        if (finalTranscript.trim()) sendMessage(finalTranscript.trim(), true);
    }};
    sendTextBtn.onclick = () => {{
        const msg = textInput.value.trim();
        if (msg) sendMessage(msg);
    }};
    textInput.onkeypress = (e) => {{
        if (e.key === 'Enter') sendTextBtn.click();
    }};
    clearBtn.onclick = async () => {{
        await fetch('/api/clear', {{ method: 'POST' }});
        chatContainer.innerHTML = '';
        const div = document.createElement('div');
        div.className = 'message assistant';
        div.innerHTML = `<div class="message-content">${{texts[currentLang].welcome}}</div>`;
        chatContainer.appendChild(div);
    }};

    updateUILanguage();
</script>

<!-- Lade avatar.js für Video-Avatar -->
<script type="module" src="/static/avatar.js"></script>
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
    language = data.get('language', 'de')
    response = get_ai_response(message, language)
    return jsonify({'response': response})

@app.route('/api/clear', methods=['POST'])
def clear():
    global chat_history
    chat_history = []
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
