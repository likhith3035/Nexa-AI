# ── Multimodal AI Assistant ─────────────────────────────────────────────
# Base: Python 3.11 slim (Debian Bookworm)
FROM python:3.11-slim-bookworm

# ── System dependencies ──────────────────────────────────────────────────
# - libportaudio2 / portaudio19-dev  → PyAudio
# - espeak / espeak-ng               → pyttsx3 TTS engine
# - libgl1 / libglib2.0-0            → OpenCV headless
# - ffmpeg                           → Whisper audio decoding
# - curl                             → Playwright browser install helper
RUN apt-get update && apt-get install -y --no-install-recommends \
        portaudio19-dev \
        libportaudio2 \
        espeak \
        espeak-ng \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        ffmpeg \
        curl \
        alsa-utils \
        libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ────────────────────────────────────────────────────
WORKDIR /app

# ── Python dependencies ──────────────────────────────────────────────────
# Copy requirements first to leverage layer caching
COPY requirements.txt .

# Use opencv-python-headless instead of opencv-python (no GUI needed in container)
RUN pip install --no-cache-dir --upgrade pip \
    && sed 's/opencv-python>=/opencv-python-headless>=/g' requirements.txt \
       | pip install --no-cache-dir -r /dev/stdin

# ── Playwright browsers ──────────────────────────────────────────────────
RUN playwright install --with-deps chromium

# ── Application source ───────────────────────────────────────────────────
COPY . .

# ── Runtime ─────────────────────────────────────────────────────────────
# Unbuffered output so logs appear immediately
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["python", "main.py"]
