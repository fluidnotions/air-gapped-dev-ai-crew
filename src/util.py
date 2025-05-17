import json
import logging
import sys
import threading
from pathlib import Path
import os
import glob
from typing import Dict, Any

SETTING_FILENAME: str = "settings.json"

file_handlers: Dict[str, logging.FileHandler] = {}
file_handler_lock = threading.Lock()  # Ensures thread-safe creation of file handlers
logging.basicConfig(level=logging.DEBUG, force=True)
SETTINGS: Dict[str, Any] = {}


def get_project_root(marker: str = "README.md") -> Path:
    """
    Walk upwards starting from the directory where this file (utils.py) resides,
    until a file named 'marker' is found. Return that directory as the project root.
    If not found, the search stops at the filesystem root.
    """
    current_script = Path(__file__).resolve()
    candidate = current_script
    while candidate != candidate.parent:
        if (candidate / marker).exists():
            return candidate
        candidate = candidate.parent
    return candidate  # returns filesystem root if not found


def get_file_path(filename: str) -> Path:
    file_path = get_project_root().joinpath(filename).resolve()
    return file_path


def load_json(filename: str) -> Dict[str, Any]:
    """
    Loads JSON from a file and returns it as a dictionary.
    Returns an empty dict if the file does not exist or JSON is invalid.
    """
    path = Path(get_file_path(filename)).resolve()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON from %s. Returning empty dict.", path)
            return {}
    return {}


# Load settings from the default JSON file
SETTINGS.update(load_json(SETTING_FILENAME))


def get_config() -> Dict[str, Any]:
    """
    Build a dict from SETTINGS, extracting key parts if they contain a dot.
    If a key does not contain a dot, it is left as is.
    """
    config_dict = {}
    for k, v in SETTINGS.items():
        parts = k.split('.', maxsplit=1)
        if len(parts) == 2:
            config_dict[parts[1]] = v
        else:
            config_dict[k] = v
    return config_dict


def save_json(filename: str, data: Dict[str, Any]) -> None:
    """
    Saves a dictionary to a JSON file with pretty-printing.
    """
    path = Path(filename).resolve()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_config_value(path: str, default: Any = None) -> Any:
    """
    Retrieves a value from the config dictionary given a dot-notation path.
    Returns 'default' if the path or a sub-path does not exist.
    """
    keys = path.split(".")
    current = get_config()
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def clear_logs():
    """
    Removes all *.log files under the 'logs' directory. If removal fails,
    it logs an error but continues.
    """
    directory = str(get_file_path('logs').absolute())
    log_files = glob.glob(directory + '/*.log')
    for log_file in log_files:
        try:
            os.remove(log_file)
        except OSError as e:
            logging.error("Could not remove log file %s: %s", log_file, e)


def _get_file_logger_handler(filename: str) -> logging.FileHandler:
    """
    Creates or retrieves a file handler for the specified filename
    in a thread-safe way.
    """
    with file_handler_lock:
        handler = file_handlers.get(filename, None)
        if handler is None:
            handler = logging.FileHandler(filename, encoding="utf-8")
            file_handlers[filename] = handler
    return handler


def to_snake_case(text: str) -> str:
    """
    Converts a class name or text to snake_case, for naming log files, etc.
    """
    import re
    words = re.findall(r'[a-z]+|[A-Z][a-z]*', text)
    return '_'.join(word.lower() for word in words)


def get_logger(cls: object) -> logging.Logger:
    """
    Returns a logger that writes records into a class-based file name.
    """
    name = cls.__class__.__name__
    log_file_path = get_file_path(f'logs/{to_snake_case(name)}.log').absolute()
    filename = str(log_file_path)
    log_formatter = logging.Formatter(
        '[%(asctime)s][%(threadName)s](%(levelname)s) %(name)s: %(message)s'
    )
    logger = logging.getLogger(name)
    handler = _get_file_logger_handler(filename)
    handler.setFormatter(log_formatter)
    # Avoid adding duplicate handlers to the same logger
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == handler.baseFilename
               for h in logger.handlers):
        logger.addHandler(handler)
    return logger