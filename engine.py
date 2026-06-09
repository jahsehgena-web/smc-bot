import time

def monitor_engine():
    print("🚀 Engine monitor started...")

    tick = 0

    while True:
        tick += 1
        print(f"🔎 Engine alive tick: {tick}")
        time.sleep(10)
