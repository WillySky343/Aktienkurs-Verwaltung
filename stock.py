#aktien.py

class stock:
    def __init__(self, name, wkn, symbol):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.history = []  # Liste für die letzten 30 Tage (PriceData Objekte)
