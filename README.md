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
    """Realistic sun - big glow plus layered colour circles, no craters."""
    draw_glow(screen, sun_outer, (850, 120), 90)   # huge outer glow
    pygame.draw.circle(screen, sun_outer, (850, 120), 60)
    pygame.draw.circle(screen, sun_mid, (850, 120), 48)
    pygame.draw.circle(screen, sun_core, (850, 120), 34)


def draw_meteor():
    """Meteor that flies across the screen with a fading trail."""
    x, y = int(meteor["x"]), int(meteor["y"])
    # Trail - small faded circles behind the meteor
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

    # Planet 1 - blue with ring (top left)
    draw_glow(screen, blue, (150, 80), 45)
    pygame.draw.circle(screen, blue, (150, 80), 35)
    pygame.draw.ellipse(screen, dark_blue, (95, 70, 110, 20), 3)

    # Planet 2 - purple planet (middle top)
    draw_glow(screen, purple, (480, 150), 35)
    pygame.draw.circle(screen, purple, (480, 150), 28)
    pygame.draw.circle(screen, dark_purple, (470, 140), 8)   # shading
    pygame.draw.circle(screen, dark_purple, (490, 160), 5)

    draw_meteor()

    #space ship
    jet=pygame.image.load("jet.png") #load image
    jet=pygame.transform.scale(jet,(100,100)) #change size
    screen.blit(jet, (450, 600)) #position of jet



clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
