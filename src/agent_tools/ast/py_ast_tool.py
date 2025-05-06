import os
import ast


# ─────────────────────────────────────────────────────────────
# Python AST Tool
# ─────────────────────────────────────────────────────────────
class PyASTTool:
    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)

    def search(self, query: str) -> str:
        results = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                except Exception:
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        func = getattr(node.func, 'id', getattr(node.func, 'attr', ''))
                        if query.lower() in func.lower():
                            results.append(f"Call to `{func}` in {fpath} (line {node.lineno})")
        return "\n".join(results) if results else "No Python call matches found."