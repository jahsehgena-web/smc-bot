import time
from logger import log_signal

SIGNAL_CACHE = {}
COOLDOWN = 900  # 15 min

def is_duplicate(signal):
    key = f"{signal['pair']}_{signal['signal']}"
    now = time.time()

    if key in SIGNAL_CACHE:
        if now - SIGNAL_CACHE[key] < COOLDOWN:
            return True

    SIGNAL_CACHE[key] = now
    return False


def process_signal(signal):
    if is_duplicate(signal):
        print("⛔ Duplicate blocked")
        return

    log_signal(signal)
    print(f"📨 SIGNAL: {signal['pair']} {signal['signal']}")
