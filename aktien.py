import csv
import json
from classes.stock import stock
from classes.pricedata import PriceData
from classes.hashtable import Hashtable

class stockmanager:
    def __init__(self):
        self.by_name = Hashtable()
        self.by_symbol = Hashtable()

########-ADD FUNKTION-###########
    def add_stock(self, name, wkn, symbol):
        new_stock = stock(name, wkn, symbol)
        self.by_name.insert(name, new_stock)
        self.by_symbol.insert(symbol, new_stock)
        print(f"Aktie '{name}' erfolgreich hinzugefügt.")

############-DELETE FUNKTION-###########
    def delete_stock(self, identifier):
        #identifier->name oder symbol
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if stock:
            self.by_name.delete(stock.name)
            self.by_symbol.delete(stock.symbol)
            print(f"Aktie '{identifier}' gelöscht.")
        else:
            print("Aktie nicht gefunden.")

###########-IMPORT FUNKTION-###########
    def import_csv(self, identifier, filename):
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if not stock:
            print("Aktie nicht gefunden.")
            return
        
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                data_list = list(reader)[:30]
                stock.history = []
                for row in data_list:

                    p = PriceData(
                        row.get('Date'), row.get('Close/Last', row.get('Close')).replace('$', ''),
                        row.get('Volume'), row.get('Open').replace('$', ''),
                        row.get('High').replace('$', ''), row.get('Low').replace('$', '')
                    )
                    stock.history.append(p)
            print(f"{len(stock.history)} Kurswerte für {stock.name} importiert.")
        except Exception as e:
            print(f"Fehler beim Import: {e}")

###########-SEARCH FUNKTION-###########
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

##########-PLOT FUNKTION-###########
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

###########-LOAD FUNKTION-###########
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for s in data: 
                    Stock = stock(s['name'], s['wkn'], s['symbol'])
                    for p in s['history']:
                        Stock.history.append(PriceData(p['date'], p['open'], p['close'], p['high'], p['low'], p['volume']))
                        self.by_name.insert(Stock.name, Stock)
                        self.by_symbol.insert(Stock.symbol, Stock)
                    print("Daten erfolgreich geladen.")
        except FileNotFoundError:
            print("Datei nicht gefunden.")

############-SAVE FUNKTION-########### 
    def save_data(self, filename):
        data = []
        for item in self.by_name.table:

            if item is not None and item[0] != Hashtable.DELETED:
                stock_obj = item[1]
                history_data = [vars(p) for p in stock_obj.history]
                data.append({
                    'name': stock_obj.name, 'wkn': stock_obj.wkn, 'symbol': stock_obj.symbol,
                    'history': history_data
                })
        with open(filename, 'w') as f:
            json.dump(data, f)
        print("Daten gespeichert.")

def main():
    manager = stockmanager()

    while True:
        print("----- Aktienverwaltung -----")
        print("1.ADD 2.DEL 3.IMPORT 4.SEARCH 5.PLOT 6.SAVE 7.LOAD 8.QUIT")
        choice = input("Auswahl: ")

        if choice == '1':
            manager.add_stock(input("Name: "),
                              input("WKN: "),
                              input("Kürzel: "))
        elif choice == '2':
            manager.delete_stock(input("Name oder Kürzel zum Löschen: "))
        elif choice == '3':
            manager.import_csv(input("Aktienname/Kürzel: "),
                               input("CSV Dateiname: "))
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