"""
GitBot configuration management.
Reads/writes config from ~/.gitbot/config.json
"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".gitbot"
CONFIG_FILE = CONFIG_DIR / "config.json"
MEMORY_FILE = CONFIG_DIR / "memory.json"

DEFAULT_CONFIG = {
    "github_email": "",
    "github_username": "",
    "github_token": "",
    "llm_provider": "",
    "llm_model": "",
    "groq_api_key": "",
    "gemini_api_key": "",
    "ollama_base_url": "http://localhost:11434",
}


def ensure_config_dir():
    """Create the config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load config from disk. Returns default config if file doesn't exist."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save config dict to disk."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def is_onboarded() -> bool:
    """Check if the user has completed onboarding."""
    if not CONFIG_FILE.exists():
        return False
    config = load_config()
    return bool(config.get("github_token")) and bool(config.get("llm_provider"))


def load_memory() -> list:
    """Load chat memory from disk."""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(messages: list):
    """Save chat memory to disk."""
    ensure_config_dir()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)
