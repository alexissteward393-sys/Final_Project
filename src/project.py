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