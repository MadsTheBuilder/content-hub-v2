import os
import datetime
import shutil
import ast
import re
import subprocess
import glob
from pathlib import Path

# Configuration
SOURCE_DIR = os.getcwd()
VAULT_DIR = os.path.join(SOURCE_DIR, 'Content-Hub-Vault')
MGMT_DIR = os.path.join(VAULT_DIR, '00-Management')

EXCLUDE_DIRS = {
    'node_modules', '.next', '__pycache__', '.git', '.venv', 
    'tmp_downloads', 'tmp_marketingskills', '.gemini', 'Content-Hub-Vault', '_vault'
}

EXCLUDE_EXTS = {
    '.mp4', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', 
    '.eot', '.ttf', '.woff', '.woff2', '.otf', '.svg', '.zip', 
    '.pyc', '.dll', '.exe', '.lock'
}

# Root-level docs to be SYNCED to 00-Management/Plans/ and DELETED from vault root
DOC_FILES_TO_MGMT = {
    'AGENTS.md', 
    'CHANGES_REPORT.md', 
    'CLAUDE.md', 
    'IMPLEMENTATION_SUMMARY.md', 
    'MARKETING_SKILL_INTEGRATION_SUMMARY.md'
}

def vault_filename(name):
    """Avoid .md.md double extension for files that are already markdown."""
    return name if name.endswith('.md') else f"{name}.md"

def extract_python_summary(content):
    """Extracts classes, functions, and docstrings from Python content."""
    try:
        tree = ast.parse(content)
        summary = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                summary.append(f"def {node.name}({ast.unparse(node.args)}):")
                if doc: summary.append(f"    \"\"\"{doc}\"\"\"")
            elif isinstance(node, ast.ClassDef):
                summary.append(f"class {node.name}:")
                class_doc = ast.get_docstring(node)
                if class_doc: summary.append(f"    \"\"\"{class_doc}\"\"\"")
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_doc = ast.get_docstring(item)
                        summary.append(f"    def {item.name}({ast.unparse(item.args)}):")
                        if method_doc: summary.append(f"        \"\"\"{method_doc}\"\"\"")
        return "\n".join(summary)
    except:
        return content[:500] + "... (Parsing failed)"

def extract_ts_summary(content):
    """Simple heuristic for TS/TSX summaries (extracting interfaces, types, functions)."""
    summary = []
    # Extract interfaces, types, functions (very basic regex)
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if any(line.startswith(p) for p in ['export interface', 'export type', 'export const', 'export function', 'export default function']):
            # Remove the body if it's a one-liner or just keep the head
            summary.append(line.split('{')[0].strip())
    return "\n".join(summary) if summary else "Component/Module structure summary not extracted."

def generate_markdown(source_path, relative_path):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ext = os.path.splitext(source_path)[1].lower()
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    header = f"""---
status: Synced
last_sync: "{now}"
original_path: "{relative_path.replace('\\', '/')}"
---
# {os.path.basename(source_path)}

"""
    if ext == '.md':
        return header + content
    elif ext == '.py':
        summary = extract_python_summary(content)
        return header + f"## Python Structure Summary\n\n```python\n{summary}\n```\n"
    elif ext in ['.ts', '.tsx']:
        summary = extract_ts_summary(content)
        return header + f"## TypeScript Structure Summary\n\n```typescript\n{summary}\n```\n"
    elif ext in ['.sql']:
        # For SQL, just keep the top (potential migration summary)
        return header + f"## SQL Migration Summary\n\n```sql\n{content[:1000]}\n```\n"
    else:
        return header + f"Content summary for {ext} not implemented. Original path: `{relative_path}`"

