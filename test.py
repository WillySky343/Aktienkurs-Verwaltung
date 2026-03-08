import csv
import json

# Datenstruktur für einen einzelnen Kurseintrag
class PriceData:
    def __init__(self, date, close, volume, open_val, high, low):
        self.date = date
        self.close = float(close)
        self.volume = volume
        self.open = float(open_val)
        self.high = float(high)
        self.low = float(low)

# Datenstruktur für eine Aktie
class Stock:
    def __init__(self, name, wkn, symbol):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.history = []  # Liste für die letzten 30 Tage (PriceData Objekte)

# Die selbst implementierte Hashtabelle
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        # Einfacher Hash-Algorithmus für Strings
        hash_val = 0
        for char in key:
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val

    def insert(self, key, value):
        index = self._hash(key)
        # Falls Key schon existiert, aktualisieren
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def search(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

# Hauptverwaltungsklasse
class StockManager:
    def __init__(self):
        self.by_name = HashTable()
        self.by_symbol = HashTable()

    def add_stock(self, name, wkn, symbol):
        new_stock = Stock(name, wkn, symbol)
        self.by_name.insert(name, new_stock)
        self.by_symbol.insert(symbol, new_stock)
        print(f"Aktie {name} erfolgreich hinzugefügt.")

    def del_stock(self, identifier):
        # Versuche über Name oder Symbol zu löschen
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if stock:
            self.by_name.delete(stock.name)
            self.by_symbol.delete(stock.symbol)
            print(f"Aktie {identifier} gelöscht.")
        else:
            print("Aktie nicht gefunden.")

    def import_csv(self, identifier, filename):
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if not stock:
            print("Aktie nicht gefunden. Bitte zuerst ADD nutzen.")
            return
        
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Wir nehmen die letzten 30 Einträge
                data_list = list(reader)[:30]
                stock.history = []
                for row in data_list:
                    # Anpassung der Spaltennamen je nach CSV-Format (Nasdaq Style)
                    p = PriceData(
                        row.get('Date'), row.get('Close/Last', row.get('Close')).replace('$', ''),
                        row.get('Volume'), row.get('Open').replace('$', ''),
                        row.get('High').replace('$', ''), row.get('Low').replace('$', '')
                    )
                    stock.history.append(p)
            print(f"{len(stock.history)} Kurswerte für {stock.name} importiert.")
        except Exception as e:
            print(f"Fehler beim Import: {e}")

    def search_stock(self, identifier):
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if stock:
            print(f"\nName: {stock.name} | WKN: {stock.wkn} | Symbol: {stock.symbol}")
            if stock.history:
                latest = stock.history[0]
                print(f"Aktuellster Kurs ({latest.date}): Close: {latest.close}, Vol: {latest.volume}")
            else:
                print("Keine Kursdaten vorhanden.")
        else:
            print("Aktie nicht gefunden.")

    def plot_stock(self, identifier):
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if not stock or not stock.history:
            print("Keine Daten zum Plotten vorhanden.")
            return

        print(f"\nSchlusskurse (ASCII) für {stock.name}:")
        prices = [p.close for p in stock.history][::-1] # Umdrehen für chronologische Anzeige
        if not prices: return
        
        min_p, max_p = min(prices), max(prices)
        range_p = max_p - min_p if max_p != min_p else 1
        
        for p in prices:
            # Skalierung auf 20 Einheiten Breite
            bar_length = int((p - min_p) / range_p * 20) + 1
            print(f"{p:8.2f} | {'#' * bar_length}")

    def save_data(self, filename):
        # Manuelle Serialisierung, da HashTable nicht direkt JSON-fähig ist
        data = []
        # Wir durchlaufen die interne Struktur der by_name Tabelle
        for bucket in self.by_name.table:
            for key, stock in bucket:
                history_data = [vars(p) for p in stock.history]
                data.append({
                    'name': stock.name, 'wkn': stock.wkn, 'symbol': stock.symbol,
                    'history': history_data
                })
        with open(filename, 'w') as f:
            json.dump(data, f)
        print("Daten gespeichert.")

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for s in data:
                    stock = Stock(s['name'], s['wkn'], s['symbol'])
                    for p in s['history']:
                        stock.history.append(PriceData(p['date'], p['close'], p['volume'], p['open'], p['high'], p['low']))
                    self.by_name.insert(stock.name, stock)
                    self.by_symbol.insert(stock.symbol, stock)
            print("Daten geladen.")
        except FileNotFoundError:
            print("Datei nicht gefunden.")

# --- Menüschleife ---
def main():
    manager = StockManager()
    while True:
        print("\n--- AKTIEN VERWALTUNG ---")
        print("1: ADD, 2: DEL, 3: IMPORT, 4: SEARCH, 5: PLOT, 6: SAVE, 7: LOAD, 8: QUIT")
        choice = input("Auswahl: ")

        if choice == '1':
            manager.add_stock(input("Name: "), input("WKN: "), input("Kürzel: "))
        elif choice == '2':
            manager.del_stock(input("Name oder Kürzel zum Löschen: "))
        elif choice == '3':
            manager.import_csv(input("Aktienname/Kürzel: "), input("CSV Dateiname: "))
        elif choice == '4':
            manager.search_stock(input("Suche nach Name oder Kürzel: "))
        elif choice == '5':
            manager.plot_stock(input("Plot für Aktie: "))
        elif choice == '6':
            manager.save_data("stocks.json")
        elif choice == '7':
            manager.load_data("stocks.json")
        elif choice == '8':
            break

if __name__ == "__main__":
    main()