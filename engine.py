import numpy as np
import yfinance as yf

# =========================
# DATA
# =========================
def get_data(symbol="GC=F", interval="15m", period="5d"):
    df = yf.download(symbol, interval=interval, period=period, progress=False)
    if df is None or len(df) < 50:
        return None
    return df.dropna()

# =========================
# SWINGS
# =========================
def get_swings(df, lookback=20):
    highs = df["High"].values[-lookback:]
    lows  = df["Low"].values[-lookback:]

    swing_highs = []
    swing_lows = []

    for i in range(2, len(highs) - 2):
        if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1]:
            swing_highs.append(highs[i])

        if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1]:
            swing_lows.append(lows[i])

    return swing_highs, swing_lows

# =========================
# STRUCTURE
# =========================
def detect_structure(df):
    swing_highs, swing_lows = get_swings(df)

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    last_high = swing_highs[-1]
    prev_high = swing_highs[-2]
    last_low = swing_lows[-1]
    prev_low = swing_lows[-2]

    close = df["Close"].iloc[-1]

    if close > last_high:
        return "bullish_bos"

    if close < last_low:
        return "bearish_bos"

    if last_high < prev_high and close < last_low:
        return "bearish_choch"

    if last_low > prev_low and close > last_high:
        return "bullish_choch"

    return None

# =========================
# LIQUIDITY
# =========================
def liquidity_sweep(df):
    highs = df["High"].values
    lows = df["Low"].values
    close = df["Close"].iloc[-1]

    recent_high = np.max(highs[-20:])
    recent_low = np.min(lows[-20:])

    if highs[-1] > recent_high and close < recent_high:
        return "bearish"

    if lows[-1] < recent_low and close > recent_low:
        return "bullish"

    return None

# =========================
# SIGNAL ENGINE (THIS IS WHAT MAIN CALLS)
# =========================
def generate_signal(symbol="GC=F", pair="GOLD"):
    df = get_data(symbol)
    if df is None:
        return None

    structure = detect_structure(df)
    sweep = liquidity_sweep(df)

    price = float(df["Close"].iloc[-1])

    if structure in ["bullish_bos", "bullish_choch"] and sweep == "bullish":
        return {
            "pair": pair,
            "signal": "BUY",
            "price": price,
            "sl": price - 10,
            "tp1": price + 10,
            "tp2": price + 20,
            "rr": 2.0,
            "score": 80,
            "structure": structure,
            "h1_bias": "bullish"
        }

    if structure in ["bearish_bos", "bearish_choch"] and sweep == "bearish":
        return {
            "pair": pair,
            "signal": "SELL",
            "price": price,
            "sl": price + 10,
            "tp1": price - 10,
            "tp2": price - 20,
            "rr": 2.0,
            "score": 80,
            "structure": structure,
            "h1_bias": "bearish"
        }

    return None
