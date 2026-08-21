# QUADCORE
CW1 - Space Invaders group project - COM4008 
Team members:
Dabi
Sulaiman
Tahir
Zohaib

import pygame #loads game tools
import random #random stars

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Last Defender")

#Colours needed for the game
white = (255, 255, 255)
black = (0, 0, 0)

#background setting, black background with stars
for _ in range(100):
    star1 = random.randint(0, 1000)
    star2 = random.randint(0, 700)
    star_size = random.randint(1, 2) #tiny stars
    pygame.draw.circle(screen, white, (star1, star2), star_size)

clock = pygame.time.Clock()
running = True

#fill the screen with black color
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            screen.fill((0, 0, 0))
#creatinfg a list of stars with random positions           
    for star in range(100):
        star1 = random.randint(0, 1000)
        star2 = random.randint(0, 700)
        pygame.draw.circle(screen, white, (star1, star2), random.randint(1, 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)


    




pygame.quit()
