"""
MCP client — connects to @modelcontextprotocol/server-github via stdio.
Exposes tools for the agent loop.
"""

import asyncio
import json
import os
import shutil
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _find_npx() -> str:
    """Locate npx executable, trying npx.cmd on Windows first."""
    for name in ("npx.cmd", "npx"):
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError(
        "Could not find 'npx' on PATH. Please install Node.js first."
    )


def build_server_params(github_token: str) -> StdioServerParameters:
    """Build the stdio server parameters for the GitHub MCP server."""
    npx_path = _find_npx()

    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token

    return StdioServerParameters(
        command=npx_path,
        args=["-y", "@modelcontextprotocol/server-github"],
        env=env,
    )


@asynccontextmanager
async def connect_mcp(github_token: str):
    """
    Async context manager that starts the GitHub MCP server and yields
    (session, tools_list).

    Usage:
        async with connect_mcp(token) as (session, tools):
            result = await session.call_tool("list_repos", {...})
    """
    server_params = build_server_params(github_token)

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            tools = tools_response.tools

            yield session, tools


def _clean_schema(schema: dict) -> dict:
    """Remove keys not supported by all LLM providers (e.g. Gemini)."""
    if not isinstance(schema, dict):
        return schema

    unsupported_keys = {"$schema", "additionalProperties"}
    cleaned = {}
    for key, value in schema.items():
        if key in unsupported_keys:
            continue
        if isinstance(value, dict):
            cleaned[key] = _clean_schema(value)
        elif isinstance(value, list):
            cleaned[key] = [
                _clean_schema(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned


def mcp_tools_to_langchain(tools) -> list[dict]:
    """
    Convert MCP tool definitions to LangChain-compatible tool schemas.
    Cleans unsupported schema keys for cross-provider compatibility.
    """
    lc_tools = []
    for tool in tools:
        raw_params = (
            tool.inputSchema
            if tool.inputSchema
            else {"type": "object", "properties": {}}
        )
        schema = {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": _clean_schema(raw_params),
        }
        lc_tools.append(schema)
    return lc_tools


async def call_mcp_tool(session: ClientSession, name: str, arguments: dict) -> str:
    """Call an MCP tool and return the text result."""
    result = await session.call_tool(name, arguments)

    parts = []
    for content in result.content:
        if hasattr(content, "text"):
            parts.append(content.text)
        else:
            parts.append(str(content))

    return "\n".join(parts)
