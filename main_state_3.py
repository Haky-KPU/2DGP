from pico2d import *

import game_framework
import locate_state
import title_state

from Character import Character# import Boy class from Character.py
from Map import Map

name = "main_state_3"
Pause = False
iskey = False
clear_image = None
key_image = None
Door_image = None
boy = None
BackGround_index = [ {'name': '3_1.png', 'json': '3_1.json'},
                     {'name': '3_2.png', 'json': '3_2.json'},
                     {'name': '3_3.png', 'json': '3_3.json'},
                     {'name': '3_4.png', 'json': '3_4.json'},
                     {'name': '3_5.png', 'json': '3_5.json'},
                     {'name': '3_6.png', 'json': '3_6.json'},
                     {'name': '3_7.png', 'json': '3_7.json'},
                     {'name': '3_8.png', 'json': '3_8.json'}
                     ]
BackGround = []
bgm = None
stage_clear = False
cur_map = None
def create_world():
    global boy, BackGround, cur_map, key_image, Door_image, clear_image
    clear_image = load_image('clear.png')
    key_image = load_image('key.png')
    Door_image = load_image('Door.png')
    boy = Character()
    for i in range(8):
        BackGround.append(Map(BackGround_index[i]['name'], BackGround_index[i]['json']))
    Empty = 8
    BackGround.append(Empty)
    cur_map = 1
    play_bgm()

def play_bgm():
    global bgm
    bgm = load_music('game.mp3')
    bgm.set_volume(100)
    bgm.repeat_play()

def destroy_world():
    global boy, BackGround

    del(BackGround)
    del(boy)

   # del(grass)
   # del(big_balls)

def enter():
    open_canvas()
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(locate_state)
            else:
                boy.handle_event(event)



def collide(a, left_b, bottom_b, right_b, top_b):
    left_a, bottom_a, right_a, top_a = a.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True

def collide_type(a, left_b, bottom_b, right_b, top_b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    collide_x, collide_y = a.get_pos()
    bottom_Up, top_Up = top_b, top_b + 11
    bottom_Down, top_Down = bottom_b - 11, bottom_b

    if (right_a > left_b and right_a < right_b) or (left_a > left_b and left_a < right_b):
        if collide_y > bottom_Up and collide_y < top_Up:
            return 0
        elif (top_a > bottom_Down and top_a  > top_Down) or (bottom_a > bottom_Down and bottom_a  > top_Down) :
            return 1

def collide_type2(a, left_b, bottom_b, right_b, top_b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    collide_x, collide_y = a.get_pos()
    left_Left, right_Left = left_b - 22, left_b
    left_Right, right_Right = right_b, right_b + 22

    if (top_a < top_b and top_a > bottom_b) or (bottom_a < top_b and bottom_a > bottom_b):
        #if (right_a < right_Left and right_a > left_Left) or (left_a < right_Left and left_a > left_Left):
        if collide_x < right_Left and collide_x > left_Left:
            return 2
        #elif (right_a < right_Right and right_a > left_Right) or (left_a < right_Right and left_a > left_Right):
        elif collide_x < right_Right and collide_x > left_Right:
            return 3


def update(frame_time):
    global cur_map, iskey, stage_clear
    if not Pause:
        isFloor = False
        type = -1
        x, y = 0, 0
        boy.update(frame_time)
        collide_index = BackGround[cur_map].get_bb()

        for i in range(len(collide_index)):
            if collide(boy, collide_index[i][0], collide_index[i][1], collide_index[i][2], collide_index[i][3]):
                type = collide_type(boy, collide_index[i][0], collide_index[i][1], collide_index[i][2],
                                        collide_index[i][3])
                if type == 0:
                    isFloor = True
                    y = collide_index[i][3]
                elif type == 1:
                   y = collide_index[i][1]


                type = collide_type2(boy, collide_index[i][0], collide_index[i][1], collide_index[i][2], collide_index[i][3])
                if type == 2:
                    x = collide_index[i][0]
                elif type == 3:
                    x = collide_index[i][2]
        if collide(boy, 682, 0, 704, 528):
            boy.move_pos()
            cur_map = 0
        if collide(boy, 0, 0, 22, 528):
            boy.move_pos()
            cur_map = 4

        if cur_map == 4:
            if collide(boy, 19*22, 4*22, 20*22, 5*22):
                iskey = True
        if cur_map == 0:
            if iskey:
                if collide(boy, 29*22, 18*22, 30*22, 20*22):
                    stage_clear = True


        boy.collide_update(isFloor, x, y)



def draw(frame_time):
    global BackGround
    clear_canvas()
    if not stage_clear:
        BackGround[cur_map].draw()
        if iskey == False:
            if cur_map == 4:
                key_image.draw(19*22, 4*22)
            elif cur_map == 0:
                Door_image.clip_draw(23, 0, 22, 44, 29*22, 18*22)
        else:
            if cur_map == 0:
                Door_image.clip_draw(0, 0, 22, 44, 29*22, 18*22)
        boy.draw()
        boy.draw_bb()
        BackGround[cur_map].draw_bb()
    else:
        clear_image.draw(400, 300)

    update_canvas()






