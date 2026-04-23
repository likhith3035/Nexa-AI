"""
Multimodal AI Assistant — Entry Point

Boots up the EventBus, registers all agents, and runs the async
event loop until the user triggers a quit command or Ctrl+C.
"""

from __future__ import annotations

import asyncio
import signal
import sys

from config import settings
from core.event_bus import EventBus
from utils.logger import get_logger

# Agent imports
from agents.gesture_agent import GestureAgent
from agents.speech_agent import SpeechAgent
from agents.fusion_agent import FusionAgent
from agents.intent_parser import IntentParser
from agents.action_agent import ActionAgent
from agents.crawler_agent import CrawlerAgent
from agents.tts_agent import TTSAgent

_log = get_logger("main")


async def main() -> None:
    """Initialise and run all agents."""

    _log.info("=" * 60)
    _log.info("  Multimodal AI Assistant — starting up")
    _log.info("=" * 60)

    # ── Shared event bus ────────────────────────────────────────────────
    bus = EventBus()

    # ── Instantiate agents ──────────────────────────────────────────────
    agents = [
        GestureAgent(bus),
        SpeechAgent(bus),
        FusionAgent(bus),
        IntentParser(bus),
        ActionAgent(bus),
        CrawlerAgent(bus),
        TTSAgent(bus),
    ]

    # ── Graceful shutdown on Ctrl+C / SIGTERM ───────────────────────────
    shutdown_event = asyncio.Event()

    def _signal_handler() -> None:
        _log.info("Shutdown signal received")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler for SIGTERM
            signal.signal(sig, lambda *_: _signal_handler())

    # ── Start all agents ────────────────────────────────────────────────
    _log.info("Starting %d agents …", len(agents))
    for agent in agents:
        try:
            await agent.start()
            _log.info("  ✓ %s", agent.name)
        except Exception as exc:
            _log.error("  ✗ %s failed to start: %s", agent.name, exc)

    _log.info("All agents running. Press Ctrl+C to stop.\n")

    # ── Wait for shutdown ───────────────────────────────────────────────
    await shutdown_event.wait()

    # ── Stop all agents (reverse order) ─────────────────────────────────
    _log.info("Shutting down …")
    for agent in reversed(agents):
        try:
            await agent.stop()
        except Exception as exc:
            _log.error("Error stopping %s: %s", agent.name, exc)

    _log.info("Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
