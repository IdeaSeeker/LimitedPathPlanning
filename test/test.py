from IPython.display import Image as Img
from IPython.display import display

import config
config.configure_imports()

from Map import Map
from Node import Node
from DStarLite import DStarLite

from visualizer import *
from data_parser import *

lak105d_filename = '../data/lak105d.map'
lak105d_scen_filename = '../data/lak105d.map.scen'
den204d_filename = '../data/den204d.map'
den204d_scen_filename = '../data/den204d.map.scen'
Paris_256_filename = '../data/Paris_1_256.map'

def run_on(map_filename, start, finish, pixel_size = 20, gif_speed = 200):
    _map = Map()
    _map.read_from_string(*read_map(map_filename))

    d_star = DStarLite(_map, start, finish)
    d_star.run()

    gif_filename = f'd_star_{start.i}_{start.j}_{finish.i}_{finish.j}.gif'
    draw_path(_map, d_star._path, gif_filename, pixel_size, gif_speed)

    return Img(filename=gif_filename)

if __name__ == "__main__":
    run_on(Paris_256_filename, Node(22, 68), Node(224, 213), 2, 1)