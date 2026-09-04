import pygame
import random  # aliens fire at random times

# INITIALIZE PYGAME
pygame.init()

# Setting background and screen size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Defender")

# Load background picture
background = pygame.image.load("background1.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images for aliens
enemy1_img = pygame.image.load("enemy1.png").convert_alpha()  # convert_alpha keeps pictures transparent
enemy2_img = pygame.image.load("enemy2.png").convert_alpha()
enemy3_img = pygame.image.load("enemy3.png").convert_alpha()

# Load barrier images
barrier1_img = pygame.image.load("barrier1.png").convert_alpha()
barrier2_img = pygame.image.load("barrier2.png").convert_alpha()

# Load player jet (needed - your shooting code fires from the jet's position)
jet = pygame.image.load("jet.png").convert_alpha()
jet = pygame.transform.scale(jet, (100, 100))


# The Enemy class
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

        self.rect = self.image.get_rect()  # where it is and how big it is
        self.rect.x = x_position
        self.rect.y = y_position


# The Barrier class
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, img):
        super().__init__()
        self.health = 8
        self.image = pygame.transform.scale(img, (110, 65)).copy()
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def take_damage(self):
        self.health -= 1
        if self.health > 0:
            self.image.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_SUB)
        else:
            self.kill()


# Grid settings and building the grid (one type per row)
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

# Barriers
barriers = pygame.sprite.Group()
barrier_positions = [95, 345, 595, 845]
barrier_y = 480


def build_barriers():
    for i, bx in enumerate(barrier_positions):
        img = barrier1_img if i % 2 == 0 else barrier2_img
        barriers.add(Barrier(bx, barrier_y, img))


build_barriers()

enemy_direction = 1    # 1 = move right, -1 = move left
enemy_speed = 2

# Enemy bullets - each is [x, y]
enemy_bullets = []
enemy_bullet_speed = 6
enemy_fire_chance = 40   # lower = fire more often

# Player bullets - each bullet is [x, y]
bullets = []
bullet_speed = 10
bullet_colour = (0, 255, 200)   # neon cyan
enemy_bullet_colour = (255, 80, 80)   # red
shoot_cooldown = 0              # frames until we can shoot again

# Player (needed by the shooting and collision code)
jet_x = SCREEN_WIDTH // 2 - 50
jet_y = 600
jet_speed = 6
lives = 3
score = 0
respawn_timer = 0

# Wave system (needed by the wave respawn code)
kills = 0
row_size = 10
wave_number = 0

game_state = "playing"

clock = pygame.time.Clock()

# MAIN LOOP - needed to keep the game running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "playing":

        # Player movement (needed so the jet the bullets fire from can move)
        if keys[pygame.K_LEFT]:
            jet_x -= jet_speed
        if keys[pygame.K_RIGHT]:
            jet_x += jet_speed
        jet_x = max(0, min(SCREEN_WIDTH - 100, jet_x))

        # Slightly smaller than the 100px image = fairer hits
        jet_rect = pygame.Rect(jet_x + 15, jet_y + 15, 70, 70)

        # Shooting - hold or tap SPACE, cooldown allows continuous fire
        if shoot_cooldown > 0:
            shoot_cooldown -= 1
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullets.append([jet_x + 50, jet_y])   # spawns at top-middle of the jet
            shoot_cooldown = 10   # smaller = faster fire rate

        # Enemy movement + edge bounce
        # Move every enemy in the current direction
        for enemy in enemies:
            enemy.rect.x += enemy_speed * enemy_direction

        # Bounce at screen edges: flip direction and drop down
        change_direction = False
        for enemy in enemies:
            if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                change_direction = True
        if change_direction:
            enemy_direction *= -1
            for enemy in enemies:
                enemy.rect.y += 15

        # Random enemy firing - small chance each frame that one enemy shoots
        if len(enemies) > 0 and random.randint(1, enemy_fire_chance) == 1:
            shooter = random.choice(enemies.sprites())   # pick a random enemy
            enemy_bullets.append([shooter.rect.centerx, shooter.rect.bottom])

        # Move player bullets up, remove off-screen ones
        for bullet in bullets[:]:            # [:] = copy, safe to remove while looping
            bullet[1] -= bullet_speed        # minus = upwards
            if bullet[1] < -10:
                bullets.remove(bullet)

        # Move enemy bullets down, remove off-screen ones
        for bullet in enemy_bullets[:]:
            bullet[1] += enemy_bullet_speed  # plus = downwards
            if bullet[1] > SCREEN_HEIGHT + 10:
                enemy_bullets.remove(bullet)

        # Player bullets vs enemies
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
            hit_list = [e for e in enemies if e.rect.colliderect(bullet_rect)]
            if hit_list:
                enemy_hit = hit_list[0]
                score += enemy_hit.points     # each type worth different points
                kills += 1                    # counts towards the next wave
                enemies.remove(enemy_hit)     # destroy the enemy
                bullets.remove(bullet)        # bullet is used up

        # Enemy bullets vs player (with lives + respawn)
        if respawn_timer > 0:
            respawn_timer -= 1     # invincible while respawning
        else:
            for bullet in enemy_bullets[:]:
                bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
                if jet_rect.colliderect(bullet_rect):
                    enemy_bullets.remove(bullet)
                    lives -= 1
                    respawn_timer = 60          # 2 seconds at 30 FPS
                    jet_x = SCREEN_WIDTH // 2 - 50   # respawn in the middle
                    if lives <= 0:
                        game_state = "game_over"
                    break

        # COLLISION 3: player bullets vs barriers
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
            hit_barriers = [b for b in barriers if b.rect.colliderect(bullet_rect)]
            if hit_barriers:
                hit_barriers[0].take_damage()
                bullets.remove(bullet)

        # COLLISION 4: enemy bullets vs barriers
        for bullet in enemy_bullets[:]:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
            hit_barriers = [b for b in barriers if b.rect.colliderect(bullet_rect)]
            if hit_barriers:
                hit_barriers[0].take_damage()
                enemy_bullets.remove(bullet)

        # Wave respawn + speed-up
        if kills >= row_size:
            kills -= row_size
            wave_number += 1
            new_type = (wave_number - 1) % 3 + 1   # 1, 2, 3, 1, 2, 3...
            for col in range(cols):
                x = start_x + (col * gap_x)
                enemies.add(Enemy(x, start_y, new_type))
            enemy_speed += 0.2

    # Drawing
    screen.blit(background, (0, 0))  # draw background first
    enemies.draw(screen)
    barriers.draw(screen)

    for bullet in bullets:
        pygame.draw.rect(screen, bullet_colour, (bullet[0] - 2, bullet[1], 4, 12))

    for bullet in enemy_bullets:
        pygame.draw.rect(screen, enemy_bullet_colour, (bullet[0] - 2, bullet[1], 4, 12))

    # Flash the jet while respawning (invincible)
    if respawn_timer == 0 or respawn_timer % 10 < 5:
        screen.blit(jet, (jet_x, jet_y))

    pygame.display.flip()  # update display
    clock.tick(60)

pygame.quit()
