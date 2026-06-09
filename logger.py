# logger.py

import json
from datetime import datetime, timezone

LOG_FILE = "signals.json"

class SignalLogger:
    def __init__(self):
        try:
            with open(LOG_FILE, "r") as f:
                self.data = json.load(f)
        except:
            self.data = []

    def save(self):
        with open(LOG_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def log(self, signal):
        entry = {
            **signal,
            "id": len(self.data) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "PENDING"
        }

        self.data.append(entry)
        self.save()

        print(f"📝 Logged signal #{entry['id']}")
        return entry
