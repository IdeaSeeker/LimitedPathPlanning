from Node import Node
from sortedcontainers import SortedSet


class QueueElem:
    def __init__(self, key, node: Node) -> None:
        self.key = key
        self.node = node

    def __lt__(self, other: "QueueElem"):
        return self.key < other.key or \
               self.key == other.key and self.node.coordinates() < other.node.coordinates()

    def __repr__(self) -> str:
        return f"{self.key} {self.node}"


class OpenList:
    ''' OpenList[node] = calculate_key(node) '''

    def __init__(self):
        self._data = {}
        self._set = SortedSet()

    def insert(self, key, node: Node):
        elem = QueueElem(key, node)
        self._set.add(elem)
        self._data[node] = elem

    def remove(self, node: Node):
        self._set.discard(self._data[node])
        self._data.pop(node)

    def __contains__(self, key):
        return key in self._data

    def is_empty(self):
        return len(self._data) == 0

    def get_min_key(self):
        result = self._set.pop(index=0)
        self._data.pop(result.node)
        return result.node

    def get_min_value(self):
        return self._set[0].key

    def pop_min_value(self):
        result = self._set.pop(index=0)
        self._data.pop(result.node)
        return result.node, result.key
