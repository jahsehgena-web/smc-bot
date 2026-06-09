# evaluator.py

import time
from engine import signal_queue
from logger import SignalLogger

logger = SignalLogger()

def evaluate_signal(signal):
    print(f"📊 Evaluating: {signal['pair']} {signal['signal']}")

    # SIMPLE MOCK EVALUATION LOGIC
    # replace with your real price checking later

    result = signal
    result["status"] = "EXECUTED"

    logger.log(result)

    print(f"✅ Evaluated + logged: {signal['pair']}")
    return result


def run_evaluator():
    print("📊 Evaluator started")

    while True:
        if not signal_queue.empty():
            signal = signal_queue.get()
            evaluate_signal(signal)

        time.sleep(2)
