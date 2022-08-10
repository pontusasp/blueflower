import math
import pygame
import numpy as np
import win32gui # pywin32
import win32con # pywin32

pygame.init()
running=True
width=800
height=600
screen_size = np.array([width, height])
color_blueflower=(0, 120, 215)
color_white=(255, 255, 255)
color_black=(0, 0, 0)
hwnd=None

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('BLUEFLOWER')

bg = bg1 = pygame.image.load(r'resources/bsod.png')
bg2 = pygame.image.load(r'resources/bsod2.png')
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

fullscreen = False
fullscreen_time = seconds()

def draw():
    if seconds() - fullscreen_time < 1:
        screen.fill(color_black)
    elif round((seconds() - fullscreen_time - 1) * 20) <= 100:
        screen.fill(color_blueflower)
        screen.blit(bg, (0,0))
        screen.blit(loadingText[min(round((seconds() - fullscreen_time - 1) * 20), 100)], (bg.get_width() * 0.1075, bg.get_height() * 0.555))
    else:
        screen.fill(color_blueflower)
        screen.blit(shrug, (bg.get_width()//2 - shrug.get_width()//2, bg.get_height()//2 - shrug.get_height()//2))
    pygame.display.flip()
    pygame.display.update()

def pre_update():
    global fullscreen, bg, fullscreen_time, shrug, hwnd
    if hwnd is None:
        hwnd = win32gui.GetForegroundWindow()
        pygame.display.iconify()
    elif not fullscreen and seconds() > 10:
        print("10 s passed")
        #if win32gui.IsIconic(hwnd):
        #win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.BringWindowToTop(hwnd)
        fullscreen_time = seconds()
        pygame.mouse.set_visible(False)
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        if display_info.current_w / display_info.current_h < 1.6:
            bg = bg2
        bg_w0 = bg.get_width()
        bg = pygame.transform.scale(bg, (display_info.current_w, display_info.current_h)) 
        bg_w1 = bg.get_width()
        shrug = pygame.transform.scale(shrug, (math.floor(shrug.get_width()*bg_w1/bg_w0), math.floor(shrug.get_height()*bg_w1/bg_w0)))
        fullscreen=True


def handle_keyboard(keypress, keydown):
    global running
    if keypress == pygame.K_ESCAPE:
        running=False

def handle_events():
    global running, width, height
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            handle_keyboard(event.key, True)
        if event.type == pygame.KEYUP:
            handle_keyboard(event.key, False)


def main():
    while running:
        pre_update()
        draw()
        handle_events()
    pygame.quit()
    quit()

if __name__=='__main__':
    main()