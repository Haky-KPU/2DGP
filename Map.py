import random
from LoadCollision import load_collision_map
from pico2d import *

class Map:

    def __init__(self, name, json):
        self.w, self.h = 704, 528
        self.x, self.y = 352, 264
        self.image = load_image(name)
        self.collision_map = load_collision_map(json)



    def update(self, frame_time):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        self.collision_map.draw_bb()

    def get_bb(self):
        return self.collision_map.get_bb()

    def get_move_bb(self):
        return self.collision_map.get_move_bb()
