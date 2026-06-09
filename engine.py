"""
====================================================
  ENGINE.PY — STABLE SMC ENGINE (RAILWAY SAFE)
====================================================
"""

import time
import traceback

# ==================================================
# OPTIONAL IMPORTS (SAFE FALLBACKS)
# ==================================================

try:
    from logger import signal_logger
except:
    signal_logger = None

try:
    from main import analyze
except:
    analyze = None


# ==================================================
# CORE MONITOR LOOP
# ==================================================

def monitor():
    """
    Main engine loop.
    This MUST run continuously on Railway.
    """

    print("🚀 Engine monitor started...")

    # safety counters so you can SEE activity
    tick = 0

    while True:
        try:
            tick += 1

            # -------------------------------------------------
            # PROOF THE ENGINE IS ALIVE (VISIBLE HEARTBEAT)
            # -------------------------------------------------
            print(f"🔎 Engine alive tick: {tick}")

            # -------------------------------------------------
            # IF ANALYZE FUNCTION EXISTS, RUN IT SAFELY
            # -------------------------------------------------
            if analyze:
                try:
                    # NOTE:
                    # You MUST replace symbols list if needed
                    symbols = ["XAUUSD=X", "EURUSD=X"]

                    for symbol in symbols:
                        result = analyze(symbol, symbol.replace("=X", ""))

                        if result:
                            print(f"📊 Signal detected: {result['signal']} {result['pair']}")

                            # log if logger exists
                            if signal_logger:
                                signal_logger.log_signal(result)

                except Exception as inner:
                    print("⚠️ Analysis error:")
                    print(traceback.format_exc())

            time.sleep(10)

        except Exception as e:
            print("❌ Monitor crash (handled):")
            print(traceback.format_exc())
            time.sleep(5)


# ==================================================
# RAILWAY ENTRY POINT (CRITICAL)
# ==================================================

def monitor_with_logging():
    """
    Railway-safe entry function.
    NEVER crashes import.
    """

    try:
        monitor()

    except Exception as e:
        print("❌ Fatal engine error:")
        print(traceback.format_exc())

        # keep container alive
        while True:
            time.sleep(10)
