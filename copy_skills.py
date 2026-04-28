import os
import shutil
from pathlib import Path

base_dir = Path(r"c:\Users\madhu\Claude cowork\Content Hub")
skills_dir = base_dir / "tmp_marketingskills" / "skills"
dest_dir = base_dir / "backend" / "prompts" / "skills"
dest_dir.mkdir(parents=True, exist_ok=True)

skills_to_copy = [
    "product-marketing-context", 
    "marketing-psychology", 
    "copywriting", 
    "social-content", 
    "copy-editing"
]

for skill in skills_to_copy:
    src = skills_dir / skill / "SKILL.md"
    dest = dest_dir / f"{skill}.md"
    if src.exists():
        shutil.copy2(src, dest)
        print(f"Success: Copied {skill}.md")
    else:
        print(f"Error: Missing {skill}")
