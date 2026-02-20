"""
GitBot CLI entry point — Click commands.
"""

import asyncio
import click
from gitbot.onboarding.wizard import run_onboarding


@click.group()
def cli():
    """GitBot — Your AI-powered Git & GitHub assistant."""
    pass


@cli.command()
def onboard():
    """Run the onboarding wizard to configure GitBot."""
    run_onboarding()


@cli.command()
def chat():
    """Start an interactive chat session with GitBot."""
    from gitbot.core.agent import run_agent_loop

    asyncio.run(run_agent_loop())


@cli.command()
def config():
    """Show current GitBot configuration."""
    from gitbot.core.config import load_config, is_onboarded, CONFIG_FILE
    from gitbot.ui.console import console
    from rich.table import Table

    if not is_onboarded():
        console.print(
            "[warning]⚠  Not onboarded yet. Run [bold]gitbot onboard[/bold] first.[/warning]"
        )
        return

    cfg = load_config()
    table = Table(title="GitBot Configuration", border_style="cyan")
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Config File", str(CONFIG_FILE))
    table.add_row("GitHub Email", cfg.get("github_email", ""))
    table.add_row("GitHub Username", cfg.get("github_username", ""))
    table.add_row(
        "GitHub Token",
        "••••" + cfg.get("github_token", "")[-4:] if cfg.get("github_token") else "",
    )
    table.add_row("LLM Provider", cfg.get("llm_provider", ""))
    table.add_row("LLM Model", cfg.get("llm_model", ""))
    table.add_row(
        "Groq API Key",
        "••••" + cfg.get("groq_api_key", "")[-4:] if cfg.get("groq_api_key") else "N/A",
    )
    table.add_row(
        "Gemini API Key",
        (
            "••••" + cfg.get("gemini_api_key", "")[-4:]
            if cfg.get("gemini_api_key")
            else "N/A"
        ),
    )

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    cli()
