import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

bg_color = (255, 255, 255)
width, height = 1200, 650
fps = 60
window = pygame.display.set_mode((width, height))

class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

def draw(window, player):
    window.fill(bg_color) 
    player.draw(window)
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    player = Player(100, 100, 50, 50)
    run = True

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw(window, player)

    pygame.quit()

if __name__ == "__main__":
    main(window)