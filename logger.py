import json
import time
from datetime import datetime, timezone

class SignalLogger:
    def __init__(self, file_name="signals.json"):
        self.file_name = file_name
        self.signals = self._load()

    def _load(self):
        try:
            with open(self.file_name, "r") as f:
                return json.load(f)
        except:
            return []

    def _save(self):
        with open(self.file_name, "w") as f:
            json.dump(self.signals, f, indent=2)

    def log_signal(self, signal):
        entry = {
            "id": len(self.signals) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbol": signal["symbol"],
            "type": signal["type"],
            "entry": signal["price"],
            "sl": signal["sl"],
            "tp1": signal["tp1"],
            "tp2": signal["tp2"],
            "score": signal["score"],
            "status": "OPEN"
        }

        self.signals.append(entry)
        self._save()

        print(f"[LOGGED] {entry['symbol']} {entry['type']} #{entry['id']}")
        return entry["id"]

    def update_status(self, signal_id, status):
        for s in self.signals:
            if s["id"] == signal_id:
                s["status"] = status
                break
        self._save()

    def get_open_signals(self):
        return [s for s in self.signals if s["status"] == "OPEN"]
