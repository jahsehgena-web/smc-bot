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
# SWING DETECTION (IMPROVED)
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
# MARKET STRUCTURE
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

    # BOS / CHoCH logic
    if close > last_high:
        return "bullish_bos"

    if close < last_low:
        return "bearish_bos"

    # CHoCH (simplified structure shift)
    if last_high < prev_high and close < last_low:
        return "bearish_choch"

    if last_low > prev_low and close > last_high:
        return "bullish_choch"

    return None

# =========================
# LIQUIDITY SWEEP (BASIC BUT REAL)
# =========================
def liquidity_sweep(df):
    highs = df["High"].values
    lows = df["Low"].values
    close = df["Close"].iloc[-1]

    recent_high = np.max(highs[-20:])
    recent_low = np.min(lows[-20:])

    # sweep high then reject
    if highs[-1] > recent_high and close < recent_high:
        return "bearish"

    # sweep low then reject
    if lows[-1] < recent_low and close > recent_low:
        return "bullish"

    return None

# =========================
# ENTRY GENERATOR (SMC CORE)
# =========================
def generate_signal():
    df = get_data()

    if df is None:
        return None

    structure = detect_structure(df)
    sweep = liquidity_sweep(df)

    close = float(df["Close"].iloc[-1])

    # =========================
    # BUY SETUP
    # =========================
    if structure in ["bullish_bos", "bullish_choch"] and sweep == "bullish":
        return {
            "pair": "GOLD",
            "signal": "BUY",
            "price": close,
            "sl": close - 10,
            "tp1": close + 10,
            "tp2": close + 20,
            "rr": 2.0,
            "score": 80,
            "structure": structure,
            "h1_bias": "bullish"
        }

    # =========================
    # SELL SETUP
    # =========================
    if structure in ["bearish_bos", "bearish_choch"] and sweep == "bearish":
        return {
            "pair": "GOLD",
            "signal": "SELL",
            "price": close,
            "sl": close + 10,
            "tp1": close - 10,
            "tp2": close - 20,
            "rr": 2.0,
            "score": 80,
            "structure": structure,
            "h1_bias": "bearish"
        }

    return None
