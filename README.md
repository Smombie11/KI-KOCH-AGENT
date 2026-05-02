# 🧑‍🍳 KI-Koch-Assistent

Eine intelligente KI-Koch-Assistenz mit Spracherkennung und Text-to-Speech, powered by Groq API.

## ✨ Features

- 🎤 **Spracherkennung**: Spreche deine Fragen auf Deutsch
- 🔊 **Text-to-Speech**: Höre die Antworten vorgelesen
- ⏸️ **Sprachkontrolle**: Pause, Fortsetzen, Stop Buttons
- 📝 **Chat-Schnittstelle**: Elegante Web-UI mit Markdown-Unterstützung
- 🍳 **Chef-Niveau KI**: Rezepte, Zutaten-Ersatz, Kochschritte

## 🚀 Installation

### 1. Repository klonen
```bash
git clone https://github.com/Smombie11/KI-KOCH-AGENT.git
cd KI-KOCH-AGENT
```

### 2. Virtuelle Umgebung erstellen
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Groq API Key einrichten
1. Öffne `.env` Datei
2. Ersetze `your_groq_api_key_here` mit deinem Groq API Key
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

Kostenlos API Key bekommen: https://groq.com

### 5. App starten
```bash
python app.py
```

Die App läuft dann unter: **http://localhost:5000** 🎉

## 📖 Verwendung

1. **📝 Textmodus**: Gib deine Frage direkt ein
2. **🎤 Sprachmodus**: 
   - Klick auf "🎤 Hier klicken und sprechen"
   - Spreche deine Frage
   - Warte auf automatische Erkennung
   - Klick auf "📤 Senden"
3. **🔊 Höre die Antwort**: Die KI spricht automatisch die Antwort vor
4. **⏸️ Kontrolle**: Pause, Fortsetzen oder Stop während der Sprachausgabe

## 🛠️ Technologie

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **KI-Modell**: Groq API (Llama 3.3-70B)
- **Speech API**: Web Speech Recognition & Speech Synthesis

## 📋 Anforderungen

- Python 3.8+
- Groq API Key
- Browser mit Speech Recognition Support (Chrome, Firefox, Edge, etc.)

## 🐛 Troubleshooting

**"GROQ_API_KEY Umgebungsvariable nicht gesetzt"**
- Überprüfe ob `.env` Datei mit deinem API Key existiert
- Starte die App neu

**Mikrofon funktioniert nicht**
- Browser unterstützt möglicherweise Speech Recognition nicht
- Nutze Text-Input als Alternative

**Stimme wird nicht vorgelesen**
- Browser muss Text-to-Speech unterstützen
- Überprüfe Browser-Einstellungen

## 📄 Lizenz

MIT

## 🤝 Kontakt

GitHub: [@Smombie11](https://github.com/Smombie11)

---

Viel Spaß beim Kochen mit deinem KI-Chef! 🍳✨
