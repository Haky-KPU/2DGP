from pico2d import *
import json
import game_framework
import main_state_3

class map_object:



    def __init__(self, pos):
        Empty_pos = pos

    def draw(self):
        self.image.draw(self.x, self.y, 200, 150)

    def update(self):
        self.update_location()

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            pass
    pass
    def update_location(self):
        if self.Location in (self.LTOP, self.TOP, self.RTOP):
            self.y = (150 * 2) + (37.5 * 3) + 100
        elif self.Location in (self.LEFT, self.MID, self.RIGHT):
            self.y = (150 * 1) + (37.5 * 2) + 100
        else:
            self.y = (150 * 0) + (37.5 + 1) + 100
        if self.Location in (self.RTOP, self.RIGHT, self.RBOTTOM):
            self.x = (200 * 2) + (50 * 3) + 75
        elif self.Location in (self.TOP, self.MID, self.BOTTOM):
            self.x = (200 * 1) + (50 * 2) + 75
        else:
            self.x = (200 * 0) + (50 + 1) + 75