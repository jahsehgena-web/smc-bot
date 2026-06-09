# engine.py

import time
import threading
from queue import Queue

signal_queue = Queue()

def generate_signal_mock():
    """
    Replace this with your real analyze() function output.
    This is just structure fix.
    """
    return {
        "pair": "GOLD",
        "signal": "BUY",
        "price": 2000,
        "sl": 1985,
        "tp1": 2020,
        "tp2": 2040,
        "rr": 2.5,
        "score": 82,
        "session": "London",
        "structure": "bullish_bos",
        "h1_bias": "bullish",
        "checks": 6
    }

def monitor_engine():
    print("🚀 Engine monitor started...")

    tick = 0

    while True:
        tick += 1
        print(f"🔎 Engine alive tick: {tick}")

        signal = generate_signal_mock()

        # only push valid signals
        if signal:
            signal_queue.put(signal)
            print(f"📥 Signal queued: {signal['pair']} {signal['signal']}")

        time.sleep(10)
