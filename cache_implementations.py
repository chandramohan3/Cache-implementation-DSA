from collections import defaultdict
from typing import Any, Dict, Optional

class Node:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node("head", None)  # Sentinel nodes
        self.tail = Node("tail", None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node: Node) -> None:
        """Add node right after head"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_tail(self) -> Node:
        """Remove the node right before tail"""
        if self.size > 0:
            node = self.tail.prev
            self.remove_node(node)
            return node
        return None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Node] = {}
        self.dll = DoublyLinkedList()
        
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache and move it to front (most recently used)"""
        if key in self.cache:
            node = self.cache[key]
            self.dll.remove_node(node)
            self.dll.add_node(node)
            return node.value
        return None

    def put(self, key: str, value: Any) -> None:
        """Put item in cache"""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.dll.remove_node(node)
            self.dll.add_node(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used item (tail)
                lru_node = self.dll.remove_tail()
                del self.cache[lru_node.key]
            
            # Add new node
            node = Node(key, value)
            self.cache[key] = node
            self.dll.add_node(node)
    
    def get_state(self) -> dict:
        """Get current state of cache for visualization"""
        items = []
        current = self.dll.head.next
        while current != self.dll.tail:
            items.append({
                'key': current.key,
                'value': current.value,
                'type': 'recent' if current == self.dll.head.next else 'normal'
            })
            current = current.next
        return {
            'items': items,
            'capacity': self.capacity,
            'size': len(self.cache)
        }

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_node: Dict[str, Node] = {}
        self.freq_to_nodes: Dict[int, DoublyLinkedList] = defaultdict(DoublyLinkedList)
        
    def _update_freq(self, node: Node) -> None:
        """Update frequency of a node"""
        # Remove from old frequency list
        self.freq_to_nodes[node.freq].remove_node(node)
        if node.freq == self.min_freq and self.freq_to_nodes[node.freq].size == 0:
            self.min_freq += 1
        
        # Add to new frequency list
        node.freq += 1
        self.freq_to_nodes[node.freq].add_node(node)

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache and update its frequency"""
        if key in self.key_to_node:
            node = self.key_to_node[key]
            self._update_freq(node)
            return node.value
        return None

    def put(self, key: str, value: Any) -> None:
        """Put item in cache"""
        if self.capacity == 0:
            return

        if key in self.key_to_node:
            node = self.key_to_node[key]
            node.value = value
            self._update_freq(node)
        else:
            if len(self.key_to_node) >= self.capacity:
                # Remove least frequent used item
                lfu_list = self.freq_to_nodes[self.min_freq]
                lfu_node = lfu_list.remove_tail()
                del self.key_to_node[lfu_node.key]
            
            # Add new node
            node = Node(key, value)
            self.key_to_node[key] = node
            self.freq_to_nodes[1].add_node(node)
            self.min_freq = 1

    def get_state(self) -> dict:
        """Get current state of cache for visualization"""
        freq_items = {}
        for freq, dll in self.freq_to_nodes.items():
            items = []
            current = dll.head.next
            while current != dll.tail:
                items.append({
                    'key': current.key,
                    'value': current.value,
                    'freq': current.freq
                })
                current = current.next
            if items:
                freq_items[freq] = items
        
        return {
            'items_by_freq': freq_items,
            'capacity': self.capacity,
            'size': len(self.key_to_node),
            'min_freq': self.min_freq
        }
