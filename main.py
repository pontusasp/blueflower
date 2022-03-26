import math
import pygame
import numpy as np
import pyautogui

pygame.init()
screenshot_raw = pyautogui.screenshot('resources/screenshot.png')
screenshot = pygame.image.load('resources/screenshot.png')
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
    'flower': load_tile('red-painter-man41'),
    'bucket': load_tile('bucket')
}


bg = pygame.image.load(r'resources/bsod.png')
shrug = pygame.image.load(r'resources/shrug.png')

smileyFont = pygame.font.Font('resources/font/segoeui.ttf', 155)
smiley = smileyFont.render(':(', True, color_white)
smileyRect = smiley.get_rect()
smileyRect.center = (3*width/10, 5*height/12)

lolJk = smileyFont.render('¯\_(ツ)_/¯', True, color_white)

font = pygame.font.Font('resources/font/segoeui.ttf', 30)
loadingText = []
for i in range(101):
    loadingText.append(font.render(f'{i}% complete', True, color_white))

smallFont = pygame.font.Font('resources/font/segoeui.ttf', 14)

seconds = lambda: pygame.time.get_ticks()/1000

key = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
}

x = width/2-tiles['flower'].get_width()/2
y = height-tiles["flower"].get_height()

scene = 1
fullscreen = False
fullscreen_time = seconds()

flowers = []

gravity = 100

speed = 0.5
score = 0

def flower_respawn(i):
    global flowers
    flowers[i][0] = round(np.random.uniform() * (width - tiles['flower'].get_width()))
    flowers[i][1] = -(seconds() * gravity + tiles['flower'].get_height()) - np.random.uniform() * bg.get_height()

def draw_scene1():
    screen.fill(color_screen)
    screen.blit(tiles['bucket'], (x, y))
    for flower in flowers:
        screen.blit(tiles['flower'], (flower[0], flower[1]+gravity*seconds()))

def update_scene1():
    global x, scene, score, gravity, speed
    if key["d"]:
        x += speed
    if key["a"]:
        x -= speed

    leftx = x - tiles['bucket'].get_width()/2
    rightx = x + tiles['bucket'].get_width()/2

    if math.log2(round(seconds()+1+score)) > len(flowers):
        flowers.append([round(np.random.uniform() * (width - tiles['flower'].get_width())), -(seconds() * gravity + tiles['flower'].get_height())])

    for i in range(len(flowers)):
        if flowers[i][1] > -(seconds() * gravity - height + tiles['bucket'].get_height() + tiles['flower'].get_height()):
            if leftx <= flowers[i][0] and flowers[i][0] <= rightx:
                print(f'flower catch {seconds()}')
                score += 1
                gravity += 1
                speed += 0.05
                flower_respawn(i)
        elif flowers[i][1] > -(seconds() * gravity - height):
            print(f'respawn {seconds()}')
            flower_respawn(i)
        
    
    if x > width:
        scene = 3

def draw_scene2():
    screen.fill(color_screen)
    screen.blit(screenshot, (0, 0))
    for flower in flowers:
        screen.blit(tiles['flower'], (flower[0], flower[1]+gravity*seconds()))

def update_scene2():
    global score, gravity
    if math.log1p(round(seconds()+1)) > len(flowers):
        flowers.append([round(np.random.uniform() * (width - tiles['flower'].get_width())), -(seconds() * gravity + tiles['flower'].get_height())])

    for i in range(len(flowers)):
        if flowers[i][1] > -(seconds() * gravity - height):
            flower_respawn(i)
            gravity += 10

def pre_update_scene2():
    global width, height
    width = bg.get_width()
    height = bg.get_height()

def draw_scene3():
    if seconds() - fullscreen_time < 1:
        screen.fill(color_black)
    elif round((seconds() - fullscreen_time - 1) * 20) <= 100:
        screen.fill(color_blueflower)
        screen.blit(bg, (0,0))
        screen.blit(loadingText[min(round((seconds() - fullscreen_time - 1) * 20), 100)], (bg.get_width() * 0.1075, bg.get_height() * 0.555))
    else:
        screen.fill(color_blueflower)
        screen.blit(shrug, (bg.get_width()//2 - shrug.get_width()//2, bg.get_height()//2 - shrug.get_height()//2))


def update_scene3():
    global running, scene
    if seconds() - fullscreen_time > 8:
        scene=2

def pre_update_scene3():
    global fullscreen, bg, fullscreen_time, shrug
    if not fullscreen:
        fullscreen_time = seconds()
        pygame.mouse.set_visible(False)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        bg_w0 = bg.get_width()
        bg = pygame.transform.scale(bg, (display_info.current_w, display_info.current_h)) 
        bg_w1 = bg.get_width()
        shrug = pygame.transform.scale(shrug, (math.floor(shrug.get_width()*bg_w1/bg_w0), math.floor(shrug.get_height()*bg_w1/bg_w0)))
        fullscreen=True


def draw():
    global x
    if scene == 1:
        draw_scene1()
    if scene == 2:
        draw_scene2()
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


def rescale(scale):
    global screen, width, height, gravity, x, y, speed, flowers
    x *= scale
    y *= scale
    speed *= scale
    gravity *= scale

    for i in range(len(flowers)):
        flowers[i][0] *= scale
        flowers[i][1] *= scale

    for key in tiles:
        tiles[key] = pygame.transform.scale(tiles[key], (tiles[key].get_width() * scale, tiles[key].get_height() * scale))

    width = math.floor(width * scale)
    height = math.floor(height * scale)
    screen=pygame.display.set_mode((width,height))

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rescale(0.75)
            running=width>50
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
    if scene == 2:
        pre_update_scene2()
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