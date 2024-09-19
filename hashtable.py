class HashMap:
    def __init__(self, capacity=6):
        self.map = []
        for _ in range(capacity):
            self.map.append([])

    # Create hash key -> O(1)
    def create_hash_key(self, key):
        return int(key) % len(self.map)

    # Insert package into hash table. Hash Table's insertion function.
    def insert_val(self, key, value):
        key_hash = self.create_hash_key(key)
        key_value = [key, value]

        if self.map[key_hash] == None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = key_value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # Update package in hash table. Hash Table's update function.
    def update_val(self, key, value):
        key_hash = self.create_hash_key(key)
        if self.map[key_hash] != None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    print(pair[1])
                    return True
        else:
            print('There was an error with updating on key: ' + key)

    # Get a value from hash table. Hash table's getter function.
    def get_val(self, key):
        key_hash = self.create_hash_key(key)
        if self.map[key_hash] != None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None


class HashTableEntry:
    def __init__(self, key, item):
        self.key = key
        self.item = item
