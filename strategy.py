import random

def generate_signal():
    """
    Temporary SMC placeholder (we replace later with real logic)
    """

    if random.randint(1, 6) == 4:
        return {
            "pair": "GOLD",
            "signal": "BUY",
            "price": 2000,
            "sl": 1985,
            "tp1": 2020,
            "tp2": 2040,
            "rr": 2.5,
            "score": 85,
            "structure": "bullish_bos",
            "h1_bias": "bullish"
        }

    return None
