class Hashtable:
    # Konstante für unsere Tombstones (Grabsteine) beim Löschen
    DELETED = "<GELOESCHT>"

    def __init__(self, size=2003): 
        # 2003 ist eine Primzahl > 2000. Wichtig für quadratische Sondierung!
        self.size = size
        # Keine Listen mehr! Nur ein flaches Array mit None-Werten.
        self.table = [None] * self.size
        self.count = 0 # Um den Füllgrad (Load Factor) zu überwachen
    
    def _hash(self, key): 
        hash_val = 0
        for char in key: 
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val     
    
    def insert(self, key, value):
        # Warnung, wenn Füllgrad über 50% steigt (für das Protokoll wichtig)
        if self.count >= self.size // 2:
            print("Warnung: Load Factor > 0.5. Sondierung wird ineffizient.")

        index = self._hash(key)
        
        # Quadratische Sondierung: h(k, i) = (h(k) + i^2) mod size
        for i in range(self.size):
            probe_index = (index + i**2) % self.size
            
            # Fach ist leer ODER enthält einen Grabstein -> Hier können wir einfügen
            if self.table[probe_index] is None or self.table[probe_index][0] == self.DELETED:
                self.table[probe_index] = (key, value)
                self.count += 1
                return

            # Fach ist belegt, aber es ist exakt unser Key -> Update!
            if self.table[probe_index][0] == key:
                self.table[probe_index] = (key, value)
                return
                
        print("Fehler: Hashtabelle ist voll.")

    def search(self, key):
        index = self._hash(key)
        
        for i in range(self.size):
            probe_index = (index + i**2) % self.size
            
            # Wenn wir auf ein komplett leeres Fach stoßen, bricht die Suche ab
            if self.table[probe_index] is None:
                return None
                
            # Wenn wir den Key finden, geben wir den Wert (Index 1 des Tupels) zurück
            if self.table[probe_index][0] == key:
                return self.table[probe_index][1]
                
            # Bei einem Grabstein (DELETED) oder anderem Key läuft die Schleife einfach weiter!
            
        return None

    def delete(self, key):
        index = self._hash(key)
        
        for i in range(self.size):
            probe_index = (index + i**2) % self.size
            
            # Key nicht da
            if self.table[probe_index] is None:
                return False
                
            # Key gefunden -> Durch Grabstein ersetzen!
            if self.table[probe_index][0] == key:
                self.table[probe_index] = (self.DELETED, None)
                self.count -= 1
                return True
                
        return False