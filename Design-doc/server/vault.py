"""Vault file reader.

Exposes three operations used by /api/vault/* endpoints:
  - recent(folder, limit)  — newest .md files in a vault subfolder
  - read_file(path)        — raw markdown content
  - outputs(path)          — list members of a bundle directory or single file

All path inputs are validated against VAULT_ROOT before any file access
(path-traversal guard).
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent
VAULT_ROOT = (PROJECT_ROOT / "Content-Hub-Vault-V2").resolve()


def _safe_resolve(path_str: str) -> Optional[Path]:
    """Return resolved Path only if it falls inside VAULT_ROOT, else None."""
    try:
        p = Path(path_str)
        if not p.is_absolute():
            p = VAULT_ROOT / p
        resolved = p.resolve()
        if not str(resolved).startswith(str(VAULT_ROOT)):
            return None
        return resolved
    except Exception:
        return None


def recent(folder: str, limit: int = 10, subfolders_only: bool = False) -> list[dict]:
    """List the most-recently-modified .md files in a vault subfolder.

    Searches both direct children and one level of subdirectories so that
    researcher outputs written to dated subfolders (e.g. 10-Research/2026-05-06_ruflo/)
    appear alongside flat _brief.md files.

    subfolders_only: when True, skip top-level .md files and only include files
    from one-level-deep subdirectories (used for 04-Trends repo pickers).
    """
    target = VAULT_ROOT / folder
    if not target.exists() or not target.is_dir():
        return []
    all_md: list[Path] = []
    for item in target.iterdir():
        if not subfolders_only and item.is_file() and item.suffix == ".md":
            all_md.append(item)
        elif item.is_dir():
            for sub in item.iterdir():
                if sub.is_file() and sub.suffix == ".md":
                    all_md.append(sub)
    files = sorted(all_md, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    return [
        {
            "name": f.relative_to(target).as_posix() if f.parent != target else f.name,
            "path": str(f),
            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
        }
        for f in files
    ]


def read_file(path_str: str) -> Optional[str]:
    """Read a vault file's raw markdown. Returns None if path is unsafe or missing."""
    resolved = _safe_resolve(path_str)
    if not resolved or not resolved.exists() or not resolved.is_file():
        return None
    return resolved.read_text(encoding="utf-8", errors="replace")


def outputs(path_str: str) -> list[dict]:
    """List readable members for a bundle directory or single file."""
    resolved = _safe_resolve(path_str)
    if not resolved:
        return []
    if resolved.is_dir():
        files = sorted(
            [f for f in resolved.iterdir() if f.is_file() and f.suffix == ".md"],
            key=lambda p: p.name,
        )
        return [{"name": f.name, "path": str(f)} for f in files]
    if resolved.is_file():
        return [{"name": resolved.name, "path": str(resolved)}]
    return []
