barrier1_img = pygame.image.load("barrier1.png").convert_alpha()
barrier2_img = pygame.image.load("barrier2.png").convert_alpha()


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
            self.image.fill(
                (30, 30, 30),
                special_flags=pygame.BLEND_RGB_SUB
            )
        else:
            self.kill()


barriers = pygame.sprite.Group()
barrier_positions = [95, 345, 595, 845]
barrier_y = 480


def build_barriers():
    for i, bx in enumerate(barrier_positions):
        img = barrier1_img if i % 2 == 0 else barrier2_img
        barriers.add(Barrier(bx, barrier_y, img))


build_barriers()


# COLLISION 3: player bullets vs barriers
for bullet in bullets[:]:
    bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
    hit_barriers = [
        b for b in barriers
        if b.rect.colliderect(bullet_rect)
    ]
    if hit_barriers:
        hit_barriers[0].take_damage()
        bullets.remove(bullet)


# COLLISION 4: enemy bullets vs barriers
for bullet in enemy_bullets[:]:
    bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1], 4, 12)
    hit_barriers = [
        b for b in barriers
        if b.rect.colliderect(bullet_rect)
    ]
    if hit_barriers:
        hit_barriers[0].take_damage()
        enemy_bullets.remove(bullet)


barriers.draw(screen)


def reset_game():
    barriers.empty()
    build_barriers()