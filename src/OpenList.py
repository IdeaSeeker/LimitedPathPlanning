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

        self.add_count = 0
        self.get_count = 0
        self.pop_count = 0

    def insert(self, key, node: Node):
        self.add_count += 1
        elem = QueueElem(key, node)
        self._set.add(elem)
        self._data[node] = elem

    def remove(self, node: Node):
        self.pop_count += 1
        self._set.discard(self._data[node])
        self._data.pop(node)

    def __contains__(self, key):
        self.get_count += 1
        return key in self._data

    def is_empty(self):
        return len(self._data) == 0

    def get_min_key(self):
        self.pop_count += 1
        result = self._set.pop(index=0)
        self._data.pop(result.node)
        return result.node

    def get_min_value(self):
        self.get_count += 1
        return self._set[0].key

    def pop_min_value(self):
        self.pop_count += 1
        result = self._set.pop(index=0)
        self._data.pop(result.node)
        return result.node, result.key
