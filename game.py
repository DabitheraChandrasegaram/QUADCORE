import pygame
import random

# --------------------------
# SETUP
# --------------------------
pygame.init()

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Defender")

# Background
background = pygame.image.load("background1.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Enemy images & sizes
enemy_sml = pygame.transform.scale(pygame.image.load("enemy1.png").convert_alpha(), (40, 35))  # smallest
enemy_med = pygame.transform.scale(pygame.image.load("enemy2.png").convert_alpha(), (50, 45))  # medium
enemy_big = pygame.transform.scale(pygame.image.load("enemy3.png").convert_alpha(), (60, 55))   # BIGGEST

# Enemy movement settings
enemy_speed = 2
drop_amount = 25
direction = 1  # 1 = right, -1 = left

# List to hold all enemies
enemies = []

# --------------------------
# CREATE ENEMY ROWS
# --------------------------
# TOP: 2 rows — enemy3 (BIGGEST)
for col in range(10):
    enemies.append( [80 + col * 100, 70, enemy_big, 60] )
for col in range(10):
    enemies.append( [80 + col * 100, 135, enemy_big, 60] )

# MIDDLE: 2 rows — enemy2 (medium)
for col in range(10):
    enemies.append( [80 + col * 100, 210, enemy_med, 50] )
for col in range(10):
    enemies.append( [80 + col * 100, 270, enemy_med, 50] )

# BOTTOM: 1 row — enemy1 (smallest)
for col in range(10):
    enemies.append( [80 + col * 100, 340, enemy_sml, 40] )

# --------------------------
# MAIN GAME LOOP
# --------------------------
running = True
clock = pygame.time.Clock()

while running:
    # Close window check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move enemies left/right
    hit_edge = False
    for enemy in enemies:
        enemy[0] = enemy[0] + enemy_speed * direction
        if enemy[0] <= 0 or enemy[0] + enemy[3] >= SCREEN_WIDTH:
            hit_edge = True

    # Drop all enemies down & flip direction together
    if hit_edge == True:
        direction = direction * -1
        for enemy in enemies:
            enemy[1] = enemy[1] + drop_amount

    # Draw everything
    screen.blit(background, (0, 0))
    for enemy in enemies:
        screen.blit(enemy[2], (enemy[0], enemy[1]))

    # Update screen
    pygame.display.flip()
    clock.tick(60)

# End game
pygame.quit()