from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"


ammo_png = image.load("images/Platform/ammo_box.png").convert_alpha()
health_png = image.load("images/Platform/health_box.png").convert_alpha()
finish_png = image.load("images/Platform/finish.png").convert_alpha()

item_boxes = {
    "Health": health_png,
    "Ammo": ammo_png,
    "Finish": finish_png
}


class Platform(sprite.Sprite):
    def __init__(self, x, y, img):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = img
        self.health = 0

        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Item_box(sprite.Sprite):
    def __init__(self, item_type, x, y):
        sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.image = transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + PLATFORM_WIDTH // 2, y)

    def update(self, hero, enemies):
        if sprite.collide_rect(self, hero):
            if self.item_type == 'Health' and hero.health != hero.max_health:
                self.kill()
                hero.health += 35

            if self.item_type == 'Ammo' and hero.ammo != hero.max_ammo:
                hero.ammo += 10
                self.kill()
            if self.item_type == 'Finish' and hero.kills == len(enemies):
                hero.kills += 1  # Чтобы закончить уровень
                hero.currentSpeed_X = 0
                '''
                current level += 1
                '''

