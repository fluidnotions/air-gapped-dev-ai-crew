import os
import subprocess
from pathlib import Path
from typing import List

# ─────────────────────────────────────────────────────────────
# Git Tool: Switch branch and scan files in repos
# ─────────────────────────────────────────────────────────────
class GitTool:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def checkout_branch(self, repo_name: str, branch: str) -> str:
        repo_path = self.root / repo_name
        if not (repo_path / ".git").exists():
            return f"❌ {repo_name} is not a Git repository."
        try:
            subprocess.run(["git", "-C", str(repo_path), "fetch"], check=True)
            subprocess.run(["git", "-C", str(repo_path), "checkout", branch], check=True)
            return f"✅ Checked out `{branch}` in `{repo_name}`"
        except subprocess.CalledProcessError:
            return f"⚠️ Failed to checkout `{branch}` in `{repo_name}`"

    def grep_file(self, repo_name: str, pattern: str, ext: str = ".ts") -> List[str]:
        repo_path = self.root / repo_name
        results = []
        for dirpath, _, files in os.walk(repo_path):
            for fname in files:
                if not fname.endswith(ext):
                    continue
                try:
                    with open(os.path.join(dirpath, fname), encoding="utf-8") as f:
                        for i, line in enumerate(f, start=1):
                            if pattern.lower() in line.lower():
                                rel_path = os.path.relpath(os.path.join(dirpath, fname), self.root)
                                results.append(f"{rel_path}:{i}: {line.strip()}")
                except Exception:
                    continue
        return results