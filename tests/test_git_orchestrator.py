import unittest
import shutil
import tempfile
import os
import stat
from pathlib import Path
from gitbot.core.git_orchestrator import GitOrchestrator


class TestGitOrchestrator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.path = Path(self.test_dir)
        self.orchestrator = GitOrchestrator()

    def tearDown(self):
        def onerror(func, path, exc_info):
            if not os.access(path, os.W_OK):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            else:
                raise

        shutil.rmtree(self.test_dir, onerror=onerror)

    def test_init_and_status(self):
        # 1. Init
        result = self.orchestrator.git_init(self.path)
        self.assertTrue(result["success"])
        self.assertTrue(self.orchestrator.is_git_initialized(self.path))

        # 2. Status (should be empty)
        status = self.orchestrator.git_status(self.path)
        self.assertTrue(status["success"])
        self.assertIn("On branch", status["stdout"])

    def test_add_and_commit(self):
        self.orchestrator.git_init(self.path)

        # Configure dummy git user for commits
        self.orchestrator._run_git(
            ["config", "--local", "user.email", "test@example.com"], cwd=self.path
        )
        self.orchestrator._run_git(
            ["config", "--local", "user.name", "Test User"], cwd=self.path
        )

        # Create a file
        test_file = self.path / "test.txt"
        test_file.write_text("hello world")

        # 1. Add
        add_result = self.orchestrator.git_add(self.path, ["."])
        self.assertTrue(add_result["success"])

        # 2. Commit
        commit_result = self.orchestrator.git_commit(self.path, "Initial commit")
        self.assertTrue(commit_result["success"])

        # 3. Log
        log_result = self.orchestrator.git_log(self.path)
        self.assertTrue(log_result["success"])
        self.assertIn("Initial commit", log_result["stdout"])


if __name__ == "__main__":
    unittest.main()
