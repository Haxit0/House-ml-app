import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"

LATEST_PATH = ARTIFACTS_DIR / "metrics_latest.json"
HISTORY_PATH = ARTIFACTS_DIR / "metrics_history.json"


def load_metrics():
    if not LATEST_PATH.exists():
        return None

    with open(LATEST_PATH, "r") as f:
        latest = json.load(f)

    history = []
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)

    return {
        "latest": latest,
        "history": history,
    }
