__author__ = 'dustinlee'

import json

from pico2d import *


class LoadCollision:

    CollisionTile =  [1, 2, 3, 4, 7, 8]
    MoveTile = 11
    def load(self, name):
        f = open(name)
        info = json.load(f)
        f.close()
        self.__dict__.update(info)
        self.move = self.layers[0]['data']
        self.data = self.layers[1]['data']

        new_data = []
        for row in reversed(range(self.height)):
            new_data.append(self.data[row * self.width : row * self.width + self.width])
        self.data = new_data

        new_move = []
        for row in reversed(range(self.height)):
            new_move.append(self.move[row * self.width: row * self.width + self.width])
        self.data = new_move

        collisiondata = []

        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x] in self.CollisionTile:
                    data = [x * self.tilewidth, y * self.tileheight, (x + 1) * self.tilewidth, (y + 1) * self.tileheight ]
                    collisiondata.append(data)

        self.data = collisiondata

    def draw_bb(self):#left, bottom, width, height, dx, dy
        for index in range(len(self.data)):
            draw_rectangle(self.data[index][0], self.data[index][1],
                           self.data[index][2], self.data[index][3])
            # self.data[y][x] - self.firstgid].draw_to_origin((x - tl) * self.tilewidth - lo,(y - tb) * self.tileheight - bo)

    def get_bb(self):
        return self.data

    def get_move_bb(self):
        return self.move

def load_collision_map(name):
    Collision_map = LoadCollision()
    Collision_map.load(name)

    return Collision_map



