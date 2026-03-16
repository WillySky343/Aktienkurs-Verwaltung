class Hashtable:
    DELETED = "<GELOESCHT>"#Tombstone Prinzip

    def __init__(self, size=2003): #Load factor ~ 0.5 
        self.size = size
        self.table = [None] * self.size
        self.count = 0 
    
    #hashfunktion
    def _hash(self, key): 
        hash_val = 0
        for char in key:    #unabhängig von Länge
            hash_val = (hash_val * 31 + ord(char)) % self.size 
        return hash_val     
    
    def insert(self, key, value):

        index = self._hash(key)
        
        for i in range(self.size):
            probe_index = (index + i**2) % self.size #quadratisches Sondieren
            if self.table[probe_index] is None or self.table[probe_index][0] == self.DELETED:
                self.table[probe_index] = (key, value)
                self.count += 1
                return

            if self.table[probe_index][0] == key:
                self.table[probe_index] = (key, value)
                return
                
        print("Fehler: Hashtabelle ist voll.")

    def search(self, key):
        index = self._hash(key)
        
        for i in range(self.size):
            probe_index = (index + i**2) % self.size
            
            if self.table[probe_index] is None:
                return None
                
            if self.table[probe_index][0] == key:
                return self.table[probe_index][1]
            
        return None

    def delete(self, key):
        index = self._hash(key)
        
        for i in range(self.size):
            probe_index = (index + i**2) % self.size
            
            if self.table[probe_index] is None:
                return False
                
            if self.table[probe_index][0] == key:
                self.table[probe_index] = (self.DELETED, None)
                self.count -= 1
                return True
                
        return False