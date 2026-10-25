import pygame

from src.config import WIN_WIDTH, GRAVITY, JUMP_POWER
from src.sprite import Sprite

class Player(Sprite):
    def __init__(self, center: list[float], image: pygame.Surface, speed: float):
        super().__init__(center, image)
        # self.health = PLAYER_MAX_HEALTH

        self.orig_image = image.copy()
        self.speed = speed
        self.velocity_y = 0.35

    def update(self, platforms: list[Sprite]):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.image = self.orig_image.copy()
            self.rect.x -= self.speed
            if self.rect.right <= 0:
                self.rect.left = WIN_WIDTH
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.image = pygame.transform.flip(self.orig_image, True, False)
            self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH:
            self.rect.right = 0

        self.velocity_y = min(self.velocity_y + GRAVITY, 15)
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.colliderect(self.rect) and self.velocity_y > 0 and platform.rect.bottom >= self.rect.bottom:
                self.velocity_y = -JUMP_POWER
                self.rect.bottom = platform.rect.top

        