import os
import subprocess
from pathlib import Path
from src.util import get_logger, get_config

class UpdateContextFiles:
    def __init__(self):
        self.logger = get_logger(self)
        self.config = get_config()

    def update_git_repos(self, base_dir: Path) -> None:
        """
        Updates the Git repositories within the specified directory by
        fetching and pulling changes from remote.
        """
        self.logger.info(f"\n🔄 Updating Git repositories in: {base_dir}")
        for repo_dir in base_dir.iterdir():
            if not repo_dir.is_dir():
                continue
            git_dir = repo_dir / ".git"
            if git_dir.exists():
                self.logger.info(f"📁 {repo_dir.name}: Fetching + pulling latest changes")
                try:
                    subprocess.run(["git", "-C", str(repo_dir), "fetch"], check=True)
                    subprocess.run(["git", "-C", str(repo_dir), "pull"], check=True)
                except subprocess.CalledProcessError as e:
                    self.logger.warning(f"⚠️ Failed to update {repo_dir.name}: {e}")
            else:
                self.logger.info(f"🚫 {repo_dir.name} is not a Git repository")

    def fetch_slack_messages(self) -> None:
        """
        Invokes an external script to download Slack messages.
        """
        self.logger.info("\n📥 Fetching Slack messages using external tool")
        if not SLACK_BIN.exists():
            self.logger.warning("⚠️ Slack export script not found. "
                                "Clone https://github.com/dmitryrck/slack-export and configure it.")
            return

        try:
            subprocess.run(["python", str(SLACK_BIN)], cwd=SLACK_BIN.parent, check=True)
            self.logger.info("✅ Slack messages downloaded")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Slack export failed: {e}")

    def run(self) -> None:
        """
        High-level method that invokes updates for code repositories and fetches Slack messages.
        """
        self.update_git_repos(CODE_DIR)
        self.update_git_repos(DOCS_DIR)
        self.fetch_slack_messages()


if __name__ == "__main__":
    updater = UpdateContextFiles()
    updater.run()