class SyncVault:
    """Manages vault synchronization and commit tracking."""

    def __init__(self, source_dir=SOURCE_DIR, vault_dir=VAULT_DIR):
        """Initialize SyncVault with directory paths.

        Args:
            source_dir: Root source directory for sync operations.
            vault_dir: Target vault directory.
        """
        self.source_dir = source_dir
        self.vault_dir = vault_dir
        self.last_sync_time = None
        self.synced_files = []

    def track_sync(self, file_path: str) -> None:
        """Track a file that was synced.

        Args:
            file_path: Absolute path to the synced file.
        """
        self.synced_files.append(file_path)
        self.last_sync_time = datetime.datetime.now()

    def track_commit(self, commit_hash: str) -> dict:
        """Update frontmatter of recently synced files with commit tracking.

        Updates all files synced within the last 5 minutes with:
        - synced_at_commit: commit hash
        - synced_at_time: ISO format timestamp

        Args:
            commit_hash: Git commit hash to record.

        Returns:
            Dictionary with keys:
                - files_updated (int): Number of files updated
                - last_sync_time (str): ISO format timestamp
                - commit_hash (str): The commit hash recorded
        """
        if not self.synced_files:
            return {
                "files_updated": 0,
                "last_sync_time": datetime.datetime.now().isoformat(),
                "commit_hash": commit_hash,
            }

        now = datetime.datetime.now()
        five_minutes_ago = now - datetime.timedelta(minutes=5)
        files_updated = 0

        for file_path in self.synced_files:
            if not os.path.exists(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue

            # Parse YAML frontmatter
            if not content.startswith('---'):
                continue

            lines = content.split('\n')
            end_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_idx = i
                    break

            if end_idx == -1:
                continue

            # Extract frontmatter and body
            frontmatter_lines = lines[1:end_idx]
            body_lines = lines[end_idx + 1:]

            # Update or add tracking fields
            updated_lines = []
            found_commit = False
            found_time = False

            for line in frontmatter_lines:
                if line.startswith('synced_at_commit:'):
                    updated_lines.append(f'synced_at_commit: "{commit_hash}"')
                    found_commit = True
                elif line.startswith('synced_at_time:'):
                    updated_lines.append(f'synced_at_time: "{now.isoformat()}"')
                    found_time = True
                else:
                    updated_lines.append(line)

            if not found_commit:
                updated_lines.append(f'synced_at_commit: "{commit_hash}"')
            if not found_time:
                updated_lines.append(f'synced_at_time: "{now.isoformat()}"')

            # Reconstruct file
            new_content = '---\n' + '\n'.join(updated_lines) + '\n---\n' + '\n'.join(body_lines)

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_updated += 1
            except Exception:
                continue

        # Clear synced files list after tracking
        self.synced_files = []

        return {
            "files_updated": files_updated,
            "last_sync_time": now.isoformat(),
            "commit_hash": commit_hash,
        }


def validate_config() -> dict:
    """Validate .env.example against backend/config.py environment variables.

    Scans backend/config.py for all os.getenv("KEY") calls and checks if each
    KEY exists in .env.example. Returns configuration validation status.

    Returns:
        Dictionary with keys:
            - config_valid (bool): True if all env vars are accounted for
            - missing_keys (list[str]): Keys in config.py but not in .env.example
            - extra_keys (list[str]): Keys in .env.example but not in config.py
            - issues (list[str]): Human-readable issue descriptions
    """
    config_py_path = os.path.join(SOURCE_DIR, 'backend', 'config.py')
    env_example_path = os.path.join(SOURCE_DIR, '.env.example')

    result = {
        "config_valid": True,
        "missing_keys": [],
        "extra_keys": [],
        "issues": [],
    }

    # Read backend/config.py
    try:
        with open(config_py_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
    except FileNotFoundError:
        result["issues"].append(f"Config file not found: {config_py_path}")
        result["config_valid"] = False
        return result
    except Exception as e:
        result["issues"].append(f"Error reading config.py: {str(e)}")
        result["config_valid"] = False
        return result

    # Extract all os.getenv("KEY") calls
    # Pattern: os.getenv("KEY") or os.getenv('KEY')
    import re
    pattern = r'os\.getenv\(["\']([^"\']+)["\']\)'
    config_keys = set(re.findall(pattern, config_content))

    # Also check for Field aliases in pydantic models
    alias_pattern = r'alias=["\']([^"\']+)["\']'
    alias_keys = set(re.findall(alias_pattern, config_content))
    config_keys.update(alias_keys)

    # Read .env.example
    try:
        with open(env_example_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    except FileNotFoundError:
        result["issues"].append(f"Environment file not found: {env_example_path}")
        result["config_valid"] = False
        return result
    except Exception as e:
        result["issues"].append(f"Error reading .env.example: {str(e)}")
        result["config_valid"] = False
        return result

    # Extract all KEY= entries from .env.example
    env_pattern = r'^([A-Z_][A-Z0-9_]*)='
    env_keys = set(re.findall(env_pattern, env_content, re.MULTILINE))

    # Find discrepancies
    missing = config_keys - env_keys
    extra = env_keys - config_keys

    if missing:
        result["missing_keys"] = sorted(list(missing))
        result["config_valid"] = False
        for key in missing:
            result["issues"].append(f"Key in config.py but not in .env.example: {key}")

    if extra:
        result["extra_keys"] = sorted(list(extra))
        for key in extra:
            result["issues"].append(f"Key in .env.example but not in config.py: {key}")

    return result


def sync():
    print(f"Refining Vault (Summarization Mode): {VAULT_DIR}")
    os.makedirs(MGMT_DIR, exist_ok=True)

    vault_sync = SyncVault()
    current_vault_files = set()

    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            source_path = os.path.join(root, file)
            rel_path = os.path.relpath(source_path, SOURCE_DIR)

            if os.path.splitext(file)[1].lower() in EXCLUDE_EXTS:
                continue

            # Route to Management or Vault
            if rel_path in DOC_FILES_TO_MGMT:
                target_path = os.path.join(MGMT_DIR, 'Plans', vault_filename(file))
            else:
                is_valid = any(rel_path.replace('\\', '/').startswith(p) for p in [
                    'backend/', 'frontend/', 'supabase/', 'remotion/', '.claude/'
                ])
                if not is_valid: continue
                target_path = os.path.join(VAULT_DIR, vault_filename(rel_path))

            current_vault_files.add(os.path.normpath(target_path))

            # Incremental Check
            if os.path.exists(target_path):
                if os.path.getmtime(source_path) <= os.path.getmtime(target_path):
                    continue

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            md_content = generate_markdown(source_path, rel_path)
            if md_content:
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                vault_sync.track_sync(target_path)
                print(f"Summarized: {rel_path}")

    # Cleanup Mode: Remove root-level duplicates in the vault that moved to management
    for doc in DOC_FILES_TO_MGMT:
        dup = os.path.join(VAULT_DIR, vault_filename(doc))
        if os.path.exists(dup):
            os.remove(dup)
            print(f"Cleaned redundant vault copy: {doc}.md")

    print(f"\nVault refinement complete.")

if __name__ == "__main__":
    sync()
