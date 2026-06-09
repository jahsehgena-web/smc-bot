import json
from datetime import datetime, timezone

FILE = "signals.json"

def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_signal(signal):
    data = load()

    entry = {
        **signal,
        "id": len(data) + 1,
        "time": datetime.now(timezone.utc).isoformat(),
        "status": "PENDING"
    }

    data.append(entry)
    save(data)

    print(f"📝 Logged #{entry['id']} {entry['pair']} {entry['signal']}")
