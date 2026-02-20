
<img src="./gitbot_logo.png" width="100" height="100"/>

## GitBot: Lightweight Personal AI Assistant for Git

> **Your AI-powered Git & GitHub Assistant.**  
> Orchestrate local git operations and manage remote repositories using natural language.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-beta-orange.svg)

**GitBot** bridges the gap between your terminal and GitHub. It combines a **local Git Orchestrator** with the **GitHub MCP Server**, allowing an LLM (Groq, Gemini, or Ollama) to understand your intent and execute commands on your behalf.

---

## Features

- **Local Git Control**: Initialize, stage, commit, push, and check status of local repositories.
- **GitHub Integration**: Create issues, review PRs, and browse remote repos via MCP.
- **Model Agnostic**: Supports **Groq** (Llama 3), **Google Gemini**, and local **Ollama** models.
- **Smart Context**: Aware of your current directory andgit status.
- **Safe & Secure**: Always asks for confirmation before destructive actions (delete, force-push).

---

## Installation

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git installed and on your PATH
- Node.js (required for GitHub MCP server)

### Install with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/udaykumar-dhokia/gitbot.git
cd gitbot

# Install dependencies and tool
uv tool install .
```

---

## Usage

### 1. Onboarding
First-time setup? Run the onboarding wizard to configure your credentials and preferred LLM.

```bash
gitbot onboard
```

You'll need:
- **GitHub Token**: A classic Personal Access Token with `repo` scope.
- **API Key**: For Groq or Gemini (or a running Ollama instance).

### 2. Chat Mode
Start the interactive assistant:

```bash
gitbot chat
```

**Example Prompts:**
- "Initialize a git repo here and commit all files with message 'Initial commit'"
- "Create a new issue on my 'test-repo' about a bug in the login flow"
- "Summarize the last 5 commits"
- "Push my changes to origin main"

### 3. Check Configuration
View your current settings:

```bash
gitbot config
```

---

## Configuration

GitBot stores configuration in `~/.gitbot/config.json`.

| Setting | Description |
| :--- | :--- |
| `github_token` | Your GitHub Personal Access Token. |
| `llm_provider` | `groq`, `gemini`, or `ollama`. |
| `llm_model` | Specific model name (e.g., `llama-3.3-70b-versatile`). |
| `ollama_base_url` | URL for local Ollama instance (default: `http://localhost:11434`). |

---

## Architecture

GitBot is built with a modular architecture:

- **`gitbot.core`**: Main agent loop and state management.
- **`gitbot.cli`**: Click-based command line interface.
- **`gitbot.tools`**: LangChain wrappers for local `git` subprocess calls.
- **`gitbot.mcp`**: Client for the Model Context Protocol, connecting to GitHub.
- **`gitbot.llm`**: Factory for initializing ChatGroq, ChatOllama, etc.
- **`gitbot.ui`**: Rich-based terminal UI components.

---

## Roadmap

- [ ] **Long Term Memory**: Semantic memories to remember user preferences and past interactions across sessions.
- [ ] **Multi-Provider Integration**: Use different LLMs for different tasks (e.g., a small fast model for routing, a large reasoning model for complex tasks).
- [ ] **TOON Implementation**: Token-Oriented Object Notation.

---

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

---

<div align="center">

If you find GitBot useful, don't forget to give it a star! ⭐

</div>