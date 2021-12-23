import argparse
from Change import Change
from DStarLite import DStarLite
from LPAStar import LPAStar
from Map import Map
from IPython.display import Image as Img
from Node import Node
from utils import *
from data_parser import *
from visualizer import *
from random import randint as rand

def run_on(map_filename, start, finish, pixel_size = 20, gif_speed = 200):
    d_star = DStarLite(_map, start, finish, 1)
    d_star.run()

    gif_filename = f'd_star_{start.i}_{start.j}_{finish.i}_{finish.j}.gif'
    draw_path(_map, d_star._path, gif_filename, pixel_size, gif_speed, 1)

    return Img(filename=gif_filename)

def run_dstarlite(map_filename: str, start: Node, finish: Node, gif_filename: str, pixel_size: int, gif_speed: int):
    _map = Map()
    _map.read_from_string(*read_map(map_filename))
    d_star = DStarLite(_map, start, finish)
    d_star.run()
    draw_path(_map, d_star._path, gif_filename, pixel_size, gif_speed)

def run_lpastar(map_filename: str, start: Node, finish: Node, gif_filename: str, pixel_size: int, gif_speed: int):
    _map, _mmap = Map(), Map()
    _map.read_from_string(*read_map(map_filename))
    _mmap.read_from_string(*read_map(map_filename))

    lpa_paths = []
    obstacles = [[]]

    lpa_star = LPAStar(_map, start, finish)
    lpa_visiteds = [lpa_star.compute_shortest_path()]
    lpa_paths = [lpa_star.greedy_path()]

    n_changes = 30

    for _ in range(n_changes):
        lpa_path = lpa_paths[-1]

        index = rand(1, len(lpa_path) - 2)
        qi, qj = lpa_path[index].coordinates()
        obstacles.append(obstacles[-1] + [Node(qi, qj)])
        
        lpa_visited = lpa_star.apply_changes([Change(0, qi, qj, True)])
        lpa_visiteds.append(lpa_visited)

        lpa_path = lpa_star.greedy_path()

        if lpa_path is None:
            break
        lpa_paths.append(lpa_path)

        if len(lpa_path) < 3:
            break
    
    draw_fast_paths(_mmap, lpa_paths, obstacles, lpa_visiteds, gif_filename, pixel_size, gif_speed)


runners = {
    "lpastar": run_lpastar,
    "dstarlite": run_dstarlite
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", type=str, help="algorithm to be used",choices=["dstarlite", "lpastar"])
    parser.add_argument("map_path", type=str, help="path to the .map file. scenario file .map.scen should be nearby")
    parser.add_argument("output_path", type=str, help="path to resulting gif")
    parser.add_argument("--vision_distance", type=int, help="dstarlite vision distance", default=1)
    parser.add_argument("--n_tasks", type=int, default=2)
    parser.add_argument("--pixel_size", type=int, default=20)
    parser.add_argument("--gif_speed", type=int, default=100)

    args = parser.parse_args()

    tasks = read_map_scen(args.map_path + ".scen", args.n_tasks)
    images = []

    for task_number, (start_i, start_j, goal_i, goal_j, _) in enumerate(tasks):
        start = Node(start_i, start_j)
        finish = Node(goal_i, goal_j)
        gif_filename = f'{task_number}_' + args.output_path

        runners[args.algorithm](args.map_path, start, finish, gif_filename, args.pixel_size, args.gif_speed)
    