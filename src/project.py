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
ground_color = (34, 139, 34)
player_vel = 5
window = pygame.display.set_mode((width, height))
ground_height = 50
ground_rect = pygame.Rect(0, height - ground_height, width * 2, ground_height)
font = pygame.font.SysFont("Arial", 30)


class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    gravity = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0

    def jump(self):
        self.y_vel = -self.gravity * 8  # Remove the quotes
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1


    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False

coin_list = pygame.sprite.Group()
for i in range(10):
    coin = Coin(i * 50 + 100, 550)
    coin_list.add(coin)

score = 0
goal = 10


def draw(window, player, coin_list, score):
    window.fill(bg_color) 
    pygame.draw.rect(window, ground_color, ground_rect)
    player.draw(window)
    coin_list.draw(window)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))
    pygame.display.update()


def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(player_vel)
    if keys[pygame.K_d]:
        player.move_right(player_vel)


def main(window):
    global score
    clock = pygame.time.Clock()
    player = Player(100, 100, 50, 50)
    run = True

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
            

        player.loop(fps)
        handle_move(player)
        if player.rect.colliderect(ground_rect):
            if player.y_vel > 0:
                player.rect.bottom = ground_rect.top
                player.y_vel = 0
                player.fall_count = 0
                player.jump_count = 0
        hits = pygame.sprite.spritecollide(player, coin_list, True)
        for hit in hits:
            score += 1
            print(f"Score: {score}")
        draw(window, player, coin_list, score)

    pygame.quit()


if __name__ == "__main__":
    main(window)