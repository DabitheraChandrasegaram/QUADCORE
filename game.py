import pygame
import random #aliens fire at random times

# INITIALIZE PYGAME 
pygame.init()

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Defender")  # optional but good

# Load background picture
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load enemy images
enemy1_img = pygame.image.load("enemy1.png").convert_alpha()
enemy2_img = pygame.image.load("enemy2.png").convert_alpha()
enemy3_img = pygame.image.load("enemy3.png").convert_alpha()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        if enemy_type == 1:
            self.image = enemy1_img
            self.points = 10
        elif enemy_type == 2:
            self.image = enemy2_img
            self.points = 20
        elif enemy_type == 3:
            self.image = enemy3_img
            self.points = 30
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 1

# MAIN LOOP needed to keep the game running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))  # draw background first

    pygame.display.flip()  # update display 

pygame.quit()
 