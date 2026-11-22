import pygame
from random import randint

from src.config import *
from src.sprite import Sprite
from src.player import Player
from src.platforms import *
from src.bullet import Bullet
from src.monster import Monster

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

    bullet_image = pygame.image.load("assets/bullet.png")
    bullet_image = pygame.transform.scale(bullet_image, (10, 10))
    bullets = []

    monster_image = pygame.image.load("assets/player.png")

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
    spawn_platform_y = 0
    monster = None
    while running:
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b = Bullet(player.rect.midtop, bullet_image, 10)
                bullets.append(b)
            elif event.type == DESTROY_PLATFORM:
                platforms.remove(event.platform)
            elif (event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and button.rect.collidepoint(pygame.mouse.get_pos())
                    or pressed_keys[pygame.K_RETURN]
                    and lose):
                spawn_platform_y = 0
                player.rect.center = [200, 450]
                platforms = [Platform([200, 500], platform_image)]
                for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
                    platforms.append(Platform([randint(0, WIN_WIDTH), y], platform_image))  
                offset_y = 0
                lose = False

        if not lose:
            player.update(platforms)
            if monster != None:
                monster.update()
                if monster.rect.top - offset_y >= WIN_HEIGHT:
                    monster = None
                elif monster.rect.colliderect(player.rect):
                    monster = None
                    lose = True
            for platform in platforms:
                platform.update()
            if player.rect.top - offset_y >= WIN_HEIGHT:
                lose = True
                fall_sound.play()
            for bullet in bullets:
                bullet.update()
                if bullet.rect.bottom - offset_y <= 0:
                    bullets.remove(bullet)
                elif monster != None and monster.rect.colliderect(bullet.rect):
                        monster = None
                        bullets.remove(bullet)
                
            if abs(offset_y) - spawn_platform_y >= SPAWN_STEP:
                spawn_platform_y = abs(offset_y)
                y = offset_y
                r = randint(1, 100)
                if r <= MOVING_PLATFORM_PERCENTAGE:
                    platform = MovingPlatform([randint(0, WIN_WIDTH), y], platform_image)
                elif r <= TRAP_PLATFORM_PERCENTAGE:
                    platform = TrapPlatform([randint(0, WIN_WIDTH), y], platform_image)
                elif r <= BATOOT_PLATFORM_PERCENTAGE:
                    platform = BatootPlatform([randint(0, WIN_WIDTH), y], platform_image)
                else:
                    platform = Platform([randint(0, WIN_WIDTH), y], platform_image)
                platforms.append(platform)

                if randint(1, 100) <= 10 and monster == None:
                    x = platform.rect.centerx
                    y = y - monster_image.width
                    monster = Monster([x, y], monster_image, randint(1, 3), 3.5)



            if player.rect.y - offset_y < WIN_HEIGHT / 3:
                offset_y = player.rect.y - WIN_HEIGHT / 3

        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface, -offset_y)
        player.render(surface, -offset_y)
        for bullet in bullets:
            bullet.render(surface, -offset_y)
        if monster != None:
            monster.render(surface, -offset_y)


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