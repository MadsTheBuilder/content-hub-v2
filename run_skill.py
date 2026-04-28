import os
import sys
import subprocess
import re

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_FILE = os.path.join(BASE_DIR, "Content-Hub-Vault", "00-Management", "Plans", "skill.md")

def parse_skills():
    if not os.path.exists(SKILL_FILE):
        print(f"Error: skill.md not found at {SKILL_FILE}")
        return {}
    
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple regex to split by ## Skill Name
    skills = {}
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    for section in sections:
        if not section.strip(): continue
        lines = section.split('\n')
        skill_name = lines[0].strip()
        
        # Extract the first bash code block
        code_blocks = re.findall(r'```bash\n(.*?)\n```', section, re.DOTALL)
        if code_blocks:
            skills[skill_name] = code_blocks[0]
            
    return skills

def run_skill(skill_name):
    skills = parse_skills()
    if skill_name not in skills:
        print(f"Error: Skill '{skill_name}' not found. Available skills: {', '.join(skills.keys())}")
        return
    
    commands = skills[skill_name].split('\n')
    print(f"--- Executing Skill: {skill_name} ---")
    
    for cmd in commands:
        cmd = cmd.strip()
        if not cmd or cmd.startswith('#'): continue
        
        # Handle custom Cwd comments if present (e.g. # Cwd: path)
        cwd = BASE_DIR
        if "# Cwd: " in cmd:
            parts = cmd.split("# Cwd: ")
            cmd = parts[0].strip()
            cwd = parts[1].strip()
        
        print(f"Running: {cmd} (in {cwd})")
        try:
            # We use shell=True to handle multiple commands or pipe-like syntax in the bash blocks
            subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with exit code {e.returncode}")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_skill.py <skill_name>")
        skills = parse_skills()
        print(f"Available skills: {', '.join(skills.keys()) if skills else 'None'}")
    else:
        run_skill(sys.argv[1])
