import config
config.configure_imports()

from Map import Map
from Node import Node
from LimitedDStar import LimitedDStar
from data_parser import *

map_file = 'data\lak105d.map'
map_scen_file = 'data\lak105d.map.scen'

map_str, map_width, map_height = read_map(map_file)
tasks = read_map_scen(map_scen_file, 1)

print(map_str)
print(tasks)

for start_i, start_j, goal_i, goal_j, path_length in tasks:
    _map = Map()
    _map.read_from_string(map_width, map_height, map_str)
    _start = Node(start_i, start_j)
    _finish = Node(goal_i, goal_j)

    d_star = LimitedDStar(_map, _start, _finish)
    d_star.run()
    d_star.print_path()