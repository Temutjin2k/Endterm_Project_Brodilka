from pygame import *
from Bullet import Bullet
from Settings import total_level_height
import os

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 50
JUMP_POWER = 11
GRAVITY = 0.35

mixer.init()
shooting_sound = mixer.Sound("Sounds/shoot_blaster.mp3")
shooting_sound.set_volume(0.6)
jump_sound = mixer.Sound("Sounds/jump.wav")
jump_sound.set_volume(0.5)
death_sound = mixer.Sound("Sounds/death_sound.mp3")
death_sound.set_volume(0.5)

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.ammo = 15
        self.max_ammo = 30
        self.speed = 5
        self.kills = 0
        self.death_count = 0
        self.level_timer = 300 * 60


        self.left = self.right = self.up = False
        self.shooting = False
        self.can_move = True

        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.currentSpeed_X = 0  # скорость перемещения. 0 - стоять на месте
        self.currentSpeed_Y = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = image.load("Images/Player/Stand/0.png").convert_alpha()
        self.rect = Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)  # Типо Хитбокс
        self.facing = 1  # Сторона куда напрвалне персонаж
        self.shoot_cooldown = 0

        #  Animation
        self.animation_list = [] # Двухмерный массив со всеми анимациямий
        self.frame_index = 0
        self.action = 0
        self.flip = False
        self.update_time = time.get_ticks()

        animation_types = ['Stand', 'Walk', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'images/{"Player"}/{animation}'))
            for i in range(num_of_frames):
                img = image.load(f'images/{"Player"}/{animation}/{i}.png')
                img = transform.scale(img, (PLAYER_WIDTH,  PLAYER_HEIGHT))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]

    def update(self, platforms):
        if self.alive and self.can_move:
            if self.up:
                if self.onGround:
                    self.currentSpeed_Y -= JUMP_POWER
                    jump_sound.play(0)
            if self.left:
                self.currentSpeed_X = -self.speed  # Лево = x- n
                self.flip = True
                self.facing = -1
            if self.right:
                self.currentSpeed_X = self.speed  # Право = x + n
                self.flip = True
                self.facing = 1

            if not (self.left or self.right):  # стоим, когда нет указаний идти
                self.currentSpeed_X = 0

            if self.health > self.max_health:
                self.health = self.max_health

            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo

        if not self.onGround:
            self.currentSpeed_Y += GRAVITY

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.check_alive()
        self.onGround = False

        self.rect.x += self.currentSpeed_X  # переносим свои положение на currentSpeed_X
        self.collide(self.currentSpeed_X, 0, platforms)

        self.rect.y += self.currentSpeed_Y
        self.collide(0, self.currentSpeed_Y, platforms)
        self.update_animation()



    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100  # Miliseconds
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        if self.facing == -1:
            self.image = transform.flip(self.image, True, False)
        else:
            self.image = transform.flip(self.image, False, False)
        # check if enough time has passed since the last update
        if time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = time.get_ticks()

    def collide(self, currentSpeed_X, currentSpeed_Y, platforms):
        for block in platforms:
            if sprite.collide_rect(self, block):  # если есть пересечение платформы с игроком

                if currentSpeed_X > 0:
                    # если движется вправо
                    self.rect.right = block.rect.left  # то не движется вправо

                if currentSpeed_X < 0:                      # если движется влево
                    self.rect.left = block.rect.right  # то не движется влево

                if currentSpeed_Y > 0:                      # если падает вниз
                    self.rect.bottom = block.rect.top  # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.currentSpeed_Y = 0                 # и энергия падения пропадает

                if currentSpeed_Y < 0:                      # если движется вверх
                    self.rect.top = block.rect.bottom  # то не движется вверх
                    self.currentSpeed_Y = 0                 # и энергия прыжка пропадает


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.currentSpeed_X = 0
            self.alive = False
            self.update_action(3)

        if self.rect.y - 800 > total_level_height:  # Проверка не вылетил ли из карты
            self.health = 0
            self.speed = 0
            self.currentSpeed_X = 0
            self.alive = False
            self.update_action(3)

        if not self.alive and self.death_count == 0:

            death_sound.play()
            self.death_count += 1

    def shoot(self, bullets):
        if self.shoot_cooldown == 0 and self.ammo != 0:
            self.shoot_cooldown = 25
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.2 * self.facing), self.rect.centery, self.facing, 8,0)
            bullets.add(bullet)
            self.ammo -= 1
            shooting_sound.play(0)


