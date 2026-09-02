# QUADCORE
CW1 - Space Invaders group project - COM4008 
Team members:
Dabi
Sulaiman
Tahir
Zohaib
import pygame  # loads game tools
import random  # random stars

pygame.init()

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

enemy1_img = pygame.image.load("enemy1.png").convert_alpha()
enemy2_img = pygame.image.load("enemy2.png").convert_alpha()
enemy3_img = pygame.image.load("enemy3.png").convert_alpha()


# Enemy class: Enemy 1, 2, 3
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, enemy_type):
        super().__init__()

        # Pick image, size and points based on enemy type
        if enemy_type == 1:
            self.image = pygame.transform.scale(enemy1_img, (45, 35))
            self.points = 10

        elif enemy_type == 2:
            self.image = pygame.transform.scale(enemy2_img, (45, 50))
            self.points = 20

        elif enemy_type == 3:
            self.image = pygame.transform.scale(enemy3_img, (45, 75))
            self.points = 30

        # Set position and collision box
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position


enemies = pygame.sprite.Group()

# Enemy grid settings
start_x = 55
start_y = 20
gap_x = 45
gap_y = 45
rows = 2
cols = 20

for row in range(rows):
    for col in range(cols):
        x = start_x + (col * gap_x)
        y = start_y + (row * gap_y)

        enemy_type = 1

        new_enemy = Enemy(x, y, enemy_type)
        enemies.add(new_enemy)


# Enemy movement settings
enemy_direction = 1
enemy_speed = 2


# Player position and speed
jet_x = 450
jet_y = 600
jet_speed = 6


# ------------------------------------------------
# Bullet class
# ------------------------------------------------

class Bullet:
    def __init__(self, x, y):

        # Create the bullet
        self.rect = pygame.Rect(x, y, 5, 15)

        # Bullet speed
        self.speed = 8

    def update(self):

        # Move bullet upwards
        self.rect.y -= self.speed


# Store all bullets
bullets = []


# Stars created ONCE
stars = []

for _ in range(150):
    x = random.randint(0, 1000)
    y = random.randint(0, 700)
    size = random.randint(1, 2)
    brightness = random.randint(100, 255)

    stars.append([x, y, size, brightness])


# Meteor - position and speed
meteor = {
    "x": -50,
    "y": 100,
    "speed_x": 4,
    "speed_y": 2
}


def draw_glow(surface, colour, pos, radius):
    """Soft neon glow - layered transparent circles."""

    glow = pygame.Surface(
        (radius * 4, radius * 4),
        pygame.SRCALPHA
    )

    for i in range(radius, 0, -2):

        alpha = int(80 * (1 - i / radius))

        pygame.draw.circle(
            glow,
            (*colour, alpha),
            (radius * 2, radius * 2),
            radius + i
        )

    surface.blit(
        glow,
        (pos[0] - radius * 2,
         pos[1] - radius * 2)
    )


def draw_sun():
    """Realistic sun - big glow plus layered colour circles."""

    draw_glow(
        screen,
        sun_outer,
        (850, 120),
        90
    )

    pygame.draw.circle(
        screen,
        sun_outer,
        (850, 120),
        60
    )

    pygame.draw.circle(
        screen,
        sun_mid,
        (850, 120),
        48
    )

    pygame.draw.circle(
        screen,
        sun_core,
        (850, 120),
        34
    )


def draw_meteor():
    """Meteor that flies across the screen with a fading trail."""

    x = int(meteor["x"])
    y = int(meteor["y"])

    for i in range(1, 6):

        trail_x = x - i * meteor["speed_x"] * 2
        trail_y = y - i * meteor["speed_y"] * 2

        alpha_col = (
            255 - i * 40,
            200 - i * 30,
            100
        )

        pygame.draw.circle(
            screen,
            alpha_col,
            (trail_x, trail_y),
            6 - i
        )

    draw_glow(
        screen,
        (255, 200, 120),
        (x, y),
        8
    )

    pygame.draw.circle(
        screen,
        meteor_col,
        (x, y),
        6
    )

    # Move meteor
    meteor["x"] += meteor["speed_x"]
    meteor["y"] += meteor["speed_y"]

    # Restart meteor when off screen
    if meteor["x"] > 1050 or meteor["y"] > 750:

        meteor["x"] = random.randint(-100, -30)
        meteor["y"] = random.randint(0, 200)


def draw_background():

    screen.fill(black)

    # Twinkling stars
    for star in stars:

        x, y, size, brightness = star

        brightness += random.randint(-20, 20)

        brightness = max(
            80,
            min(255, brightness)
        )

        star[3] = brightness

        colour = (
            brightness,
            brightness,
            brightness
        )

        if brightness > 220:

            draw_glow(
                screen,
                (200, 200, 255),
                (x, y),
                4
            )

        pygame.draw.circle(
            screen,
            colour,
            (x, y),
            size
        )

    draw_sun()

    # Planet 1 - blue with ring
    draw_glow(
        screen,
        blue,
        (300, 90),
        45
    )

    pygame.draw.circle(
        screen,
        blue,
        (300, 90),
        35
    )

    pygame.draw.ellipse(
        screen,
        dark_blue,
        (245, 80, 110, 20),
        3
    )

    # Planet 2 - purple planet
    draw_glow(
        screen,
        purple,
        (480, 150),
        35
    )

    pygame.draw.circle(
        screen,
        purple,
        (480, 150),
        28
    )

    pygame.draw.circle(
        screen,
        dark_purple,
        (470, 140),
        8
    )

    pygame.draw.circle(
        screen,
        dark_purple,
        (490, 160),
        5
    )

    draw_meteor()


# ------------------------------------------------
# Main game loop
# ------------------------------------------------

clock = pygame.time.Clock()
running = True

while running:

    # Check events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Fire bullet when Space is pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                bullet = Bullet(
                    jet_x + 48,
                    jet_y
                )

                bullets.append(bullet)


    # Player movement - arrow keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        jet_x -= jet_speed

    if keys[pygame.K_RIGHT]:
        jet_x += jet_speed


    # Keep the jet inside the screen
    jet_x = max(
        0,
        min(1000 - 100, jet_x)
    )


    # ------------------------------------------------
    # Move bullets
    # ------------------------------------------------

    for bullet in bullets:
        bullet.update()


    # Remove bullets that leave the screen
    bullets = [
        bullet for bullet in bullets
        if bullet.rect.bottom > 0
    ]


    # Move every enemy in the current direction
    for enemy in enemies:

        enemy.rect.x += (
            enemy_speed *
            enemy_direction
        )


    # Check if any enemy hit the LEFT or RIGHT edge
    change_direction = False

    for enemy in enemies:

        if (
            enemy.rect.right >= 1000
            or enemy.rect.left <= 0
        ):

            change_direction = True


    # Bounce: flip direction and move enemies down
    if change_direction:

        enemy_direction *= -1

        for enemy in enemies:
            enemy.rect.y += 15


    # ------------------------------------------------
    # Draw everything
    # ------------------------------------------------

    draw_background()

    enemies.draw(screen)

    # Draw bullets
    for bullet in bullets:

        pygame.draw.rect(
            screen,
            (255, 255, 100),
            bullet.rect
        )

    # Draw player
    screen.blit(
        jet,
        (jet_x, jet_y)
    )


    pygame.display.flip()

    clock.tick(30)


pygame.quit()



