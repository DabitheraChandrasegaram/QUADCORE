import pygame
import random #aliens fire at random times

# INITIALIZE PYGAME 
pygame.init()



# Setting background and screen size
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



    pygame.display.flip()  # update display 
    pygame.quit()





#Load images for alien

enemy1_img = pygame.image.load("enemy1.png").convert_alpha()  # convert_alpha keeps pictures transparent
enemy2_img = pygame.image.load("enemy2.png").convert_alpha()
enemy3_img = pygame.image.load("enemy3.png").convert_alpha()

#The Enemy class:

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, enemy_type):
        super().__init__()  # Required - sets up the sprite

        if enemy_type == 1:
            self.image = pygame.transform.scale(enemy1_img, (45, 35))
            self.points = 10  # points when shot down
        elif enemy_type == 2:
            self.image = pygame.transform.scale(enemy2_img, (45, 50))
            self.points = 20
        elif enemy_type == 3:
            self.image = pygame.transform.scale(enemy3_img, (45, 75))
            self.points = 30

        self.rect = self.image.get_rect() #where it is and how big it is
        self.rect.x = x_position
        self.rect.y = y_position

#Grid settings and building the grid (one type per row):

enemies = pygame.sprite.Group()

start_x = 60
start_y = 20
gap_x = 90   # space between enemies
gap_y = 85   # space between rows
rows = 3
cols = 10


def build_enemies():
    """Top row = type 3 (worth most), middle = type 2, bottom = type 1."""
    for row in range(rows):
        for col in range(cols):
            x = start_x + (col * gap_x)
            y = start_y + (row * gap_y)
            enemy_type = 3 - row          # row 0 -> 3, row 1 -> 2, row 2 -> 1
            enemies.add(Enemy(x, y, enemy_type))


build_enemies()

enemy_direction = 1    # 1 = move right, -1 = move left
enemy_speed = 2



#Enemy movement + edge bounce (inside the game loop):
# Move every enemy in the current direction
    for enemy in enemies:
            enemy.rect.x += enemy_speed * enemy_direction

# Bounce at screen edges: flip direction and drop down
        change_direction = False
    for enemy in enemies:
            if enemy.rect.right >= 1000 or enemy.rect.left <= 0:
                change_direction = True
        if change_direction:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.rect.y += 15



# Random enemy firing (inside the loop):

enemy_bullets = []
enemy_bullet_speed = 6
enemy_fire_chance = 40   # lower = fire more often

        if len(enemies) > 0 and random.randint(1, enemy_fire_chance) == 1:
            shooter = random.choice(enemies.sprites())
            enemy_bullets.append([shooter.rect.centerx, shooter.rect.bottom])

        # Move enemy bullets down, remove off-screen ones
        for bullet in enemy_bullets[:]:
            bullet[1] += enemy_bullet_speed
            if bullet[1] > 710:
                enemy_bullets.remove(bullet)

#Wave respawn + speed-up (inside the loop):

        if kills >= row_size:
            kills -= row_size
            wave_number += 1
            new_type = (wave_number - 1) % 3 + 1   # 1, 2, 3, 1, 2, 3...
            for col in range(cols):
                x = start_x + (col * gap_x)
                enemies.add(Enemy(x, start_y, new_type))
            enemy_speed += 0.2
#Drawing (inside the loop):


enemies.draw(screen)
