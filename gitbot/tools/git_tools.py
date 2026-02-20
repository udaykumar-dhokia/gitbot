"""
LangChain tool wrappers for local git operations.
"""

from pathlib import Path
from langchain_core.tools import tool
from gitbot.core.git_orchestrator import GitOrchestrator

orchestrator = GitOrchestrator()


@tool
def local_git_init(path: str = ".") -> str:
    """
    Initialize a new local git repository.

    Args:
        path: Path to initialize the repo in (default: current directory).
    """
    result = orchestrator.git_init(Path(path))
    if result["success"]:
        return f"Successfully initialized git repo in {path}"
    return f"Failed to initialize git repo: {result['stderr']}"


@tool
def local_git_status(path: str = ".") -> str:
    """
    Show the working tree status.

    Args:
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_status(Path(path))
    if result["success"]:
        return result["stdout"]
    return f"Error getting status: {result['stderr']}"


@tool
def local_git_add(files: list[str], path: str = ".") -> str:
    """
    Add file contents to the staging area.

    Args:
        files: List of files to add (e.g. ["file1.py", "."]).
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_add(Path(path), files)
    if result["success"]:
        return result["stdout"] or "Files staged successfully."
    return f"Error staging files: {result['stderr']}"


@tool
def local_git_commit(message: str, path: str = ".") -> str:
    """
    Record changes to the repository.

    Args:
        message: The commit message.
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_commit(Path(path), message)
    if result["success"]:
        return result["stdout"]
    return f"Error committing: {result['stderr']}"


@tool
def local_git_log(n: int = 10, path: str = ".") -> str:
    """
    Show commit logs.

    Args:
        n: Number of commits to show (default: 10).
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_log(Path(path), n)
    if result["success"]:
        return result["stdout"]
    return f"Error getting log: {result['stderr']}"


@tool
def local_git_remote_add(name: str, url: str, path: str = ".") -> str:
    """
    Add a remote repository.

    Args:
        name: Name of the remote (e.g. "origin").
        url: URL of the remote.
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_remote_add(Path(path), name, url)
    if result["success"]:
        return f"Remote '{name}' added successfully."
    return f"Error adding remote: {result['stderr']}"


@tool
def local_git_push(
    remote: str = "origin", branch: str = "main", path: str = "."
) -> str:
    """
    Update remote refs along with associated objects.

    Args:
        remote: Remote name (default: "origin").
        branch: Branch name (default: "main").
        path: Path to the repo (default: current directory).
    """
    result = orchestrator.git_push(Path(path), remote, branch)
    if result["success"]:
        return result["stdout"] or "Push successful."
    return f"Error pushing to {remote}/{branch}: {result['stderr']}"


def get_git_tools() -> list:
    """Return a list of all git tools."""
    return [
        local_git_init,
        local_git_status,
        local_git_add,
        local_git_commit,
        local_git_log,
        local_git_remote_add,
        local_git_push,
    ]
