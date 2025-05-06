import difflib
import subprocess
from pathlib import Path
from typing import List


class MCMGitDiffTool:
    def __init__(self, repo_path: str, reference_branch: str = "default-integration"):
        self.repo = Path(repo_path)
        self.ref_branch = reference_branch
        assert (self.repo / ".git").exists(), f"Not a valid Git repo: {repo_path}"

    def _checkout_branch(self, branch: str):
        subprocess.run(["git", "-C", str(self.repo), "fetch"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "checkout", branch], check=True)

    def _get_changed_files(self, branch: str) -> List[str]:
        cmd = [
            "git", "-C", str(self.repo), "diff", "--name-only",
            f"origin/{self.ref_branch}...origin/{branch}"
        ]
        output = subprocess.check_output(cmd, text=True).splitlines()
        return [f for f in output if not f.startswith("src/aggregator/channels/") and f.endswith(".ts")]

    def _get_file_from_branch(self, branch: str, filepath: str) -> str:
        cmd = ["git", "-C", str(self.repo), "show", f"origin/{branch}:{filepath}"]
        try:
            return subprocess.check_output(cmd, text=True)
        except subprocess.CalledProcessError:
            return ""

    def diff_to_html(self, target_branch: str, limit: int = 20) -> str:
        changed_files = self._get_changed_files(target_branch)
        html = ["<html><body><h2>⚠️ MCM Drift Report</h2>"]

        for file in changed_files[:limit]:
            before = self._get_file_from_branch(self.ref_branch, file).splitlines()
            after = self._get_file_from_branch(target_branch, file).splitlines()

            if not before and not after:
                continue

            diff = difflib.HtmlDiff().make_table(before, after,
                                                 fromdesc=f"{self.ref_branch}:{file}",
                                                 todesc=f"{target_branch}:{file}")
            html.append(f"<h3>{file}</h3>\n{diff}<hr>")

        html.append("</body></html>")
        return "\n".join(html)


if __name__ == "__main__":
    tool = MCMGitDiffTool("/path/to/mcm-repo")
    html = tool.diff_to_html("domains/ng.mycontent.mobi")
    with open("mcm_diff_report.html", "w") as f:
        f.write(html)
    print("✅ HTML diff report written to mcm_diff_report.html")
