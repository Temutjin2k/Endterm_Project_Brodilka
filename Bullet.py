from pygame import *
from random import randint


class Bullet(sprite.Sprite):
    def __init__(self, x, y, direction, speed, side):
        self.image = image.load("images/Bullets/bullet.png").convert_alpha()
        self.image = transform.scale(self.image, (15, 10))
        if direction == -1:
            self.image = transform.flip(self.image, True, False)

        sprite.Sprite.__init__(self)
        self.speed = speed
        self.rect = self.image.get_rect()  # Хитбоксы пули
        self.rect.center = (x, y)
        self.direction = direction
        self.side = side  # Если '0' то пуля выпущена игроком если '1' то пуля вражеская
        self.startX = x
        self.startY = y


    def update(self, platforms, hero, enemies, bullets):
        self.rect.x += (self.speed * self.direction)

        if sprite.collide_rect(self, hero):
            if hero.alive and self.side == 1:
                hero.health -= randint(10, 25)
                self.kill()

        for enemy in enemies:
            if sprite.collide_rect(self, enemy) and enemy != hero and self.side == 0:
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

        for platform in platforms:
            if sprite.collide_rect(self, platform):
                self.kill()
        if abs(self.startX - self.rect.x) > 1000:
            self.kill()
