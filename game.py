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


# === Alien movement settings — put these after your Enemy class ===
alien_speed = 1.0
move_down_amount = 20
rows = 4
cols = 10
total_aliens = rows * cols

# === Create the enemy group and spawn enemies — put this BEFORE line 41 ===
enemy_group = pygame.sprite.Group()

start_x = 60
start_y = 50
gap_x = 60
gap_y = 50

for row in range(rows):
    if row == 0 or row == 1:
        enemy_type = 1
    elif row == 2:
        enemy_type = 2
    elif row == 3:
        enemy_type = 3
    
    for col in range(cols):
        x = start_x + (col * gap_x)
        y = start_y + (row * gap_y)
        new_enemy = Enemy(x, y, enemy_type)
        enemy_group.add(new_enemy)

# === THE MISSING FUNCTION — put this BEFORE line 41 ===
def update_enemies():
    global alien_speed
    edge_hit = False
    
    # Move all enemies sideways
    for enemy in enemy_group:
        enemy.rect.x += enemy.direction * alien_speed
        
        # Check if any enemy hits screen edge
        if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
            edge_hit = True
    
    # If edge hit — reverse direction and move down
    if edge_hit:
        for enemy in enemy_group:
            enemy.rect.y += move_down_amount
            enemy.direction *= -1
    
    # Speed up as enemies are destroyed
    remaining = len(enemy_group)
    alien_speed = 1.0 + ((total_aliens - remaining) / total_aliens) * 2.0
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
 