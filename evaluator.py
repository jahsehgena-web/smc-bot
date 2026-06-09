import time
import yfinance as yf
from datetime import datetime, timezone
from logger import SignalLogger

class SignalEvaluator:
    def __init__(self, logger: SignalLogger):
        self.logger = logger

    def get_price(self, symbol):
        try:
            df = yf.download(symbol, interval="5m", period="1d", progress=False)
            if df is not None and not df.empty:
                return float(df["Close"].iloc[-1])
        except:
            return None

    def evaluate(self, signal):
        symbol = signal["symbol"]
        price = self.get_price(symbol)

        if price is None:
            return

        entry = signal["entry"]
        sl    = signal["sl"]
        tp1   = signal["tp1"]
        tp2   = signal["tp2"]

        outcome = None

        # BUY logic
        if signal["type"] == "BUY":
            if price <= sl:
                outcome = "SL"
            elif price >= tp2:
                outcome = "TP2"
            elif price >= tp1:
                outcome = "TP1"

        # SELL logic
        if signal["type"] == "SELL":
            if price >= sl:
                outcome = "SL"
            elif price <= tp2:
                outcome = "TP2"
            elif price <= tp1:
                outcome = "TP1"

        if outcome:
            self.logger.update_status(signal["id"], outcome)
            print(f"[EVALUATED] {symbol} #{signal['id']} -> {outcome}")

    def run(self):
        print("[EVALUATOR STARTED]")

        while True:
            open_signals = self.logger.get_open_signals()

            for signal in open_signals:
                self.evaluate(signal)

            time.sleep(60)
