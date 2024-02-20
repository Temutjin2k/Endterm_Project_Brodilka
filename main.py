import pygame
from Settings import *
from Platform import *
from Player import *
from Enemy import *
from Bullet import *
from Button import Button

pygame.init()
font.init()
mixer.init()


# Музыка и Звуки
mixer.music.load("Sounds/Ground_Theme.mp3")
mixer_music.set_volume(0.2)
mixer.music.play(-1)


# Шрифты
font_italic = font.SysFont('Futura', 40, False, True)
font_victory = font.SysFont('Futura', 60, True, False)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# CAMERA
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = - l + WIDTH / 2, - t + HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def camera_setup(level):
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    return Camera(camera_configure, total_level_width, total_level_height)



def reset_setting():
    entities.empty()
    platforms.clear()
    bullets.empty()
    enemies.empty()
    item_box_group.empty()


def draw_level(level):
    player = 0
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if y == 0:
                wall = Platform.Platform(x, y, platform_default)
                platforms.append(wall)
            if x < PLATFORM_WIDTH:
                wall = Platform.Platform(x - PLATFORM_WIDTH, y, platform_default)
                platforms.append(wall)
            if x >= (PLATFORM_WIDTH * len(level[0])) - PLATFORM_WIDTH:
                wall = Platform.Platform(x + PLATFORM_WIDTH, y, platform_default)
                platforms.append(wall)
            if col == "-":
                block = Platform.Platform(x, y, platform_default)
                entities.add(block)
                platforms.append(block)
            if col == '1':
                block = Platform.Platform(x, y, platform_black)
                entities.add(block)
                platforms.append(block)
            if col == '2':
                block = Platform.Platform(x, y, platform_red)
                entities.add(block)
                platforms.append(block)
            if col == '3':
                block = Platform.Platform(x, y, platform_grey)
                entities.add(block)
                platforms.append(block)
            if col == "E":
                enemy = Enemy(x, y - 18, -1)
                entities.add(enemy)
                enemies.add(enemy)
            if col == "P":
                player = Player(x, y)
                entities.add(player)
            if col == "a":  # ammo box
                ammo_box = Item_box('Ammo', x, y)
                item_box_group.add(ammo_box)
            if col == "h":  # health box
                health_box = Item_box('Health', x, y)
                item_box_group.add(health_box)
            if col == "F":
                finish = Item_box('Finish', x, y)
                item_box_group.add(finish)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    return player


current_level = 0
hero = draw_level(levels[current_level])
hero_hp_left = hero.health
hero_ammo_left = hero.ammo

start_game = False  #  Определяет начало уровня

