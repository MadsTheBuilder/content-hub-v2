import os
import datetime
import shutil
import ast
import re

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

def sync():
    print(f"Refining Vault (Summarization Mode): {VAULT_DIR}")
    os.makedirs(MGMT_DIR, exist_ok=True)
    
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
