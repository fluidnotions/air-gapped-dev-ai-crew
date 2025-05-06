import os
import subprocess
import yaml
from pathlib import Path
from typing import List, Optional

# ─────────────────────────────────────────────────────────────
# Kubernetes YAML Tool
# ─────────────────────────────────────────────────────────────
class K8sYAMLTool:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

    def find_metadata(self) -> List[str]:
        findings = []
        for dirpath, _, files in os.walk(self.root):
            for fname in files:
                if not fname.endswith(('.yaml', '.yml')):
                    continue
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, encoding='utf-8') as f:
                        docs = list(yaml.safe_load_all(f))
                    for doc in docs:
                        if not isinstance(doc, dict):
                            continue
                        ns = doc.get('metadata', {}).get('namespace')
                        labels = doc.get('metadata', {}).get('labels')
                        kind = doc.get('kind')
                        name = doc.get('metadata', {}).get('name')
                        if ns or labels:
                            findings.append(f"{kind} `{name}` (ns={ns}, labels={labels}) in {fpath}")
                except Exception:
                    continue
        return findings

    def describe(self, resource: str, namespace: Optional[str] = None) -> str:
        cmd = ["kubectl", "describe", resource]
        if namespace:
            cmd += ["--namespace", namespace]
        try:
            output = subprocess.check_output(cmd, text=True)
            return output.strip()
        except subprocess.CalledProcessError:
            return f"❌ Failed to describe `{resource}`"

    def get(self, resource: str, namespace: Optional[str] = None) -> str:
        cmd = ["kubectl", "get", resource, "-o", "yaml"]
        if namespace:
            cmd += ["--namespace", namespace]
        try:
            output = subprocess.check_output(cmd, text=True)
            return output.strip()
        except subprocess.CalledProcessError:
            return f"❌ Failed to get `{resource}`"