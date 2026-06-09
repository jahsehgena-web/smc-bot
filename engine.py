import time
from strategy import generate_signal
from execution import process_signal

def monitor_engine():
    print("🚀 SMC Engine started...")

    tick = 0

    while True:
        tick += 1
        print(f"🔎 Engine tick: {tick}")

        signal = generate_signal()

        if signal:
            process_signal(signal)

        time.sleep(10)
