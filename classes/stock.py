
class stock:
    def __init__(self, name, wkn, symbol):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.history = []  #Liste der letzten 30 tage (pricedata)
