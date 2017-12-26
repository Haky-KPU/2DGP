import random

from pico2d import *


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

class Character:
    #캐릭터의 속성. 픽셀당 센티 및 움직이는 속도.
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    JUMP_SPEED_KMPH = 30.0  # Km / Hour
    JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    stand_image = None
    walk_image = None
    jump_fall_image = None

    #일반 STATE
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3

    #JUMP STATE
    JUMP_RIGHT, JUMP_LEFT, FALL_RIGHT, FALL_LEFT, JUMP_READY = 11, 10, 9, 8, 4


    def __init__(self):
        self.x, self.y = 150, 200

        self.Max_y = 528
        self.Min_y = 88
        self.Max_x = 704
        self.Min_x = 0

        self.frame = random.randint(0, 7)
        self.life_time = 0.0
        self.total_frames = 0.
        self.dir = 00
        self.state = self.RIGHT_STAND

        self.jump_state = self.JUMP_READY
        self.jump_max_y = 0  # Jump시 올라가는 Y의 최대점.
        self.jump_cur_y = 0
        self.jump_frame = 0
        self.frame_count = 0
        self.max_frame_count = 18

        if Character.walk_image == None:
            Character.walk_image = load_image('Walk_Sheet.png')

        if Character.stand_image == None:
            Character.stand_image = load_image('Stand_Sheet.png')

        if Character.jump_fall_image == None:
            Character.jump_fall_image = load_image('Jump_Fall_Sheet.png')


    def update(self, frame_time):


        self.life_time += frame_time
        distance = Character.RUN_SPEED_PPS * frame_time
        self.total_frames += Character.FRAMES_PER_ACTION * Character.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.dir * distance)
        self.Jump(frame_time)
        self.y = clamp(self.Min_y, self.y, self.Max_y)
        self.x = clamp(self.Min_x, self.x, self.Max_x)

    def Jump(self, frame_time):
        if self.jump_state in (self.JUMP_LEFT, self.JUMP_RIGHT):
            if 0 < self.jump_max_y : #y 증가
                self.y += (Character.JUMP_SPEED_PPS * frame_time)
                self.jump_max_y -= (Character.JUMP_SPEED_PPS * frame_time)

                if self.jump_frame < 1: #frame 증가
                    if self.frame_count < self.max_frame_count:
                        self.frame_count += 1
                    else:
                        self.frame_count = 0
                        self.jump_frame += 1
            else:
                if self.jump_state == self.JUMP_RIGHT: #jump_state 변경
                    self.jump_state = self.FALL_RIGHT
                    self.jump_frame = 0
                elif self.jump_state == self.JUMP_LEFT:
                    self.jump_state = self.FALL_LEFT
                    self.jump_frame = 0

        elif self.jump_state in (self.FALL_LEFT, self.FALL_RIGHT):
            self.y -= (Character.JUMP_SPEED_PPS * frame_time) #y 감소
            if self.jump_frame < 2:#frame 증가
                if self.frame_count < self.max_frame_count:
                     self.frame_count += 1
                else:
                     self.frame_count = 0
                     self.jump_frame += 1

        elif self.jump_state in (self.JUMP_READY,):#평상시 MaxJump 계산
            self.jump_max_y = 200
            self.jump_cur_y = self.y
            self.jump_frame = 0
            self.frame_count = 0

    def draw(self):
        if self.state in (self.LEFT_RUN, self.RIGHT_RUN):
            if self.jump_state in (self.JUMP_LEFT, self.FALL_LEFT, self.JUMP_RIGHT, self.FALL_RIGHT ):
                self.jump_fall_image.clip_draw(self.jump_frame * 32, (self.jump_state % 4) * 40, 32, 40, self.x, self.y)
            else:
                self.walk_image.clip_draw(self.frame * 32, self.state * 40, 32, 40, self.x, self.y)
        elif self.state in (self.LEFT_STAND, self.RIGHT_STAND):
            if self.jump_state in (self.JUMP_LEFT, self.FALL_LEFT, self.JUMP_RIGHT, self.FALL_RIGHT):
                self.jump_fall_image.clip_draw(self.jump_frame * 32, (self.jump_state % 4) * 40, 32, 40, self.x, self.y)
            else:
                self.stand_image.clip_draw(0, (self.state - 2) * 40, 32, 40, self.x, self.y)

    def collide_update(self, isFloor, x, y):
        if isFloor:
            if self.jump_state in (self.FALL_LEFT, self.FALL_RIGHT):
                self.jump_state = self.JUMP_READY
        else:
            if self.jump_state in (self.JUMP_READY,):
                if self.state in (self.RIGHT_STAND, self.RIGHT_RUN):
                    self.jump_state = self.FALL_RIGHT
                elif self.state in (self.LEFT_STAND, self.LEFT_RUN):
                    self.jump_state = self.FALL_LEFT
        if y != 0:
            if self.y > y:
                self.Min_y = y
                self.Max_y = 528
            else:
                self.Max_y = y - 11
                self.Min_y = 88
        else:
            self.Max_y = 528
            self.Min_y = 88

        if x != 0:
            if self.x > x:
                self.x = clamp(x, self.x, self.Max_x)

            else:
                self.x = clamp(self.Min_x, self.x, x)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def move_pos(self):
        if self.x > 600:
            self.x = 55
            self.y += 11
        else:
            self.x = 664
            self.y += 11

    def get_pos(self):
        return self.x, self.y

    def get_bb(self):
        return self.x - 16, self.y - 20, self.x + 16, self.y + 16

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state = self.LEFT_RUN
                self.dir = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.RIGHT_RUN
                self.dir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.jump_state == self.JUMP_READY:
                if self.state in (self.RIGHT_STAND, self.RIGHT_RUN):
                    self.jump_state = self.JUMP_RIGHT
                elif self.state in (self.LEFT_STAND, self.LEFT_RUN):
                    self.jump_state = self.JUMP_LEFT





