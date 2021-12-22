class OpenList:
    ''' OpenList[node] = calculate_key(node) '''

    def __init__(self):
        self._data = {}


    def __getitem__(self, key):
        return self._data[key]


    def __setitem__(self, key, value):
        self._data[key] = value


    def __contains__(self, key):
        return key in self._data


    def is_empty(self):
        return len(self._data) == 0


    def get_min_key(self):
        result = None
        for key in self._data:
            if result is None or self._data[key] < self._data[result]:
                result = key
        return result


    def get_min_value(self):
        return self._data[self.get_min_key()]


    def pop_min_value(self):
        key = self.get_min_key()
        return key, self._data.pop(key)


    def slow_pop(self, key):
        return key, self._data.pop(key)
