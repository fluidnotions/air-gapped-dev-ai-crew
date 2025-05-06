import os
import javalang


# ─────────────────────────────────────────────────────────────
# Java AST Tool
# ─────────────────────────────────────────────────────────────
class JavaASTTool:
    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)

    def search(self, query: str) -> str:
        matches = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(".java"):
                    continue
                fpath = os.path.join(dirpath, fname)
                try:
                    code = open(fpath, encoding="utf-8").read()
                    tree = javalang.parse.parse(code)
                except Exception:
                    continue

                for cls in tree.types:
                    if not isinstance(cls, javalang.tree.ClassDeclaration):
                        continue
                    for method in cls.methods:
                        if method.body is None:
                            continue
                        for _, node in method.filter(javalang.tree.MethodInvocation):
                            if query.lower() in node.member.lower():
                                matches.append(f"{cls.name}.{method.name} in {fpath} (line {method.position.line})")
        return "\n".join(matches) if matches else "No matching method invocations found."




