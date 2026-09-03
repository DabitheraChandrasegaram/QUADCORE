import pygame
import random #aliens fire at random times

# INITIALIZE PYGAME 
pygame.init()

# Screen size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Defender")  # optional but good

# Load background picture
background = pygame.image.load("background1.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load enemy images
enemy1_img = pygame.image.load("enemy1.png").convert_alpha()
enemy2_img = pygame.image.load("enemy2.png").convert_alpha()
enemy3_img = pygame.image.load("enemy3.png").convert_alpha()

# MAIN LOOP needed to keep the game running

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))  # draw background first

    update_enemies()  # update enemy positions

    enemy_group.draw(screen)  # draw enemies

    pygame.display.flip()  # update display 

pygame.quit()
 