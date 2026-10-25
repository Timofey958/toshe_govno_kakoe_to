import pygame

from src.config import *
from src.sprite import Sprite
from src.player import Player

def main():
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()
    clock = pygame.Clock()
    platform_image = pygame.image.load("assets/platform.png")
    platform = Sprite([200, 500], platform_image)

    background_image = pygame.image.load("assets/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    player_image = pygame.image.load("assets/player.png")
    window.set_icon(player_image)
    player = Player([200, 450], player_image, 6)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

        player.update()

        surface.blit(background_image)
        platform.render(surface)
        player.render(surface)

        window.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()