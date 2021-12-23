from IPython.display import Image as Img
from IPython.display import display

import config
config.configure_imports()

from Map import Map
from Node import Node
from Change import Change
from LPAStar import LPAStar

from visualizer import *
from data_parser import *

_map = Map()
_map.read_from_string(3, 3,
'''
...
#..
#..
''')
_start = Node(0, 0)
_finish = Node(2, 2)
_changes = [
    [Change(1, 1, 1, True)],
    [Change(1, 1, 2, True),
    Change(10, 1, 0, False),
    Change(10, 2, 0, False)]
]

d_star = LPAStar(_map, _start, _finish, _changes)
d_star.run()