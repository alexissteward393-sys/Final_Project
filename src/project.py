import os
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Gloop Glade")

game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, 'assets')
bg_color = (0, 150, 200)
width, height = 1200, 650
fps = 60
player_vel = 4
window = pygame.display.set_mode((width, height))
bg_image = pygame.image.load(os.path.join(asset_folder, 'background.png')).convert()
bg_image = pygame.transform.scale(bg_image, (1300, 590)) 
font = pygame.font.SysFont("Arial", 30)
win_image = pygame.image.load(os.path.join(asset_folder, "win_screen.png")).convert_alpha()
win_image = pygame.transform.scale(win_image, (1300, 700)) 


def get_block(size):
    path = os.path.join(asset_folder, "terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    color = (255, 0, 0)
    gravity = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        full_image = pygame.image.load(os.path.join(asset_folder, 'player.png')).convert_alpha()
        self.image = pygame.transform.scale(full_image, (int(width * 1.5), int(height * 1.5)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
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
    

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    
    def hit_head(self):
        self.count = 0
        self.y_vel += -1

    def reset(self, x, y):
     self.rect.x = x
     self.rect.y = y
     self.y_vel = 0
     self.x_vel = 0
     self.jump_count = 0
     self.fall_count = 0
     self.hit = False

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__() 
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 100, 255, 150)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "water"

    def draw(self, window, offset_x):
        pygame.draw.rect(window, (0, 0, 255), self.rect.move(-offset_x, 0))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, "spider.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = 1
        self.vel = 2

    def update(self, objects):
        self.rect.x += self.vel * self.direction
        
        for obj in objects:
            if self.rect.colliderect(obj.rect) and not isinstance(obj, Water):
                self.direction *= -1
                self.rect.x += self.vel * self.direction
                break


    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        

class Flowers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(asset_folder, "flowers.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

flower_list = pygame.sprite.Group()
for i in range(10):
    flower = Flowers(i * 50 + 100, 550)
    flower_list.add(flower)

score = 0
goal = 20


def draw(window, player, flower_list, enemies, score, objects, offset_x):
    window.blit(bg_image, (0, 0))
    player.draw(window, offset_x)

    for flower in flower_list:
        flower.draw(window, offset_x)
    
    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)

    score_text = font.render(f"Flowers: {score}/{goal}", True, (255, 255, 255)) 
    window.blit(score_text, (15, 15))

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if isinstance(obj, Water): continue
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        collided_objects.append(obj)
    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break       
    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -player_vel * 2)
    collide_right = collide(player, objects, player_vel * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(player_vel)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(player_vel)
    handle_vertical_collision(player, objects, player.y_vel)


def setup_level(layout, block_size):
    objects = []                
    flowers_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * block_size
            y = row_index * block_size
            if cell == "B":
                objects.append(Block(x, y, block_size))
            elif cell == "E":
                enemy = Enemy(x, y + (block_size - 40), 40, 40)
                enemies_group.add(enemy)                
            elif cell == "C":                
                flower_y = y + (block_size - 64) 
                flower = Flowers(x, flower_y)
                flowers_group.add(flower)
            elif cell == "W":
                objects.append(Water(x, y + (block_size // 2), block_size))
    return objects, flowers_group, enemies_group


LEVEL_MAP = [
    "B                                                                                                            C                               ",
    "B                          C                                                        C                   C   BBB                B    CEB      ",
    "B               C      C   B   C                                                    B                   B        B          B  BBBBBBBBB     ",
    "B               B      B       B         C                                            B                            B   C  B                  ",
    "B            B            BBB            B             C  C  C                     B      B   C               B      BBB                     ",
    "B      C                             B      EB      B  B  B  B  B   C E  E C  E  B            B    C  E   B E   E C  E  E    E  C            B",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBWWWWWWWWWWWBBBBBBBBBBBBBBBBBBBWWWWWWWWWBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" 
]


def draw_text_box(surface, text, font, color, rect_color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x + 10, y + 5)
    box_rect = pygame.Rect(x, y, text_obj.get_width() + 20, text_obj.get_height() + 10)
    pygame.draw.rect(surface, rect_color, box_rect)
    surface.blit(text_obj, text_rect)


def main(window):
    global score
    clock = pygame.time.Clock()
    player = Player(100, 100, 50, 50)
    block_size = 96
    objects, flower_list, enemies = setup_level(LEVEL_MAP, block_size)
    player = Player(100, height - block_size * 2, 50, 50)
    offset_x = 0
    scroll_area_width = 200
    tutorial_text_timer = 0
    show_tutorial_text = True 
    font = pygame.font.SysFont("Arial", 30)

   
    run = True

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        if score >= 20:
            window.blit(win_image, (0, 0))
            pygame.display.update()
            
            # Keep the window open until the player quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            continue

        player.loop(fps) 
        handle_vertical_collision(player, objects, player.y_vel)
        handle_move(player, objects)

        for enemy in enemies:
            enemy.update(objects)

        water_objects = pygame.sprite.Group()
        for obj in objects:
            if isinstance(obj, Water):
                water_objects.add(obj)
                if pygame.sprite.spritecollideany(player, water_objects, pygame.sprite.collide_mask):
                    objects, flower_list, enemies = setup_level(LEVEL_MAP, block_size) 
                    player = Player(100, height - block_size * 2, 50, 50)
                    offset_x = 0
                    score = 0 
        
        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            player = Player(100, height - block_size * 2, 50, 50)
            objects, flower_list, enemies = setup_level(LEVEL_MAP, block_size)
            offset_x = 0
            score = 0 
        
        hits = pygame.sprite.spritecollide(player, flower_list, True)
        for hit in hits:
            score += 1
            show_tutorial_text = False 
            print(f"Score: {score}")

        draw(window, player, flower_list, enemies, score, objects, offset_x)
        
        if ((player.rect.right - offset_x >= width - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if show_tutorial_text:
            msg1 = font.render("Use A & D to move, Space to jump", True, (255, 255, 255))
            msg2 = font.render("Collect flowers to a crown", True, (255, 255, 255))
            window.blit(msg1, (width // 2 - msg1.get_width() // 2, height // 2 - 40))
            window.blit(msg2, (width // 2 - msg2.get_width() // 2, height // 2))
        pygame.display.update()
        

    pygame.quit()


if __name__ == "__main__":
    main(window)