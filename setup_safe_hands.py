"""
setup_safe_hands.py — Run ONCE before using checkpoint.py for the first time.

Does:
  1. Verifies .gitignore covers all sensitive/large files
  2. Initializes a local Git repository (if not already done)
  3. Creates the very first checkpoint commit

After this runs, use:
  - python checkpoint.py  → save progress
  - python undo_changes.py  → revert to last checkpoint
"""

import subprocess
import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REQUIRED_IGNORES = [
    "node_modules/",
    ".next/",
    "__pycache__/",
    ".venv/",
    ".env",
    ".env.local",
    "*.pyc",
    "*.png",
]


def run_git_cmd(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True,
            cwd=cwd or PROJECT_ROOT
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  Git error: {e.stderr.strip()}")
        return None


def check_gitignore():
    gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
    if not os.path.exists(gitignore_path):
        print("  WARNING: .gitignore not found — creating one...")
        with open(gitignore_path, "w") as f:
            f.write("\n".join(REQUIRED_IGNORES) + "\n")
        print("  .gitignore created.")
        return

    with open(gitignore_path) as f:
        content = f.read()

    missing = [rule for rule in REQUIRED_IGNORES if rule not in content]
    if missing:
        print(f"  WARNING: .gitignore is missing: {missing}")
        print("  Add these manually to .gitignore before proceeding.")
        sys.exit(1)
    else:
        print("  .gitignore OK")


def setup():
    print("=== Safe Hands Setup ===")
    print(f"Project root: {PROJECT_ROOT}\n")

    # Step 1: Check .gitignore
    print("[1/3] Checking .gitignore...")
    check_gitignore()

    # Step 2: Init git if needed
    print("\n[2/3] Initializing Git repository...")
    git_dir = os.path.join(PROJECT_ROOT, ".git")
    if os.path.exists(git_dir):
        print("  Git already initialized. Skipping.")
    else:
        result = run_git_cmd(["git", "init"])
        if result is None:
            print("  FAILED to initialize Git. Is Git installed?")
            sys.exit(1)
        print(f"  {result}")

    # Step 3: Create initial checkpoint
    print("\n[3/3] Creating initial checkpoint commit...")
    run_git_cmd(["git", "add", "."])
    status = run_git_cmd(["git", "status", "--porcelain"])
    if not status:
        print("  Nothing to commit — repository is already clean.")
    else:
        result = run_git_cmd(["git", "commit", "-m", "Safe Hands: Initial Checkpoint"])
        if result:
            print(f"  Committed: {result}")
        else:
            print("  WARNING: Commit may have failed. Check git status manually.")

    print("\n[DONE] Safe Hands is ready.")
    print("  -> Run 'python checkpoint.py' before any AI session to save your state.")
    print("  -> Run 'python undo_changes.py' to revert to the last checkpoint.")
    print("\n  IMPORTANT: undo_changes.py reverts FILE changes only.")
    print("  Supabase DB migrations are NOT reverted. Use Supabase branching for DB safety.")


if __name__ == "__main__":
    setup()
