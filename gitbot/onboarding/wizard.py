"""
GitBot onboarding wizard — collects GitHub creds, LLM provider & model.
"""

import json
import urllib.request
import urllib.error

from rich.prompt import Prompt, Confirm

from gitbot.core.config import save_config, load_config, is_onboarded
from gitbot.ui.console import (
    console,
    print_banner,
    print_step,
    print_success,
    print_error,
)

GROQ_TOOL_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

GEMINI_TOOL_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-pro",
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
]


def _fetch_ollama_models(base_url: str) -> list[str]:
    """Fetch locally available models from the Ollama API."""
    url = f"{base_url.rstrip('/')}/api/tags"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            return sorted(models)
    except urllib.error.URLError as e:
        print_error(f"Could not connect to Ollama at {base_url}: {e}")
        return []
    except Exception as e:
        print_error(f"Failed to fetch models: {e}")
        return []


def run_onboarding():
    """Run the full onboarding wizard."""

    print_banner()

    if is_onboarded():
        console.print("[warning]⚠  You are already onboarded![/warning]")
        if not Confirm.ask("  Do you want to re-configure?", default=False):
            return
        console.print()

    config = load_config()

    print_step(1, "GitHub Credentials")
    console.print(
        "[muted]  We need your GitHub info to interact with repositories.[/muted]\n"
    )

    config["github_email"] = Prompt.ask(
        "    [cyan]📧 GitHub Email[/cyan]", default=config.get("github_email") or ""
    )
    config["github_username"] = Prompt.ask(
        "    [cyan]👤 GitHub Username[/cyan]",
        default=config.get("github_username") or "",
    )
    config["github_token"] = Prompt.ask(
        "    [cyan]🔑 GitHub Personal Access Token[/cyan]", password=True
    )

    if not config["github_token"]:
        print_error("GitHub token is required!")
        return

    print_success("GitHub credentials saved.")

    print_step(2, "LLM Provider")
    console.print(
        "[muted]  Choose which LLM backend to use for natural language processing.[/muted]\n"
    )

    provider = Prompt.ask(
        "    [cyan]🧠 LLM Provider[/cyan]",
        choices=["ollama", "groq", "gemini"],
        default=config.get("llm_provider") or "gemini",
    )
    config["llm_provider"] = provider

    if provider == "groq":
        config["groq_api_key"] = Prompt.ask(
            "    [cyan]🔑 Groq API Key[/cyan]",
            password=True,
            default=config.get("groq_api_key") or "",
        )
        if not config["groq_api_key"]:
            print_error("Groq API key is required!")
            return

    elif provider == "gemini":
        config["gemini_api_key"] = Prompt.ask(
            "    [cyan]🔑 Google Gemini API Key[/cyan]",
            password=True,
            default=config.get("gemini_api_key") or "",
        )
        if not config["gemini_api_key"]:
            print_error("Gemini API key is required!")
            return

    elif provider == "ollama":
        default_url = config.get("ollama_base_url") or "http://localhost:11434"
        console.print(
            f"    [muted]Press Enter to use default ([bold]{default_url}[/bold])[/muted]"
        )
        base_url = Prompt.ask(
            "    [cyan]🌐 Ollama Base URL[/cyan]",
            default=default_url,
        )
        config["ollama_base_url"] = base_url.rstrip("/")

    print_success(f"LLM provider set to [bold]{provider}[/bold].")

    print_step(3, "Model Selection")
    console.print("[muted]  Pick a model that supports tool calling.[/muted]\n")

    if provider == "groq":
        models = GROQ_TOOL_MODELS
        console.print(
            "    [muted]Recommended Groq models with tool-calling support:[/muted]\n"
        )
    elif provider == "gemini":
        models = GEMINI_TOOL_MODELS
        console.print(
            "    [muted]Google Gemini models with tool-calling support:[/muted]\n"
        )
    else:
        console.print(
            f"    [muted]Fetching models from Ollama ({config['ollama_base_url']})…[/muted]\n"
        )
        models = _fetch_ollama_models(config["ollama_base_url"])
        if not models:
            print_error(
                "No models found. Make sure Ollama is running and has models pulled.\n"
                "    Try: ollama pull llama3.1:8b"
            )
            return

    for i, model in enumerate(models, 1):
        console.print(f"    [cyan]{i}.[/cyan] {model}")

    console.print()
    choice = Prompt.ask(
        "    [cyan]🤖 Select model number[/cyan]",
        choices=[str(i) for i in range(1, len(models) + 1)],
        default="1",
    )
    config["llm_model"] = models[int(choice) - 1]

    print_success(f"Model set to [bold]{config['llm_model']}[/bold].")

    save_config(config)

    console.print()
    console.rule(style="green")
    console.print("\n  [success]🎉 Onboarding complete![/success]")
    console.print(
        "  [muted]Run [bold]gitbot chat[/bold] to start interacting with GitHub.[/muted]\n"
    )
    console.rule(style="green")
    console.print()
