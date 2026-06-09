# main.py

import threading
from engine import monitor_engine
from evaluator import run_evaluator

print("🚀 System starting...")

t1 = threading.Thread(target=monitor_engine, daemon=True)
t2 = threading.Thread(target=run_evaluator, daemon=True)

t1.start()
t2.start()

print("✅ System running...")

while True:
    pass
