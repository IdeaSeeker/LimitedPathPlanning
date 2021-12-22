import config
config.configure_imports()

from Map import Map
from Node import Node
from LimitedDStar import LimitedDStar
from data_parser import *
from visualizer import draw_path

map_file = 'data\lak105d.map'
map_scen_file = 'data\lak105d.map.scen'

map_str, map_width, map_height = read_map(map_file)
tasks = read_map_scen(map_scen_file, 1)

for start_i, start_j, goal_i, goal_j, path_length in tasks:
    _map = Map()
    _map.read_from_string(map_width, map_height, map_str)
    _start = Node(8, 25)
    _finish = Node(19, 3)
    print(_start, _finish)
    # 5, 4, 19, 21
    # 8, 25, 19, 3

    d_star = LimitedDStar(_map, _start, _finish)
    d_star.run(map_logging=True)
    d_star.print_path()
    draw_path(_map, d_star._path, filename='d_star', log_current_map=d_star._log_current_map)
