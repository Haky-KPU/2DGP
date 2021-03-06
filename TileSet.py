__author__ = 'dustinlee'

import json

from pico2d import *

class TileSet:

    def __init__(self):
        self.firstgid = 0

    def load(self, file_name):
        f = open(file_name)
        data = json.load(f)
        f.close()
        self.__dict__.update(data)
        print(self.__dict__)
        self.base_image = load_image(self.image)
        self.tile_images = []
        for i in range(self.tilecount):
            col, row = i % self.columns, i // self.columns
            left = col * self.tilewidth
            bottom = self.base_image.h - (row + 1) * self.tileheight
            image = self.base_image.clip_image(left, bottom, self.tilewidth, self.tileheight)
            self.tile_images.append(image)

def load_tile_set(file_name):
    tile_set = TileSet()
    tile_set.load(file_name)

    return tile_set

if __name__ =='__main__':
    open_canvas(800, 600)

    tile_set = load_tile_set('desert_tileset.json')

    for i in range(tile_set.tilecount):
        col = i % tile_set.columns
        row = i // tile_set.columns
        tile_set.tile_images[i].draw_to_origin(400 + col * tile_set.tilewidth,
                                               300 + row * tile_set.tileheight)

    update_canvas()
    delay(5)
    close_canvas()