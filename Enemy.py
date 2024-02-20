from pygame import *

import Platform
from Bullet import Bullet
from Settings import bullets, platforms, total_level_height
from Player import Player
import os
import random


PLAYER_WIDTH = 35
PLAYER_HEIGHT = 50
JUMP_POWER = 10
GRAVITY = 0.4

class Enemy(Player):
    def __init__(self, x, y, facing):
        super().__init__(x, y)
        self.facing = facing
        self.up = False
        self.left = False
        self.right = False
        self.speed = 3
        self.move_delay = 0

        self.walk_area = Platform.PLATFORM_WIDTH * 2.5

        self.animation_list = []  # Двухмерный массив со всеми анимациямий
        animation_types = ['Stand', 'Walk', 'Jump', 'Death']

        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'images/{"Enemy"}/{animation}'))
            for i in range(num_of_frames):
                img = image.load(f'images/{"Enemy"}/{animation}/{i}.png')
                img = transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]

    def update(self, hero):
        self.check_alive()
        if self.alive:
            self.ai(hero)

            if self.up:
                if self.onGround:
                    self.currentSpeed_Y -= JUMP_POWER
            if self.left:
                self.currentSpeed_X = -self.speed  # Лево = x - n
                self.flip = True
                self.facing = -1
            if self.right:
                self.currentSpeed_X = self.speed  # Право = x + n
                self.flip = True
                self.facing = 1
            if self.onGround:
                self.up = False

            if not (self.left or self.right):  # стоим, когда нет указаний идти
                self.currentSpeed_X = 0

            if self.health > self.max_health:
                self.health = self.max_health

            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo

            if self.rect.x < self.startX - self.walk_area:
                self.rect.x += 1
                self.move_delay = 0
            elif self.rect.x > self.startX + self.walk_area:
                self.rect.x -= 1
                self.move_delay = 0

        if not self.onGround:
            self.currentSpeed_Y += GRAVITY
        self.onGround = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.move_delay > 0:  # Для работы ai
            self.move_delay -= 1
        else:
            self.right = False
            self.left = False


        self.rect.x += self.currentSpeed_X  # переносим свои положение на currentSpeed_X
        self.collide(self.currentSpeed_X, 0, platforms)

        self.rect.y += self.currentSpeed_Y
        self.collide(0, self.currentSpeed_Y, platforms)
        self.update_animation()


    def ai(self, hero):
        if self.alive and hero.alive and abs(self.rect.x - hero.rect.x) < 350 and abs(self.rect.y - hero.rect.y) < 64:  # Cтрельба
            self.right = 0
            self.left = 0
            if hero.rect.x < self.rect.x:
                self.facing = -1
            elif hero.rect.x > self.rect.x:
                self.facing = 1
            self.shoot(bullets)
        else:
            if random.randint(1, 100) == 1 and self.move_delay == 0:
                self.move_delay = random.randint(15, self.walk_area)
                if random.randint(1, 2) == 1:
                    self.right = True
                else:
                    self.left = True
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.currentSpeed_X = 0
            self.alive = False
            self.update_action(3)
        if self.rect.y - 800 > total_level_height:  # Проверка не вылетил ли из карты
            self.kill()


    def shoot(self, bullets):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 70
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.2 * self.facing), self.rect.centery, self.facing,8,1)
            bullets.add(bullet)
