import threading
from engine import monitor_engine

def start():
    print("🚀 Engine started")

    threading.Thread(target=monitor_engine, daemon=True).start()

    while True:
        pass  # keep Railway container alive

if __name__ == "__main__":
    start()
