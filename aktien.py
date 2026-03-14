import csv
from classes.stock import stock
from classes.pricedata import PriceData
from classes.hashtable import Hashtable

class stockmanager:
    def __init__(self):
        self.by_name = Hashtable()
        self.by_symbol = Hashtable()

    def add_stock(self, name, wkn, symbol):
        new_stock = stock(name, wkn, symbol)
        self.by_name.insert(name, new_stock)
        self.by_symbol.insert(symbol, new_stock)
        print(f"Aktie '{name}' erfolgreich hinzugefügt.")

    def delete_stock(self, identifier):
        #identifier->name oder symbol
        stock = self.by_name.search(identifier) or self.by_symbol.search(identifier)
        if stock:
            self.by_name.delete(stock.name)
            self.by_symbol.delete(stock.symbol)
            print(f"Aktie '{identifier}' gelöscht.")
        else:
            print("Aktie nicht gefunden.")

    

while True:
    print("----- Aktienverwaltung -----")
    print("1.ADD 2.DEL 3.IMPORT 4.SEARCH 5.PLOT 6.SAVE 7.LOAD 8.QUIT")
    choice = input("Auswahl: ")

    if choice == '1':
        name = input("Name: ")
        wkn = input("WKN: ")
        kuerzel = input("Kürzel: ")
    
    elif choice == '2':
        del_input = input("Name oder Kürzel zum Löschen: ")
    elif choice == '3':
        print("placeholder for import functionality")
    elif choice == '4':
        search_input = input("Suche nach Name oder Kürzel: ")
    elif choice == '5':
        plot_input = input("Plot für Aktie: ")
    elif choice == '6':
        print("placeholder for save functionality")
    elif choice == '7':
        print("placeholder for load functionality")
    elif choice == '8':
        break