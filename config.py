"""
Configuration module.

Loads settings from environment variables and .env file.
All API keys and tunables live here as a single Settings dataclass.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# ── Load .env from project root ────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """Immutable application settings populated from environment variables."""

    # ── LLM / Claude ────────────────────────────────────────────────────
    anthropic_api_key: str = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", "")
    )
    claude_model: str = field(
        default_factory=lambda: os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    )

    # ── Gesture agent ───────────────────────────────────────────────────
    gesture_camera_index: int = field(
        default_factory=lambda: int(os.environ.get("GESTURE_CAMERA_INDEX", "0"))
    )
    gesture_confidence: float = field(
        default_factory=lambda: float(os.environ.get("GESTURE_CONFIDENCE", "0.7"))
    )

    # ── Speech agent ────────────────────────────────────────────────────
    whisper_model_size: str = field(
        default_factory=lambda: os.environ.get("WHISPER_MODEL_SIZE", "base")
    )
    audio_sample_rate: int = field(
        default_factory=lambda: int(os.environ.get("AUDIO_SAMPLE_RATE", "16000"))
    )
    audio_chunk_size: int = field(
        default_factory=lambda: int(os.environ.get("AUDIO_CHUNK_SIZE", "1024"))
    )
    silence_threshold: float = field(
        default_factory=lambda: float(os.environ.get("SILENCE_THRESHOLD", "0.03"))
    )
    silence_duration: float = field(
        default_factory=lambda: float(os.environ.get("SILENCE_DURATION", "1.5"))
    )

    # ── Fusion agent ────────────────────────────────────────────────────
    fusion_window_seconds: float = field(
        default_factory=lambda: float(os.environ.get("FUSION_WINDOW_SECONDS", "2.0"))
    )

    # ── TTS agent ───────────────────────────────────────────────────────
    tts_rate: int = field(
        default_factory=lambda: int(os.environ.get("TTS_RATE", "175"))
    )

    # ── Crawler agent ───────────────────────────────────────────────────
    crawler_timeout: int = field(
        default_factory=lambda: int(os.environ.get("CRAWLER_TIMEOUT", "15"))
    )

    # ── Logging ─────────────────────────────────────────────────────────
    log_level: str = field(
        default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO")
    )


# Singleton – import this from anywhere
settings = Settings()
