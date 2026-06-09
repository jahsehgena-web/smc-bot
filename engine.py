import numpy as np

def analyze(df, symbol):
    """
    Simple structured signal engine (safe version for deployment)
    Returns: signal dict or None
    """

    if df is None or len(df) < 50:
        return None

    close = df["Close"].values
    high = df["High"].values
    low = df["Low"].values

    price = float(close[-1])

    # simple trend logic (temporary placeholder)
    ema_fast = np.mean(close[-10:])
    ema_slow = np.mean(close[-30:])

    trend = "bullish" if ema_fast > ema_slow else "bearish"

    # simple volatility filter
    recent_range = np.mean(high[-10:] - low[-10:])

    if recent_range <= 0:
        return None

    # fake structured entry logic (safe baseline)
    if trend == "bullish":
        return {
            "symbol": symbol,
            "type": "BUY",
            "price": price,
            "sl": price - (recent_range * 1.5),
            "tp1": price + (recent_range * 1.5),
            "tp2": price + (recent_range * 3),
            "score": 70
        }

    if trend == "bearish":
        return {
            "symbol": symbol,
            "type": "SELL",
            "price": price,
            "sl": price + (recent_range * 1.5),
            "tp1": price - (recent_range * 1.5),
            "tp2": price - (recent_range * 3),
            "score": 70
        }

    return None
