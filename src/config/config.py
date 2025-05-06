from pathlib import Path

class Config:
    # --- CONFIGURATION ---
    CODE_DIR = Path("/Users/justinrobinson/Documents/hyvemobile/repos")
    DOCS_DIR = Path("/Users/justinrobinson/Documents/knowledge")
    SLACK_EXPORT_DIR = Path("/Users/justinrobinson/Documents/knowledge/slack-context")
    SLACK_DLP_SCRIPT = Path("scripts/fetch_slack_data.py")  # clone of https://github.com/dmitryrck/slack-export