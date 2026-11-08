from random import randint

from src.sprite import Sprite
from src.config import *
import pygame

class Platform(Sprite):
    def on_collide(self, player: Sprite):
        pass
    def update(self):
        pass

class MovingPlatform(Platform):
    def __init__(self, center: list[float], image: pygame.Surface):
        super().__init__(center, image)
        self.speed = randint(PLATFORM_SPEED_MIN, PLATFORM_SPEED_MAX)
    def update(self):
        if self.rect.right >= WIN_WIDTH:
            self.speed = -abs(self.speed)
        if self.rect.left <= 0:
            self.speed = abs(self.speed)
            
        self.rect.x += self.speed