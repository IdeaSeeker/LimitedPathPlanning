from typing import List
from Node import Node
from heapq import heappush, heappop, heapify

class QueueElem:
    def __init__(self, key, node: Node) -> None:
        self.key = key
        self.node = node

    def __lt__(self, other: "QueueElem"):
        return self.key < other.key

    def __repr__(self) -> str:
        return f"{self.key} {self.node}"

class OpenList:
    ''' OpenList[node] = calculate_key(node) '''

    def __init__(self):
        self._data = {}
        self.queue: List[QueueElem] = []

    def insert(self, key, node: Node):
        elem = QueueElem(key, node)
        heappush(self.queue, elem)
        self._data[node] = elem

    def remove(self, node: Node):
        self.queue.remove(self._data[node])
        heapify(self.queue)
        self._data.pop(node)

    def __contains__(self, key):
        return key in self._data

    def is_empty(self):
        return len(self._data) == 0

    def get_min_key(self):
        result = heappop(self.queue)
        self._data.pop(result.node)

        return result.node

    def get_min_value(self):
        return self.queue[0].key


    def pop_min_value(self):
        result = heappop(self.queue)
        self._data.pop(result.node)

        return result.node, result.key
