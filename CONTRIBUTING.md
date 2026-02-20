# Contributing to GitBot

Thank you for your interest in contributing to GitBot! We welcome contributions from the community to help make this AI-powered Git assistant even better.

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

---

## 🛠️ Development Setup

### 1. Prerequisites

Before you start, ensure you have the following installed:

- **Python 3.13+**
- **Git**
- **Node.js** (for the GitHub MCP server dependency)
- **uv** (recommended for dependency management)

### 2. Fork and Clone

fork the repository to your own GitHub account and then clone it locally:

```bash
git clone https://github.com/udaykumar-dhokia/gitbot.git
cd gitbot
```

### 3. Set Up Environment

We recommend using `uv` to manage the virtual environment and dependencies.

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (including dev tools)
uv pip install -e .
```

---

## 📂 Project Structure

Current modular structure of the codebase:

```
gitbot/
├── cli/                    # CLI entry points and command definitions
├── core/                   # Core logic (agent loop, config, git orchestrator)
├── llm/                    # LLM provider factories (Groq, Gemini, Ollama)
├── mcp/                    # MCP client integration for GitHub API
├── tools/                  # LangChain tool definitions (local git tools)
├── ui/                     # Rich-based terminal UI components
└── onboarding/             # Onboarding wizard logic
```

---

## 🧪 Testing Your Changes

### Manual Testing

Since GitBot interacts with both local filesystem and live GitHub APIs, manual testing is often required.

1. **Verify local changes**:
   ```bash
   python main.py chat
   ```
2. **Test local git operations**: Ask the bot to init/commit in a temp folder.
3. **Test remote operations**: Ask the bot to list issues on a test repository.

---

## 📝 Pull Request Process

1. **Create a new branch**: Use a descriptive name for your branch (e.g., `feature/add-log-summaries` or `fix/windows-path-bug`).
2. **Commit your changes**: Write clear, concise commit messages.
3. **Push to your fork**: `git push origin feature/your-feature-name`.
4. **Open a Pull Request**: Submit a PR to the `main` branch of the original repository.
    - Describe the changes you made.
    - Link to any relevant issues.
    - Include screenshots if you modified the UI.

---

## 🎨 Code Style

- We follow **PEP 8** guidelines.
- Please use **type hints** for function arguments and return values.
- Ensure your code is formatted cleanly (you can use `ruff` or `black` before committing).

---

## ❓ Getting Help

If you have questions or run into issues, please open an issue on GitHub. We're happy to help!

Thank you for contributing! 🚀
