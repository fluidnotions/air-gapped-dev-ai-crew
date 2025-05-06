import os

# ─────────────────────────────────────────────────────────────
# Go AST Tool (dummy stub — real version needs go/parser or gopls)
# ─────────────────────────────────────────────────────────────
class GoASTTool:
    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)

    def search(self, query: str) -> str:
        results = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(".go"):
                    continue
                fpath = os.path.join(dirpath, fname)
                with open(fpath, encoding="utf-8") as f:
                    code = f.read()
                if query.lower() in code.lower():
                    results.append(f"Possible match in {fpath}")
        return "\n".join(results) if results else "No Go matches found."