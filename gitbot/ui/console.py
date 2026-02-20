"""
GitBot terminal UI helpers using Rich and Pyfiglet.
"""

import json
import pyfiglet
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "heading": "bold magenta",
        "muted": "dim white",
    }
)

console = Console(theme=custom_theme)


def print_banner():
    """Display the GitBot ASCII art banner."""
    ascii_art = pyfiglet.figlet_format("GitBot", font="slant")
    console.print(f"[bold cyan]{ascii_art}[/bold cyan]", end="")
    console.print("[muted]  Your AI-powered Git & GitHub assistant[/muted]\n")
    console.rule(style="cyan")
    console.print()


def print_step(step_num: int, title: str):
    """Print a numbered onboarding step header."""
    console.print(
        f"\n[heading]  Step {step_num}[/heading]  [bold white]{title}[/bold white]\n"
    )


def print_success(message: str):
    """Print a success message."""
    console.print(f"  [success]✔[/success]  {message}")


def print_error(message: str):
    """Print an error message."""
    console.print(Panel(f"[error]✖  {message}[/error]", border_style="red"))


def print_tool_call(name: str, args: dict):
    """Show a tool call in a styled panel."""
    args_str = json.dumps(args, indent=2)
    syntax = Syntax(args_str, "json", theme="monokai", line_numbers=False)
    console.print(
        Panel(
            syntax,
            title=f"[bold yellow]🔧 Tool Call:[/bold yellow] [white]{name}[/white]",
            border_style="yellow",
            padding=(0, 1),
        )
    )


def print_tool_result(result: str):
    """Show a tool result in a styled panel."""
    display = result if len(result) < 2000 else result[:2000] + "\n… (truncated)"
    console.print(
        Panel(
            display,
            title="[bold green]📦 Tool Result[/bold green]",
            border_style="green",
            padding=(0, 1),
        )
    )


def print_response(text: str):
    """Render an LLM response as markdown."""
    console.print()
    console.print(
        Panel(
            Markdown(text),
            title="[bold cyan]🤖 GitBot[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


def print_thinking():
    """Return a Rich Status context manager for 'thinking' spinner."""
    return console.status("[bold cyan]  Thinking…[/bold cyan]", spinner="dots")


def print_welcome_back(username: str):
    """Print a welcome-back message for returning users."""
    console.print(f"\n[success]👋 Welcome back, [bold]{username}[/bold]![/success]\n")
    console.print(
        "[muted]Type your message to interact with GitHub, or 'exit' to quit.[/muted]\n"
    )
    console.rule(style="cyan")
    console.print()
