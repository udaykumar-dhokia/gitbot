"""
Local Git Orchestrator — wraps git CLI commands.
Responsible for executing git operations on the local filesystem.
"""

import subprocess
import shutil
from pathlib import Path


class GitOrchestrator:
    def __init__(self):
        self._check_git_installed()

    def _check_git_installed(self):
        if not shutil.which("git"):
            raise RuntimeError("Git is not installed or not on PATH.")

    def _run_git(self, args: list[str], cwd: Path) -> dict:
        """Run a git command in the specified directory."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=str(cwd.resolve()),
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
            }

    def is_git_initialized(self, path: Path) -> bool:
        """Check if a directory is a git repository."""
        return (path.resolve() / ".git").is_dir()

    def git_init(self, path: Path) -> dict:
        """Initialize a new git repository."""
        if self.is_git_initialized(path):
            return {
                "success": True,
                "stdout": "Already a git repository.",
                "stderr": "",
            }

        path.mkdir(parents=True, exist_ok=True)
        return self._run_git(["init"], cwd=path)

    def git_status(self, path: Path) -> dict:
        """Get git status."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}
        return self._run_git(["status"], cwd=path)

    def git_add(self, path: Path, files: list[str]) -> dict:
        """Stage files."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}

        if not files:
            return {"success": False, "stderr": "No files specified to add."}

        return self._run_git(["add"] + files, cwd=path)

    def git_commit(self, path: Path, message: str) -> dict:
        """Commit staged changes."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}

        if not message:
            return {"success": False, "stderr": "Commit message is required."}

        return self._run_git(["commit", "-m", message], cwd=path)

    def git_log(self, path: Path, n: int = 10) -> dict:
        """Show commit log."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}

        return self._run_git(
            ["log", f"-n {n}", "--oneline", "--graph", "--decorate"], cwd=path
        )

    def git_remote_add(self, path: Path, name: str, url: str) -> dict:
        """Add a remote."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}

        # Check if remote exists
        remotes = self._run_git(["remote"], cwd=path)
        if name in remotes["stdout"].split():
            return {"success": False, "stderr": f"Remote '{name}' already exists."}

        return self._run_git(["remote", "add", name, url], cwd=path)

    def git_push(
        self, path: Path, remote: str = "origin", branch: str = "main"
    ) -> dict:
        """Push to remote."""
        if not self.is_git_initialized(path):
            return {"success": False, "stderr": "Not a git repository."}

        return self._run_git(["push", "-u", remote, branch], cwd=path)

    def ensure_git_ready(self, path: Path) -> dict:
        """Ensure git is initialized."""
        if not self.is_git_initialized(path):
            return self.git_init(path)
        return {"success": True, "stdout": "Git is ready.", "stderr": ""}
