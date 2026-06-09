import threading
import time

from engine import monitor_with_logging
from evaluator import SignalEvaluator
from logger import SignalLogger

logger = SignalLogger()
evaluator = SignalEvaluator(logger)

# =========================
# RUN ENGINE (signals)
# =========================
def run_engine():
    print("🚀 Engine started")
    monitor_with_logging()

# =========================
# RUN EVALUATOR (tracking)
# =========================
def run_evaluator():
    print("📊 Evaluator started")
    evaluator.run()

# =========================
# START SYSTEM
# =========================
if __name__ == "__main__":
    t1 = threading.Thread(target=run_engine)
    t2 = threading.Thread(target=run_evaluator)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
