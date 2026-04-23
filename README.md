# Multimodal AI Assistant

Real-time multimodal AI assistant combining gesture recognition, voice commands,
web automation, and intelligent response generation.

## Architecture

- **Async Python 3.10+** with an **EventBus pub/sub** backbone.
- Each capability is encapsulated in an independent **Agent**.

### Agents

| Agent | Stack | Role |
|-------|-------|------|
| GestureAgent | OpenCV + MediaPipe | Hand gesture detection |
| SpeechAgent | PyAudio + Whisper | Voice command capture |
| IntentParser | regex + Claude API | Command understanding |
| ActionAgent | Playwright + pyautogui | Browser & desktop control |
| CrawlerAgent | requests + BeautifulSoup + Claude | Web summarization |
| TTSAgent | pyttsx3 | Text-to-speech output |
| FusionAgent | — | Merges gesture + speech into unified actions |

## Quick Start

```bash
# 1. Clone & enter
cd multimodal_assistant

# 2. Create virtualenv
python -m venv .venv && .venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Set up env vars
copy .env.example .env   # then fill in your keys

# 5. Run
python main.py
```

## Testing

```bash
pytest tests/
```
