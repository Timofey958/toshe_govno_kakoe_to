import pygame

from src.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, center: list[float], image: pygame.Surface, speed: float):
        super().__init__(center, image)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed