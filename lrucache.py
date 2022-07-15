# Solution 1 (ideal)
# Read complexity: O(1)
# Write complexity: O(1), for eviction and non-eviction cases
class LRUCache:
    class DoublyLinkedList:
        class Node:
            def __init__(self, key, val, prev, next):
                self.key = key
                self.val = val
                self.prev = prev
                self.next = next

        def __init__(self, start, end):
            self.start = start
            self.end = end

        def push(self, n):
            if self.start == None:
                self.end = n
            else:
                self.start.prev = n
                n.next = self.start
            self.start = n
            return n
        
        def remove(self, n):
            if n == self.start:
                return
            if n.prev != None:
                n.prev.next = n.next
            if n.next != None:
                n.next.prev = n.prev
            if n == self.end:
                self.end = n.prev
            n.prev = None
            n.next = None
            return n

        def moveFront(self, n):
            self.remove(n)
            self.push(n)
            
    def __init__(self, size):
        if size < 1:
            raise ValueError("size must be greater than 0")
        self.cache = {}
        self.list = LRUCache.DoublyLinkedList(None, None)
        self.size = size

    def evict(self):
        n = self.list.end
        del self.cache[n.key]

        # Size 1 case
        if self.list.start == self.list.end:
            self.list.start = None
            self.list.end = None
            return
        
        # Size > 1 case
        n.prev.next = None
        self.list.end = n.prev
        n.prev = None

    def write(self, key, val):
        n = self.cache.get(key, None)
        if n != None:
            n.val = val
            self.list.moveFront(n)
            return
        if len(self.cache) == self.size:
            self.evict()
        self.cache[key] = self.list.push(LRUCache.DoublyLinkedList.Node(key, val, None, None))

    def read(self, key):
        n = self.cache.get(key, None)
        if n != None:
            self.list.moveFront(n)
            return n.val
        raise KeyError(f"could not find key {key}")

# Solution 2 (naive)
# Read complexity: O(1)
# Write complexity: O(1) for non-eviction case, O(n) for eviction case
class LRUCacheNaive:
    class Entry:
        def __init__(self, val, priority):
            self.val = val
            self.priority = priority

    def __init__(self, size):
        self.size = size
        self.cache = {}
        self.max_priority = 0

    def max_priority_inc(self):
        self.max_priority += 1
        return self.max_priority
        
    def read(self, key):
        if key not in self.cache:
            raise KeyError(f"could not find key {key}")
        self.cache[key].priority = self.max_priority_inc()
        return self.cache[key].val

    def write(self, key, val):
        if len(self.cache) == self.size and key not in self.cache:
            self.evict()
        self.cache[key] = LRUCacheNaive.Entry(val, self.max_priority_inc())

    def evict(self):
        # This function is O(n), very slow!
        min = None
        min_key = None
        for key, e in self.cache.items():
            if min is None:
                min = e.priority
                min_key = key
                continue
            elif e.priority < min:
                min = e.priority
                min_key = key
        del self.cache[min_key]
                
# Quick test of both implementations
for c in [LRUCache(2), LRUCacheNaive(2)]:
    c.write(0, "a")
    c.write(1, "b")
    c.write(2, "c") # this write should evict 0 => a, the oldest mapping
    err = None
    try:
        c.read(0)
    except KeyError as e:
        err = e
    assert str(err) == "'could not find key 0'"
    assert c.read(1) == "b"
    assert c.read(2) == "c"

    c.read(1) # this read should make 1 => b the most recently used entry
    c.write(3, "d") # this write should evict 2 => c
    err = None
    try:
        c.read(2)
    except KeyError as e:
        err = e
    assert str(err) == "'could not find key 2'"
    assert c.read(1) == "b"
    assert c.read(3) == "d"

    c.write(3, "e") # this write should not evict, just update 3 => e
    assert c.read(1) == "b"
    assert c.read(3) == "e"