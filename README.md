# QUADCORE
CW1 - Space Invaders group project - COM4008 
Team members:
Dabi
Sulaiman
Tahir
Zohaib

import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Last Defender")

x = 250
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            screen.fill((0, 0, 0))


pygame.quit()
