import config
config.configure_imports()

from Map import Map
from PIL import Image, ImageDraw

color_black = (0, 0, 0)
color_gray = (102, 102, 102)
color_light_gray = (204, 204, 204)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_light_red = (255, 204, 204)
color_green = (0, 255, 0)


def draw_pix(draw, i, j, color, k):
    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=color)


def calculate_open_obstacles(path: list):
    result = [set()]
    for node in path:
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            i, j = node.i + di, node.j + dj
            result[-1].add((i, j))
        result.append(result[-1].copy())
    return result


def draw_path(full_map: Map, path: list, filename = 'path', k = 20, gif_speed = 200):
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
    log_obstacles = calculate_open_obstacles(path)

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
