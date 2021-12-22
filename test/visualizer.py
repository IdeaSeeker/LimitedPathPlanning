import config
config.configure_imports()

from Map import Map
from PIL import Image, ImageDraw

k = 20

color_black = (0, 0, 0)
color_gray = (102, 102, 102)
color_light_gray = (204, 204, 204)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_light_red = (255, 204, 204)
color_green = (0, 255, 0)


def draw_pix(draw, i, j, color):
    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=color)


def draw_path(full_map: Map, path: list, filename = 'path', log_current_map = None):
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
    cur_map_str = None

    for index, node in enumerate(path + [None]):
        im = Image.new('RGB', (wIm, hIm), color='green')
        draw = ImageDraw.Draw(im)

        if log_current_map is not None and index < len(log_current_map):
            cur_map_str = str(log_current_map[index]).split('\n')
            cur_map_str = list(map(list, cur_map_str))

        for i in range(full_map._height):
            for j in range(full_map._width):
                if map_str[i][j] == '.':
                    draw_pix(draw, i, j, color_white)
                elif map_str[i][j] == '#':
                    if cur_map_str is not None and cur_map_str[i][j] == '#':
                        draw_pix(draw, i, j, color_gray)
                    else:
                        draw_pix(draw, i, j, color_light_gray)
                elif map_str[i][j] == 'R':
                    draw_pix(draw, i, j, color_red)
                elif map_str[i][j] == 'P':
                    draw_pix(draw, i, j, color_light_red)
                elif map_str[i][j] == 'F':
                    draw_pix(draw, i, j, color_green)

        if node is not None:
            map_str[node.i][node.j] = 'R'
        if last_node is not None:
            map_str[last_node.i][last_node.j] = 'P'
        last_node = node

        images.append(im)

    images[0].save(filename, save_all=True, append_images=images[1:], optimize=False, duration=200, loop=0)
