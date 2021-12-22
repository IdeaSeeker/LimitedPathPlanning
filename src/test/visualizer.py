import config
config.configure_imports()

from Map import Map
from PIL import Image, ImageDraw
from data_parser import read_map


color_black = (0, 0, 0)
color_gray = (100, 100, 100)
color_white = (255, 255, 255)


def draw_path(full_map: Map, path: list, filename = 'path'):
    k = 20
    quality = 5
    hIm = full_map._height * k
    wIm = full_map._width * k

    images = []
    for step in range(len(path)):
        for n in range(quality):
            im = Image.new('RGB', (wIm, hIm), color='white')
            draw = ImageDraw.Draw(im)
            for i in range(full_map._height):
                for j in range(full_map._width):
                    if full_map._cells[i][j] is None and step % 2 == 0:
                        draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=color_gray)
            images.append(im)

    images[0].save('./' + filename + '.gif', save_all=True, append_images=images[1:], optimize=False, duration=500/quality, loop=0)


map_file = 'data\lak105d.map'
map_str, map_width, map_height = read_map(map_file)
_map = Map()
_map.read_from_string(map_width, map_height, map_str)
draw_path(_map, [1] * 8)