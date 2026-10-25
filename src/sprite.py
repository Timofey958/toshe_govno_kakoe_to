import pygame

class Sprite:
    def __init__(self, center: list[float], image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_frect(center=center)

    def render(self, surface):
        surface.blit(self.image, self.rect)