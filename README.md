# QUADCORE
CW1 - Space Invaders group project - COM4008 
Team members:
Dabi
Sulaiman
Tahir
Zohaib
import pygame  # loads game tools
import random  # random starspygame.init()

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Last Defender")

# Colours
black = (5, 5, 15)
sun_core = (255, 230, 120)
sun_mid = (255, 180, 60)
sun_outer = (255, 120, 30)
blue = (100, 160, 255)
dark_blue = (60, 90, 150)
purple = (170, 110, 220)
dark_purple = (110, 70, 160)
meteor_col = (200, 160, 120)

# Load images ONCE at the start
jet = pygame.image.load("jet.png").convert_alpha()
jet = pygame.transform.scale(jet, (100, 100))

enemy1_img = pygame.image.load("enemy1.png").convert_alpha() #convert alpha keeps the transparent background
enemy1_img = pygame.transform.scale(enemy1_img, (90, 52)) #resize the image 

enemy2_img = pygame.image.load("enemy2.png").convert_alpha() 
enemy2_img = pygame.transform.scale(enemy2_img, (90, 100))

enemy3_img = pygame.image.load("enemy3.png").convert_alpha()
enemy3_img = pygame.transform.scale(enemy3_img, (90, 150))

# Enemy class: Enemy 1, 2, 3 using your loaded images

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, enemy_type):
        super().__init__()  # Required — sets up the sprite, sprite is something that moves on the screen, like a character or object
        
        # Use your pre-loaded images (enemy1_img, enemy2_img, enemy3_img)
        if enemy_type == 1:
            self.image = enemy1_img
            self.image = pygame.transform.scale(self.image, (45, 35))  # Resize the image to 90x52 pixels
            self.points = 10 #points when shot down
        elif enemy_type == 2:
            self.image = enemy2_img
            self.image = pygame.transform.scale(self.image, (45, 50))  # Resize the image to 90x100 pixels
            self.points = 20
        elif enemy_type == 3:
            self.image = enemy3_img  #BIGGEST — bottom row
            self.image = pygame.transform.scale(self.image, (45, 75))  # Resize the image to 90x150 pixels
            self.points = 30
        
        # Set position and collision box
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

enemies = pygame.sprite.Group()

# Starting position of enemy 1
start_x = 55
start_y = 20
gap_x = 45  # space between enemies 
gap_y = 45  # space between rows down
rows = 2
cols = 20

for row in range(rows):
    for col in range(cols):
        x = start_x + (col * gap_x)
        y = start_y + (row * gap_y)

        enemy_type =  1  
        
        new_enemy = Enemy(x, y, enemy_type)
        enemies.add(new_enemy)

# Enemy movement settings
enemy_direction = 1    # 1 = move right, -1 = move left
enemy_speed = 2        # How fast they move — bigger = faste

# Player position and speed
jet_x = 450
jet_y = 600
jet_speed = 6

# Stars created ONCE - x, y, size, brightness
stars = []
for _ in range(150):
    x = random.randint(0, 1000)
    y = random.randint(0, 700)
    size = random.randint(1, 2)
    brightness = random.randint(100, 255)
    stars.append([x, y, size, brightness])

# Meteor - position and speed
meteor = {"x": -50, "y": 100, "speed_x": 4, "speed_y": 2}


def draw_glow(surface, colour, pos, radius):
    """Soft neon glow - layered transparent circles."""
    glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    for i in range(radius, 0, -2):
        alpha = int(80 * (1 - i / radius))
        pygame.draw.circle(glow, (*colour, alpha),
                           (radius * 2, radius * 2), radius + i)
    surface.blit(glow, (pos[0] - radius * 2, pos[1] - radius * 2))


def draw_sun():
    """Realistic sun - big glow plus layered colour circles."""
    draw_glow(screen, sun_outer, (850, 120), 90)
    pygame.draw.circle(screen, sun_outer, (850, 120), 60)
    pygame.draw.circle(screen, sun_mid, (850, 120), 48)
    pygame.draw.circle(screen, sun_core, (850, 120), 34)


def draw_meteor():
    """Meteor that flies across the screen with a fading trail."""
    x, y = int(meteor["x"]), int(meteor["y"])
    for i in range(1, 6):
        trail_x = x - i * meteor["speed_x"] * 2
        trail_y = y - i * meteor["speed_y"] * 2
        alpha_col = (255 - i * 40, 200 - i * 30, 100)
        pygame.draw.circle(screen, alpha_col, (trail_x, trail_y), 6 - i)
    draw_glow(screen, (255, 200, 120), (x, y), 8)
    pygame.draw.circle(screen, meteor_col, (x, y), 6)

    # Move it; when off screen, restart from a random left position
    meteor["x"] += meteor["speed_x"]
    meteor["y"] += meteor["speed_y"]
    if meteor["x"] > 1050 or meteor["y"] > 750:
        meteor["x"] = random.randint(-100, -30)
        meteor["y"] = random.randint(0, 200)


def draw_background():
    screen.fill(black)

    # Twinkling stars
    for star in stars:
        x, y, size, brightness = star
        brightness += random.randint(-20, 20)
        brightness = max(80, min(255, brightness))
        star[3] = brightness
        colour = (brightness, brightness, brightness)
        if brightness > 220:
            draw_glow(screen, (200, 200, 255), (x, y), 4)
        pygame.draw.circle(screen, colour, (x, y), size)

    draw_sun()

    # Planet 1 - blue with ring
    draw_glow(screen, blue, (300, 90), 45)
    pygame.draw.circle(screen, blue, (300, 90), 35)
    pygame.draw.ellipse(screen, dark_blue, (245, 80, 110, 20), 3)

    # Planet 2 - purple planet
    draw_glow(screen, purple, (480, 150), 35)
    pygame.draw.circle(screen, purple, (480, 150), 28)
    pygame.draw.circle(screen, dark_purple, (470, 140), 8)
    pygame.draw.circle(screen, dark_purple, (490, 160), 5)

    draw_meteor()


clock = pygame.time.Clock()
running = True
enemy_direction = 1  # 1 = move right, -1 = move left
enemy_speed = 2      # How fast they move — bigger = faster

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement - arrow keys (held down)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jet_x -= jet_speed
    if keys[pygame.K_RIGHT]:
        jet_x += jet_speed

    # Keep the jet inside the screen
    jet_x = max(0, min(1000 - 100, jet_x))

    draw_background()
    enemies.draw(screen)  # Draw all enemies in the group

      # Move every enemy in the current direction
    for enemy in enemies:
        enemy.rect.x += enemy_speed * enemy_direction #x position changes by speed * direction (1 or -1)

    # Check if enemies hit the LEFT or RIGHT edge — bounce them back
    change_direction = False

    for enemy in enemies:
        # If any enemy hits the RIGHT edge of the screen
        if enemy.rect.right >= 1000:   # 1000 = your screen width
            change_direction = True
        # checks if enemy hits the LEFT edge of the screen
        elif enemy.rect.left <= 0:
            change_direction = True

    # If we need to bounce — flip direction AND move all enemies down a bit
    if change_direction:
        enemy_direction *= -1   # Reverse: right → left, left → right
        for enemy in enemies:
            enemy.rect.y += 15    # Drop down slightly each time they hit the edge

    # Draw enemies and player
    enemies.draw(screen)
    screen.blit(jet, (jet_x, jet_y))


    # Player jet - drawn at its current position
    screen.blit(jet, (jet_x, jet_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
