class Change:

    def __init__(self, time: int, i: int, j: int, is_obst: bool):
        self._time = time
        self._i = i
        self._j = j
        self._is_obst = is_obst

    @property
    def coordinates(self):
        return self._i, self._j

    
    def __str__(self):
        return f'Change({self._i}, {self._j}, is_obst: {self._is_obst})'


    def __repr__(self):
        return str(self)
