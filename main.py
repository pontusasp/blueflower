import math
import pygame
import numpy as np
import pyautogui

pygame.init()
screenshot_raw = pyautogui.screenshot('resources/screenshot.png')
bg = pygame.image.load('resources/screenshot.png')
running=True
width=bg.get_width()
height=bg.get_height()
screen_size = np.array([width, height])
color_screen=(22,22,28)
color_blueflower=(0, 120, 215)
color_white=(255, 255, 255)
color_black=(0, 0, 0)

screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption('BLUEFLOWER')

def load_tile(name):
    return pygame.transform.scale(pygame.image.load(f'resources/tiles/{name}.png'), (64, 64))

tiles = {
    'flower': [
        load_tile('red-painter-man41'),
        load_tile('red-painter-man40'),
        load_tile('red-painter-man38'),
        load_tile('red-painter-man43')
    ]
}

flower_width = tiles['flower'][0].get_width()
flower_height = tiles['flower'][0].get_height()

seconds = lambda: pygame.time.get_ticks()/1000

fullscreen = False
fullscreen_time = seconds()

flowers = []

gravity = 100

score = 100

def flower_respawn(i):
    global flowers
    flowers[i][0] = round(np.random.uniform() * (width - flower_width))
    flowers[i][1] = -(seconds() * gravity + flower_height) - np.random.uniform() * height
    flowers[i][2] = np.random.randint(0, len(tiles['flower']))

def draw_scene2():
    screen.fill(color_screen)
    screen.blit(bg, (0, 0))
    for flower in flowers:
        screen.blit(tiles['flower'][flower[2]], (flower[0], flower[1]+gravity*seconds()))

def update_scene2():
    global score, gravity
    if math.log1p(round(seconds()+1+score*10)) > len(flowers):
        flowers.append([round(np.random.uniform() * (width - flower_width)), -(seconds() * gravity*10 + flower_height), np.random.randint(0, len(tiles['flower']))])
        flower_respawn(len(flowers)-1)

    for i in range(len(flowers)):
        if flowers[i][1] > -(seconds() * gravity - height):
            flower_respawn(i)
            score += 1

def draw():
    draw_scene2()
    pygame.display.flip()
    pygame.display.update()

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            pygame.mouse.set_visible(True)
            running=False

def main():
    while running:
        draw()
        handle_events()
        update_scene2()
    pygame.quit()
    quit()

if __name__=='__main__':
    main()