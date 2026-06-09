"""
====================================================
SMC ENGINE v2.1 — FIXED VERSION
- Removes duplicate signal spam
- Adds proper cooldown cache
- Clean single-file engine (Railway safe)
====================================================
"""

import time
from datetime import datetime, timezone

# ==============================================
# SIGNAL CACHE (FIX: stops spam)
# ==============================================
SIGNAL_CACHE = {}
SIGNAL_TTL = 900  # 15 minutes

def is_duplicate_signal(pair, signal_type, price):
    key = f"{pair}_{signal_type}"
    now = time.time()

    if key in SIGNAL_CACHE:
        last_time, last_price = SIGNAL_CACHE[key]

        # cooldown window
        if now - last_time < SIGNAL_TTL:
            return True

        # prevent micro-spam at same level
        if abs(price - last_price) / price < 0.0005:
            return True

    SIGNAL_CACHE[key] = (now, price)
    return False


# ==============================================
# ENGINE STATE (used by main.py)
# ==============================================
ENGINE_TICK = 0


def engine_alive_tick():
    global ENGINE_TICK
    ENGINE_TICK += 1
    print(f"🔎 Engine alive tick: {ENGINE_TICK}")


# ==============================================
# PLACEHOLDER ANALYSIS FUNCTION
# (Your real logic already exists in main bot)
# This just ensures import NEVER breaks again
# ==============================================
def analyze_placeholder():
    return None


# ==============================================
# MONITOR LOOP (SAFE VERSION FOR RAILWAY)
# ==============================================
def monitor_with_logging():
    """
    IMPORTANT:
    This version ONLY proves engine is alive.
    Your real analyze() stays in main.py.
    """
    print("🚀 Engine monitor started...")

    while True:
        try:
            engine_alive_tick()
            time.sleep(10)

        except Exception as e:
            print(f"Engine error: {e}")
            time.sleep(5)
