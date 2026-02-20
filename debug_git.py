from pathlib import Path
from gitbot.core.git_orchestrator import GitOrchestrator
from gitbot.tools.git_tools import local_git_status

# Create a dummy repo in a non-cwd location
test_path = Path("C:/Users/HP/Desktop/test_git_debug")
test_path.mkdir(parents=True, exist_ok=True)

orch = GitOrchestrator()
print(f"Initializing repo at {test_path}...")
print(orch.git_init(test_path))

print(f"\nChecking status at {test_path}...")
# invoke method for LangChain tools
status = local_git_status.invoke({"path": str(test_path)})
print(f"Status output:\n{status}")

# explicitly check is_git_initialized
print(f"\nis_git_initialized({test_path}): {orch.is_git_initialized(test_path)}")
