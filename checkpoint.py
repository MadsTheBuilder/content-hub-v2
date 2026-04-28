import subprocess
import datetime
import os
import sys

def run_git_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def checkpoint():
    print("--- Safe Hands: Creating Checkpoint ---")
    
    # 1. Check if git is initialized
    if not os.path.exists(".git"):
        print("Error: Git is not initialized. Run 'git init' first.")
        return

    # 1.5 Run Vault Sync to capture the latest Brain State
    print("Syncing Obsidian Vault...")
    try:
        sync_result = subprocess.run(
            ["python", "sync_vault.py"],
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if sync_result.returncode != 0:
            print(f"Warning: Vault sync failed (exit {sync_result.returncode}): {sync_result.stderr.strip()}")
            print("  Proceeding without vault update...")
        else:
            print("  Vault sync OK")
    except Exception as e:
        print(f"Warning: Vault sync failed ({e}). Proceeding anyway...")

    # 2. Stage all changes
    print("Staging changes...")
    run_git_cmd(["git", "add", "."])

    # 3. Check if there are changes to commit
    status = run_git_cmd(["git", "status", "--porcelain"])
    if not status:
        print("No changes detected. Your project is already up to date with the last checkpoint.")
        return

    # 4. Commit with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Safe Hands Checkpoint: {timestamp}"
    
    print(f"Saving state: {msg}")
    run_git_cmd(["git", "commit", "-m", msg])
    
    print("\n[SUCCESS] Checkpoint saved. You can now safely let the AI work.")
    print("If things go wrong, run 'python undo_changes.py' to revert.")

if __name__ == "__main__":
    checkpoint()
