class Hashtable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    
    def _hash(self, key): 
        hash_val = 0
        for char in key:  #unique value->each key
            hash_val = (hash_val * 31 + ord(char)) % self.size
        return hash_val     
    
    def insert(self, key, value):
        index = self._hash(key)
        #duplicate check
        for i, (k, _) in enumerate(self.table[index]):#enumerate->index+value
            if k == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))

    def search(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        print(f"Key '{key}' not found.")
        return None
        #inhalt des Schlüssels zurückgeben

    def delete(self, key):
        index = self._hash(key)
        for i, (k, _) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False
        #entfernt den Schlüssel und seinen Wert