# Buttons
start_button = Button(WIDTH // 2 - 130, HEIGHT // 2 - 100, start_btn_image, 1)
exit_button = Button(WIDTH // 2 - 110, HEIGHT // 2 + 100, exit_btn_image, 1)
restart_button = Button(WIDTH // 2 + 50, HEIGHT // 2 + 100, restart_btn_image, 1)

exit_button_win = Button(WIDTH // 2 + 70, HEIGHT // 2 + 100, exit_btn_image, 1)
continue_button = Button(WIDTH // 2, HEIGHT // 2 + 100, continue_btn_image, 1)
menu_button = Button(WIDTH // 2 - 380, HEIGHT // 2 + 100, menu_btn_image, 1)

clock = time.Clock()
FPS = 60
running = True

while running:
    clock.tick(FPS)

    if not start_game:
        #  Начальная менюшка
        #screen.fill((137, 0, 171))
        screen.blit(bg_start, (0, 0))
        draw_text("Endterm Project Brodilka", font_italic, (255, 255, 255), 10, 10)
        draw_text("Created by Koszhanov Temutjin", font_italic, (255, 255, 255), 10, 40)
        draw_text("Group: SE-2334", font_italic, (255, 255, 255), 10, 70)
        draw_text(f'Version: {VERSION}', font_italic, (255, 255, 255), WIDTH - 250, HEIGHT - 50)

        if start_button.draw(screen):  # нажатие на кнопку старт
            start_game = True
            camera = camera_setup(levels[current_level])  # Камера на игрока
        if exit_button.draw(screen):  # нажатие на кнопку exit
            running = False

    else:

        screen.blit(bg, (0, 0))

        camera.update(hero)  # Камера на игрока

        hero.update(platforms)
        enemies.update(hero)
        bullets.update(platforms, hero, entities, bullets)
        item_box_group.update(hero, enemies)


        for item in item_box_group:
            screen.blit(item.image, camera.apply(item))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for b in bullets:
            screen.blit(b.image, camera.apply(b))


        # Cтатистика игрока
        draw_text(f'Health: {hero.health}', font_italic, (255, 0, 0), 10, 10)
        draw_text(f'Ammo: {hero.ammo}/{hero.max_ammo}', font_italic, (0, 255, 0), 10, 35)
        draw_text(f'Enemy killed: {hero.kills} / {len(enemies)}', font_italic, (255, 255, 255), 10, 60)
        killed_enemies = 0
        for enemy in enemies:
            if enemy.alive:
                if enemy.up:
                    enemy.update_action(2)
                elif enemy.right or enemy.left:
                    enemy.update_action(1)
                else:
                    enemy.update_action(0)
            else:
                killed_enemies += 1
        if killed_enemies > hero.kills:
            hero.kills = killed_enemies

        if hero.alive:
            if hero.up:
                hero.update_action(2)
            elif hero.right or hero.left:
                hero.update_action(1)
            else:
                hero.update_action(0)

            if hero.shooting:
                hero.shoot(bullets)

            if hero.kills - 1 == len(enemies):  # Убил всех и добрался до таблички
                hero.left = hero.right = hero.up = False
                hero.can_move = False

                if current_level < len(levels) - 1:  # Если это не Последний уровень то переходим на следущий
                    screen.blit(overlay_surface, (0, 0))
                    # screen.blit(level_completed_btn_image, (WIDTH // 2 - 200, 130))
                    screen.blit(lvl_complete_image, (WIDTH // 2 - 300, 60))
                    if continue_button.draw(screen):
                        current_level += 1
                        reset_setting()
                        hero_hp_left = hero.health
                        hero_ammo_left = hero.ammo

                        hero = draw_level(levels[current_level])
                        camera = camera_setup(levels[current_level])

                        hero.health = hero_hp_left
                        hero.ammo = hero_ammo_left

                    if menu_button.draw(screen):
                        start_game = False
                        reset_setting()
                        hero = draw_level(levels[current_level])
                        camera = camera_setup(levels[current_level])
                else:  # Прошел все уровни (Победа)
                    screen.blit(overlay_surface, (0, 0))
                    screen.blit(victory_btn_image, (WIDTH // 2 - 200, 60))
                    if restart_button.draw(screen):
                        current_level = 0
                        reset_setting()
                        hero = draw_level(levels[current_level])
                        camera = camera_setup(levels[current_level])

                    if menu_button.draw(screen):
                        start_game = False
                        reset_setting()
                        hero = draw_level(levels[current_level])
                        camera = camera_setup(levels[current_level])

        else:  # Умер во время прохождения
            screen.blit(overlay_surface, (0, 0))
            if restart_button.draw(screen):
                reset_setting()
                hero = draw_level(levels[current_level])
                camera = camera_setup(levels[current_level])
                hero.health = hero_hp_left
                hero.ammo = hero_ammo_left
            if menu_button.draw(screen):
                start_game = False
                reset_setting()
                hero = draw_level(levels[current_level])
                camera = camera_setup(levels[current_level])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_UP:
            jump_sound.play(0)
            hero.up = True
        if event.type == KEYDOWN and event.key == K_LEFT:
            hero.left = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            hero.right = True
        if event.type == KEYDOWN and event.key == K_SPACE:
            hero.shooting = True

        if event.type == KEYUP and event.key == K_UP:
            hero.up = False
        if event.type == KEYUP and event.key == K_RIGHT:
            hero.right = False
        if event.type == KEYUP and event.key == K_LEFT:
            hero.left = False
        if event.type == KEYUP and event.key == K_SPACE:
            hero.shooting = False
    display.update()

quit()
