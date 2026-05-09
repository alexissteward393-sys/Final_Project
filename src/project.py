import os
import random
import math
import pygame
from os import listdir
from os import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

bg_color = (255, 255, 255)
width, height = 800, 500
fps = 60
player_vel = 5

window = pygame.display.set_mode((width, height))

def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)