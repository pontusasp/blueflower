import pygame
import numpy as np

pygame.init()
running=True
width=800
height=600
Color_screen=(22,22,28)
Color_blueflower=(0, 120, 215)

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('BLUEFLOWER')

def load_tile(name):
    return pygame.transform.scale(pygame.image.load(f'textures/tiles/{name}.png'), (64, 64))

tiles = {
    "grass": load_tile('red-painter-man41')
}

screen_size = np.array([width, height])

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

def draw_scene1():
    screen.fill(Color_screen)
    screen.blit(tiles["grass"], (x, y))

def update_scene1():
    global x, scene
    if key["d"]:
        x += 1
    if key["a"]:
        x -= 1

def draw_scene2():
    screen.fill(Color_screen)

def update_scene2():
    pass

def draw_scene3():
    screen.fill(Color_blueflower)

def update_scene3():
    pass

def draw():
    global x
    if scene == 1:
        draw_scene1()
    if scene == 2:
        draw_scene3()
    if scene == 3:
        draw_scene3()
    pygame.draw.line(screen,Color_blueflower,(x,80),(130,100))
    pygame.display.flip()
    pygame.display.update()


def handle_keyboard(keypress, keydown):
    global key
    if keypress == pygame.K_w:
        key["w"] = keydown
    if keypress == pygame.K_a:
        key["a"] = keydown
    if keypress == pygame.K_s:
        key["s"] = keydown
    if keypress == pygame.K_d:
        key["d"] = keydown


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


def main():
    while running:
        draw()
        handle_events()
        update()
    pygame.quit()
    quit()

if __name__=='__main__':
    main()