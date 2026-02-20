"""
GitBot agent loop — ties together LLM, MCP, and terminal UI.
"""

import asyncio
import json

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

from gitbot.core.config import load_config, load_memory, save_memory, is_onboarded
from gitbot.llm.providers import get_llm
from gitbot.mcp.client import connect_mcp, mcp_tools_to_langchain, call_mcp_tool
from gitbot.tools.git_tools import get_git_tools
from gitbot.ui.console import (
    console,
    print_banner,
    print_tool_call,
    print_tool_result,
    print_response,
    print_thinking,
    print_error,
    print_welcome_back,
)

SYSTEM_PROMPT = """You are GitBot, an AI assistant that helps users interact with Git and GitHub using natural language.

The current user's GitHub details:
- Username: {github_username}
- Email: {github_email}

You have access to GitHub tools via MCP (Model Context Protocol) and local git tools. Use them to:
- Manage local git repositories (init, add, commit, push, status, log)
- Search and browse repositories
- Create, update, and manage issues
- Create and review pull requests
- Read file contents from repos
- Manage branches and commits
- And much more

Guidelines:
- Be helpful, concise, and accurate.
- When using tools, explain what you're doing.
- Always use the user's GitHub username from above — never ask for it.
- Format output nicely using markdown.
- If a tool call fails, explain the error and suggest alternatives.
- Always confirm destructive actions (delete, force-push, etc.) before proceeding.
"""


def _serialize_messages(messages) -> list[dict]:
    """Convert LangChain messages to serializable dicts for persistence."""
    serialized = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            continue
        entry = {"type": msg.type, "content": msg.content}
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            entry["tool_calls"] = [
                {"name": tc["name"], "args": tc["args"], "id": tc["id"]}
                for tc in msg.tool_calls
            ]
        if hasattr(msg, "tool_call_id") and msg.tool_call_id:
            entry["tool_call_id"] = msg.tool_call_id
        serialized.append(entry)
    return serialized


def _deserialize_messages(data: list[dict]) -> list:
    """Convert persisted dicts back to LangChain messages."""
    messages = []
    for entry in data:
        msg_type = entry.get("type", "")
        content = entry.get("content", "")

        if msg_type == "human":
            messages.append(HumanMessage(content=content))
        elif msg_type == "ai":
            tool_calls = entry.get("tool_calls", [])
            messages.append(AIMessage(content=content, tool_calls=tool_calls))
        elif msg_type == "tool":
            messages.append(
                ToolMessage(content=content, tool_call_id=entry.get("tool_call_id", ""))
            )
    return messages


async def run_agent_loop():
    """Main agent loop — connect MCP, bind tools, and chat."""

    if not is_onboarded():
        print_error("You haven't onboarded yet! Run [bold]gitbot onboard[/bold] first.")
        return

    config = load_config()

    print_banner()
    print_welcome_back(config["github_username"])

    try:
        llm = get_llm(config)
    except Exception as e:
        print_error(f"Failed to initialize LLM: {e}")
        return

    console.print("[muted]  Connecting to GitHub MCP server…[/muted]")

    try:
        async with connect_mcp(config["github_token"]) as (session, mcp_tools):
            console.print(
                f"  [success]✔[/success]  Connected! [muted]{len(mcp_tools)} tools available.[/muted]\n"
            )
            console.rule(style="cyan")
            console.print()

            lc_tools = mcp_tools_to_langchain(mcp_tools)
            local_tools = get_git_tools()
            local_tool_map = {t.name: t for t in local_tools}

            llm_with_tools = llm.bind_tools(lc_tools + local_tools)

            raw_memory = load_memory()
            messages = _deserialize_messages(raw_memory)

            system_msg = SystemMessage(
                content=SYSTEM_PROMPT.format(
                    github_username=config.get("github_username", ""),
                    github_email=config.get("github_email", ""),
                )
            )

            while True:
                try:
                    user_input = console.input("[bold cyan]  You → [/bold cyan]")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[muted]  Goodbye! 👋[/muted]")
                    break

                user_input = user_input.strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit", "q"):
                    console.print("\n[muted]  Goodbye! 👋[/muted]")
                    break

                messages.append(HumanMessage(content=user_input))

                full_messages = [system_msg] + messages

                with print_thinking():
                    response = await asyncio.to_thread(
                        llm_with_tools.invoke, full_messages
                    )

                while response.tool_calls:
                    messages.append(response)

                    for tool_call in response.tool_calls:
                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]
                        tool_id = tool_call["id"]

                        print_tool_call(tool_name, tool_args)

                        try:
                            with print_thinking():
                                if tool_name in local_tool_map:
                                    result = local_tool_map[tool_name].invoke(tool_args)
                                else:
                                    result = await call_mcp_tool(
                                        session, tool_name, tool_args
                                    )
                            print_tool_result(result)
                        except Exception as e:
                            result = f"Error calling tool '{tool_name}': {e}"
                            print_error(result)

                        llm_result = (
                            result
                            if len(result) < 4000
                            else result[:4000] + "\n... (truncated)"
                        )

                        messages.append(
                            ToolMessage(content=llm_result, tool_call_id=tool_id)
                        )

                    full_messages = [system_msg] + messages
                    with print_thinking():
                        response = await asyncio.to_thread(
                            llm_with_tools.invoke, full_messages
                        )

                messages.append(response)
                print_response(response.content)

                save_memory(_serialize_messages(messages))

                if len(messages) > 50:
                    messages = messages[-50:]

    except FileNotFoundError as e:
        print_error(str(e))
        console.print(
            "[muted]  Make sure Node.js is installed and 'npx' is on your PATH.[/muted]"
        )
    except BaseException as e:
        actual = e
        while hasattr(actual, "exceptions") and actual.exceptions:
            actual = actual.exceptions[0]
        print_error(f"MCP connection failed: {actual}")
