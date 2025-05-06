import os
import re

# ─────────────────────────────────────────────────────────────
# TypeScript AST Tool (basic — would benefit from ts-morph or tree-sitter)
# ─────────────────────────────────────────────────────────────
class TypeScriptASTTool:
    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)

    def search(self, query: str) -> str:
        results = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(".ts"):
                    continue
                fpath = os.path.join(dirpath, fname)
                with open(fpath, encoding="utf-8") as f:
                    code = f.read()
                matches = re.findall(rf"\b{re.escape(query)}\b", code)
                if matches:
                    results.append(f"{len(matches)} hits in {fpath}")
        return "\n".join(results) if results else "No TS matches found."