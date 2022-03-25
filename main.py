import pygame
import numpy as np

pygame.init()
running=True
width=800
height=600
Color_screen=(22,22,28)
Color_line=(255,0,0)
Color_line2=(255,255,0)
Color_line3=(255,0,255)

screen=pygame.display.set_mode((width,height))
screen.fill(Color_screen)

b0 = np.array([ 0,  0])
b1 = np.array([ 0, 27])
b2 = np.array([27, 27])
b3 = np.array([27,  0])

screen_size = np.array([width, height])

seconds = lambda: pygame.time.get_ticks()/1000

direction = 1

def draw():
    screen.fill(Color_screen)
    if direction == 1:
        pygame.draw.line(screen,Color_line,(seconds() * 100,80),(130,100))
    elif direction == -1:
        pygame.draw.line(screen,Color_line2,(seconds() * 100,80),(130,100))
    elif direction == 2:
        pygame.draw.line(screen,Color_line3,(seconds() * 100,80),(130,100))
    pygame.display.flip()
    pygame.display.update()

def handle_events():
    global running, direction
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running=False
        if events.type == pygame.KEYDOWN:
            direction = -1
        if events.type == pygame.CONTROLLER_AXIS_LEFTY:
            direction = 2
        

def main():
    while running:
        draw()
        handle_events()
    pygame.quit()
    quit()

if __name__=='__main__':
    main()