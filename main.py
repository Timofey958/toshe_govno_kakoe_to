import pygame
from random import randint

from src.config import WIN_SIZE, SPAWN_STEP, WIN_WIDTH
from src.sprite import Sprite
from src.player import Player

def main():
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()
    clock = pygame.Clock()
    platform_image = pygame.image.load("assets/platform.png")
    platforms = [Sprite([200, 500], platform_image)]

    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Sprite([randint(0, WIN_WIDTH), y], platform_image))

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

        player.update(platforms)

        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface)
        player.render(surface)

        window.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()