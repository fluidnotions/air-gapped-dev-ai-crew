import os


# ─────────────────────────────────────────────────────────────
# PHP AST Tool (basic grep-style for now)
# ─────────────────────────────────────────────────────────────
class PHPASTTool:
    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)

    def search(self, query: str) -> str:
        results = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(".php"):
                    continue
                fpath = os.path.join(dirpath, fname)
                with open(fpath, encoding="utf-8") as f:
                    code = f.read()
                if query.lower() in code.lower():
                    results.append(f"Found in {fpath}")
        return "\n".join(results) if results else "No PHP matches found."
