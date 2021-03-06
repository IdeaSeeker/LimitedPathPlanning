from PIL import Image, ImageDraw
from Map import Map
from utils import *


color_black = (0, 0, 0)
color_gray = (102, 102, 102)
color_light_gray = (204, 204, 204)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_light_red = (255, 204, 204)
color_green = (0, 255, 0)


def draw_pix(draw, i, j, color, k):
    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=color)


def calculate_open_obstacles(path: list, vision_distance: int):
    result = [set()]
    for node in path:
        for di in range(-vision_distance, vision_distance + 1):
            for dj in range(-vision_distance, vision_distance + 1):
                if di == dj and di == 0:
                    continue
                i, j = node.i + di, node.j + dj
                result[-1].add((i, j))
        result.append(result[-1].copy())
    return result


def draw_path(full_map: Map, path: list, filename = 'path', k = 20, gif_speed = 200, vision_distance = 1):
    if len(path) == 0:
        print('empty path!')
        return

    images = []
    hIm = full_map._height * k
    wIm = full_map._width * k

    map_str = str(full_map).split('\n')
    map_str = list(map(list, map_str))
    finish = path[-1]
    map_str[finish.i][finish.j] = 'F'

    last_node = None
    log_obstacles = calculate_open_obstacles(path, vision_distance)

    for index, node in enumerate(path + [None]):
        im = Image.new('RGB', (wIm, hIm), color='green')
        draw = ImageDraw.Draw(im)

        for i in range(full_map._height):
            for j in range(full_map._width):
                if map_str[i][j] == '.':
                    draw_pix(draw, i, j, color_white, k)
                elif map_str[i][j] == '#':
                    if index < len(log_obstacles) and (i, j) in log_obstacles[index]:
                        draw_pix(draw, i, j, color_gray, k)
                    else:
                        draw_pix(draw, i, j, color_light_gray, k)
                elif map_str[i][j] == 'R':
                    draw_pix(draw, i, j, color_red, k)
                elif map_str[i][j] == 'P':
                    draw_pix(draw, i, j, color_light_red, k)
                elif map_str[i][j] == 'F':
                    draw_pix(draw, i, j, color_green, k)

        if node is not None:
            map_str[node.i][node.j] = 'R'
        if last_node is not None:
            map_str[last_node.i][last_node.j] = 'P'
        last_node = node

        images.append(im)

    images[0].save(filename, save_all=True, append_images=images[1:], optimize=False, duration=gif_speed, loop=0)

def draw_paths(full_map: Map, paths: list, filename = 'path', k = 20, gif_speed = 200):
    if len(paths) == 0:
        print('empty path!')
        return

    images = []
    hIm = full_map._height * k
    wIm = full_map._width * k

    for path in paths:
        map_str = str(full_map).split('\n')
        map_str = list(map(list, map_str))
        finish = path[0]
        im = Image.new('RGB', (wIm, hIm), color='green')
        draw = ImageDraw.Draw(im)
        for index, node in enumerate(path):
            map_str[node.i][node.j] = "P"
        map_str[node.i][node.j] = "R"
        map_str[finish.i][finish.j] = 'F'
        
        for i in range(full_map._height):
            for j in range(full_map._width):
                if map_str[i][j] == '.':
                    draw_pix(draw, i, j, color_white, k)
                elif map_str[i][j] == '#':
                    draw_pix(draw, i, j, color_light_gray, k)
                elif map_str[i][j] == 'R':
                    draw_pix(draw, i, j, color_red, k)
                elif map_str[i][j] == 'P':
                    draw_pix(draw, i, j, color_light_red, k)
                elif map_str[i][j] == 'F':
                    draw_pix(draw, i, j, color_green, k)

        images.append(im)

    images[0].save(filename, save_all=True, append_images=images[1:], optimize=False, duration=gif_speed, loop=0)
    

def draw_fast_paths(full_map: Map, paths: list, obstacles: list, visited: list, filename = 'fast_paths', k = 20, gif_speed = 200):
    if len(paths) == 0:
        print('empty path!')
        return

    images = []
    hIm = full_map._height * k
    wIm = full_map._width * k

    map_str_d = str(full_map).split('\n')
    map_str_d = list(map(list, map_str_d))
    start = paths[0][0]
    finish = paths[0][-1]
    map_str_d[start.i][start.j] = 'S'
    map_str_d[finish.i][finish.j] = 'F'

    for index, path in enumerate(paths):
        im = Image.new('RGB', (wIm, hIm), color='green')
        draw = ImageDraw.Draw(im)
        
        map_str = [x[:] for x in map_str_d]
        for s in obstacles[index]:
            if s != start and s != finish:
                map_str[s.i][s.j] = 'O'
        for s in visited[index]:
            if s != start and s != finish:
                map_str[s.i][s.j] = 'V'
        for s in path:
            if s != start and s != finish:
                map_str[s.i][s.j] = 'P'

        for i in range(full_map._height):
            for j in range(full_map._width):
                if map_str[i][j] == '.':
                    draw_pix(draw, i, j, color_white, k)
                elif map_str[i][j] == '#':
                    draw_pix(draw, i, j, color_gray, k)
                elif map_str[i][j] == 'O':
                    draw_pix(draw, i, j, color_black, k)
                elif map_str[i][j] == 'F':
                    draw_pix(draw, i, j, color_green, k)
                elif map_str[i][j] == 'S':
                    draw_pix(draw, i, j, color_red, k)
                elif map_str[i][j] == 'V':
                    draw_pix(draw, i, j, color_light_gray, k)
                elif map_str[i][j] == 'P':
                    draw_pix(draw, i, j, color_light_red, k)

        images.append(im)

    images[0].save(filename, save_all=True, append_images=images[1:], optimize=False, duration=gif_speed, loop=0)
