import os
import subprocess
from pathlib import Path








# --- CODE REPOS ---
def update_git_repos(base_dir):
    print("\n🔄 Updating Git repositories in:", base_dir)
    for repo_dir in base_dir.iterdir():
        if not repo_dir.is_dir():
            continue
        git_dir = repo_dir / ".git"
        if git_dir.exists():
            print(f"📁 {repo_dir.name}: Fetching + pulling latest changes")
            try:
                subprocess.run(["git", "-C", str(repo_dir), "fetch"], check=True)
                subprocess.run(["git", "-C", str(repo_dir), "pull"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Failed to update {repo_dir.name}: {e}")
        else:
            print(f"🚫 {repo_dir.name} is not a Git repository")


# --- SLACK DOWNLOAD ---
def fetch_slack_messages():
    print("\n📥 Fetching Slack messages using external tool")
    if not SLACK_DLP_SCRIPT.exists():
        print("⚠️ Slack export script not found. Clone https://github.com/dmitryrck/slack-export and configure it.")
        return

    try:
        subprocess.run(["python", str(SLACK_DLP_SCRIPT)], cwd=SLACK_DLP_SCRIPT.parent, check=True)
        print("✅ Slack messages downloaded")
    except subprocess.CalledProcessError as e:
        print(f"❌ Slack export failed: {e}")


# --- MAIN ---
if __name__ == "__main__":
    update_git_repos(CODE_DIR)
    update_git_repos(DOCS_DIR)
    fetch_slack_messages()
