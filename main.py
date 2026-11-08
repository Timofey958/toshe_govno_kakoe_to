import pygame
from random import randint

from src.config import *
from src.sprite import Sprite
from src.player import Player
from src.platforms import *

def main():
    pygame.init()
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()

    clock = pygame.Clock()

    font = pygame.Font("assets/pixel.ttf", 32)

    platform_image = pygame.image.load("assets/platform.png")

    platforms = [Platform([200, 500], platform_image)]

    button_image = pygame.image.load("assets/button_image.jpg")
    button_image = pygame.transform.scale(button_image, [WIN_WIDTH / 5 * 4, WIN_WIDTH / 5])
    img = font.render("Заного", True, "white")
    rect = img.get_rect(center=[button_image.width / 2, button_image.height / 2])
    button_image.blit(img, rect)

    x = WIN_WIDTH / 2
    y = WIN_HEIGHT / 3 * 2
    button = Platform([x, y], button_image)

    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Platform([randint(0, WIN_WIDTH), y], platform_image))

    background_image = pygame.image.load("assets/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    fall_sound = pygame.Sound("assets/fall.mp3")
    fall_sound.set_volume(0.1)
    jump_sound = pygame.Sound("assets/jump.wav")
    jump_sound.set_volume(0.1)

    player_image = pygame.image.load("assets/player.png")
    window.set_icon(player_image)
    player = Player([200, 450], player_image, PLAYER_SPEED, jump_sound)

    pygame.mixer_music.load("assets/background_music.mp3")
    pygame.mixer_music.set_volume(0.1)
    pygame.mixer_music.play(-1)

    running = True
    lose = False
    offset_y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and button.rect.collidepoint(pygame.mouse.get_pos())
                    and lose):
                player.rect.center = [200, 450]
                platforms = [Platform([200, 500], platform_image)]
                for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
                    platforms.append(Platform([randint(0, WIN_WIDTH), y], platform_image))
                offset_y = 0
                lose = False

        if not lose:
            player.update(platforms)
            for platform in platforms:
                platform.update()
            if player.rect.top - offset_y >= WIN_HEIGHT:
                lose = True
                fall_sound.play()
            if platforms[-1].rect.y - offset_y >= SPAWN_STEP:
                platforms.pop(0)
                y = platforms[-1].rect.y - SPAWN_STEP
                r = randint(1, 100)
                if r < 10:
                    platform = MovingPlatform([randint(0, WIN_WIDTH), y], platform_image)
                else:
                    platform = Platform([randint(0, WIN_WIDTH), y], platform_image)
                platforms.append(platform)



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

            button.render(surface, 0)

        window.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()