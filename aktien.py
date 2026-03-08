import csv
from stock import stock
from pricedata import 
from hashtable import  

class stockmanager:
    def __init__(self):
        self.by_name = hashtable()
        self.by_symbol = hashtable()


def add_stock(self, name, wkn, symbol):


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