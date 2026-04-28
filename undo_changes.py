import subprocess
import os

def run_git_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def undo():
    print("--- Safe Hands: EMERGENCY REVERT ---")
    print()
    print("  *** IMPORTANT LIMITS OF THIS SCRIPT ***")
    print("  This ONLY reverts FILE changes (code, vault, config).")
    print("  Supabase DB changes (migrations, table edits) are NOT reverted.")
    print("  If the AI touched the database, use Supabase dashboard to roll back manually.")
    print()

    # 1. Check if git is initialized
    if not os.path.exists(".git"):
        print("Error: Git is not initialized. Run 'python setup_safe_hands.py' first.")
        return

    print("Reverting all files to the last saved checkpoint...")

    # Reset tracked files
    run_git_cmd(["git", "reset", "--hard", "HEAD"])

    # Clean untracked files (new files created by the AI)
    run_git_cmd(["git", "clean", "-fd"])

    print("\n[SUCCESS] All file changes wiped. Project restored to the previous checkpoint.")
    print("  If you also need to revert DB changes, do that in the Supabase dashboard.")

if __name__ == "__main__":
    undo()
