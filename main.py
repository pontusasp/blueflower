import pygame
import numpy as np

pygame.init()
running=True
width=800
height=600
screen_size = np.array([width, height])
color_screen=(22,22,28)
color_blueflower=(0, 120, 215)
color_white=(255, 255, 255)
color_black=(0, 0, 0)

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('BLUEFLOWER')

def load_tile(name):
    return pygame.transform.scale(pygame.image.load(f'resources/tiles/{name}.png'), (64, 64))

tiles = {
    "grass": load_tile('red-painter-man41')
}


bg = pygame.image.load(r'resources/bsod.png')

smileyFont = pygame.font.Font('resources/font/segoeui.ttf', 155)
smiley = smileyFont.render(':(', True, color_white)
smileyRect = smiley.get_rect()
smileyRect.center = (3*width/10, 5*height/12)

font = pygame.font.Font('resources/font/segoeui.ttf', 30)
smallFont = pygame.font.Font('resources/font/segoeui.ttf', 14)

seconds = lambda: pygame.time.get_ticks()/1000

key = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
}

direction = 1

x = 0
y = 1

scene = 1
fullscreen = False
fullscreen_time = seconds()

def draw_scene1():
    screen.fill(color_screen)
    screen.blit(tiles["grass"], (x, y))

def update_scene1():
    global x, scene
    if key["d"]:
        x += 1
    if key["a"]:
        x -= 1
    if x > width:
        scene = 3

def draw_scene2():
    screen.fill(color_screen)

def update_scene2():
    pass

def draw_scene3():
    if seconds() - fullscreen_time < 1:
        screen.fill(color_black)
    else:
        screen.fill(color_blueflower)
        screen.blit(bg, (0,0))

def update_scene3():
    pass

def pre_update_scene3():
    global fullscreen, bg, fullscreen_time
    if not fullscreen:
        fullscreen_time = seconds()
        pygame.mouse.set_visible(False)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        bg = pygame.transform.scale(bg, (display_info.current_w, display_info.current_h)) 
        fullscreen=True


def draw():
    global x
    if scene == 1:
        draw_scene1()
    if scene == 2:
        draw_scene3()
    if scene == 3:
        draw_scene3()
    pygame.display.flip()
    pygame.display.update()


def handle_keyboard(keypress, keydown):
    global key, running
    if keypress == pygame.K_w:
        key["w"] = keydown
    if keypress == pygame.K_a:
        key["a"] = keydown
    if keypress == pygame.K_s:
        key["s"] = keydown
    if keypress == pygame.K_d:
        key["d"] = keydown
    if keypress == pygame.K_ESCAPE:
        running=False


def handle_events():
    global running, direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            handle_keyboard(event.key, True)
        if event.type == pygame.KEYUP:
            handle_keyboard(event.key, False)

def update():
    if scene == 1:
        update_scene1()
    if scene == 2:
        update_scene2()
    if scene == 3:
        update_scene3()

def pre_update():
    if scene == 3:
        pre_update_scene3()


def main():
    while running:
        pre_update()
        draw()
        handle_events()
        update()
    pygame.quit()
    quit()

if __name__=='__main__':
    main()