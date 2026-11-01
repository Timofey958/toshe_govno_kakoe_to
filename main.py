import pygame
from random import randint

from src.config import *
from src.sprite import Sprite
from src.player import Player

def main():
    pygame.init()
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()
    clock = pygame.Clock()
    font = pygame.Font("assets/pixel.ttf", 32)
    platform_image = pygame.image.load("assets/platform.png")
    platforms = [Sprite([200, 500], platform_image)]

    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Sprite([randint(0, WIN_WIDTH), y], platform_image))

    background_image = pygame.image.load("assets/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    player_image = pygame.image.load("assets/player.png")
    window.set_icon(player_image)
    player = Player([200, 450], player_image, PLAYER_SPEED)

    running = True
    lose = False
    offset_y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

        if not lose:
            player.update(platforms)
            if player.rect.top - offset_y >= WIN_HEIGHT:
                lose = True
            if platforms[-1].rect.y - offset_y >= SPAWN_STEP:
                platforms.pop(0)
                y = platforms[-1].rect.y - SPAWN_STEP
                platforms.append(Sprite([randint(0, WIN_WIDTH), y], platform_image))

            if player.rect.y - offset_y < WIN_HEIGHT / 3:
                offset_y = player.rect.y - WIN_HEIGHT / 3

        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface, -offset_y)
        player.render(surface, -offset_y)

        text = str(round(-offset_y/150))
        img = font.render(text, True, "black")
        rect = img.get_rect(midtop = [WIN_WIDTH / 2, 10])
        surface.blit(img, rect)

        if lose:
            img = font.render("Вы проиграли!\nВаш Результат: " + text, True, "black")
            rect = img.get_rect(midtop = [WIN_WIDTH / 2, WIN_HEIGHT / 3])
            surface.blit(img, rect)

        window.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()