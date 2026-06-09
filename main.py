import os
import time
import threading
import telebot

from logger import SignalLogger
from evaluator import SignalEvaluator
from engine import analyze

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
logger = SignalLogger()

PAIRS = {
    "EURUSD=X": "EURUSD",
    "GBPUSD=X": "GBPUSD",
    "BTC-USD": "BTCUSD",
    "XAUUSD=X": "GOLD"
}

def fetch(symbol):
    import yfinance as yf
    df = yf.download(symbol, interval="15m", period="5d")
    return df

def monitor():
    while True:
        for symbol, name in PAIRS.items():
            df = fetch(symbol)
            if df is None or df.empty:
                continue

            signal = analyze(df, name)

            if signal:
                logger.log_signal(signal)
                bot.send_message(CHAT_ID, f"📊 SIGNAL\n{signal}")

        time.sleep(60)

evaluator = SignalEvaluator(logger, fetch, bot, CHAT_ID)

threading.Thread(target=monitor, daemon=True).start()
threading.Thread(target=evaluator.run, daemon=True).start()

bot.infinity_polling()
