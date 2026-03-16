class PriceData:
    def __init__(self, date, close, volume, open_val, high, low):
        self.date = date
        self.close = float(close)
        self.volume = volume
        self.open = float(open_val)
        self.high = float(high)
        self.low = float(low)

    