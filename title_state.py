from pico2d import *
import game_framework
import main_state_3

name = "TitleState"
image = None
bgm = None

def enter():
    global image
    image = load_image('title.png')
    play_bgm()
    pass

def play_bgm():
    global bgm
    bgm = load_music('title.mp3')
    bgm.set_volume(100)
    bgm.repeat_play()


def exit():
    global image
    del(image)
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
                game_framework.change_state(main_state_3)
    pass


def draw(frame_time):
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass



def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






