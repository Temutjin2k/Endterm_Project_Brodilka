from pygame import *

VERSION = 'beta 0.1'


WIDTH, HEIGHT = 1000, 600
screen = display.set_mode((WIDTH, HEIGHT))
icon_img = image.load("images/icons/icon.png")
display.set_icon(icon_img)
display.set_caption("Endterm project")
bg = image.load("images/Background/black.png").convert_alpha()
bg = transform.scale(bg, (WIDTH, HEIGHT))
bg_start = image.load("images/Background/mountain_bg.png").convert_alpha()


# Создание объекта Surface для затемнения при смерти
overlay_color = (0, 0, 0, 200)
overlay_surface = Surface((WIDTH, HEIGHT), SRCALPHA)
overlay_surface.fill(overlay_color)


# Кнопки
start_btn_image = image.load("images/Buttons/start_btn.png").convert_alpha()
exit_btn_image = image.load("images/Buttons/exit_btn.png").convert_alpha()
restart_btn_image = image.load("images/Buttons/restart_btn.png").convert_alpha()
restart_btn_image = transform.scale(restart_btn_image, (300, 120))

victory_btn_image = image.load("images/Buttons/victory_btn.png").convert_alpha()
victory_btn_image = transform.scale(victory_btn_image, (400, 120))

continue_btn_image = image.load("images/Buttons/continue_btn.png").convert_alpha()
continue_btn_image = transform.scale(continue_btn_image, (400, 120))

menu_btn_image = image.load("images/Buttons/menu_btn.png").convert_alpha()
menu_btn_image = transform.scale(menu_btn_image, (250, 120))

lvl_complete_image = image.load("images/Buttons/lvl_complete.png"). convert_alpha()
lvl_complete_image = transform.scale(lvl_complete_image, (600, 120))


# Блоки
platform_default = image.load("images/Platform/platform.png").convert_alpha()
platform_black = image.load("images/Platform/BrickBlack.png").convert_alpha()
platform_red = image.load("images/Platform/BrickFireRed.png").convert_alpha()
platform_grey = image.load("images/Platform/BrickLightGrey.png").convert_alpha()

BG_COLOR = (94, 7, 86)

entities = sprite.Group()  # Все объекты
bullets = sprite.Group()  # Пули
platforms = []  # то, во что мы будем врезаться или опираться
item_box_group = sprite.Group()
enemies = sprite.Group()


PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32


levels = []
level_1 = [
       "                 -                                            ",
       "                 -                                            ",
       "                 -                                            ",
       "                 -                                            ",
       "                 -                                            ",
       "                                       E            333  333  ",
       "                          -----     ---------      3322332233 ",
       "                                                  332112211233",
       "                     --                           321111111123",
       "  P                                               321111111123",
       "------------------                   ah            3211111123 ",
       "                 --                -----            32111123  ",
       "      haE        ---      E                          321123   ",
       "      33333      -------------                        3223    ",
       "                                                       33     ",
       "                                                              ",
       " F        E   a                                            Eah",
       "--------------------------------------------------------------",

]

levels.append(level_1)

level2 = [
       "                                         ",
       "                                         ",
       "                                         ",
       "                                         ",
       "               E                         ",
       "            ---------                    ",
       "                    -           E ah  F  ",
       "                    ---------------------",
       "                                   -21312",
       "------                            E-13123",
       "                                ---------",
       "                                         ",
       "                           E             ",
       "       E                 ----            ",
       "     ------                              ",
       "                                         ",
       "                                         ",
       "                ah                       ",
       "22           -----                E      ",
       "                                ---------",
       "                                         ",
       "                   E                     ",
       " a  E  h         1212121                 ",
       "22222222                                 ",
       "                                      a  ",
       "                               ----------",
       "                                         ",
       " ah  E       E                           ",
       "-------------------------                ",
       "                                         ",
       "                                         ",
       "                                         ",
       "  P                       E           E  ",
       "11111111111111111111111111111111111111111",

]
levels.append(level2)

level_3 = [
       "1                                                                                           1",
       "1                                                                                           1",
       "1                                                                                           1",
       "1                                                                                           1",
       "1                                   E  h  E                                                 1",
       "1         E                       -----------                                               1",
       "1       ------                                                  E                           1",
       "1                                                              --------                     1",
       "1                       E                                              -              E   ah1",
       "1                     22222                                            --          ---------1",
       "1                                                                   E h---                  1",
       "1                            33             E              -----------------                1",
       "1              33333                    2222222                                             1",
       "1h a                                                                                        1",
       "1------                                                      ah                    aEah     1",
       "1                                                        ------                   -----     1",
       "1                             ----                                                          1",
       "1            a               -                                                              1",
       "1         ------                                                                            1",
       "1                                             11111                  -----                  1",
       "1                           E                                             --                1",
       "1 E                    22--22--                                                             1",
       "1----                          2   E                                                   E    1",
       "1                               22--22--22---              ------                   --------1",
       "1                                                                                           1",
       "1               a  E  h                                              E                      1",
       "1              222222222                                           -----                    1",
       "1                                                                                           1",
       "1                                                                            a              1",
       "1        E                                                                 ---              1",
       "1      22222                                                                                1",
       "1                                                                                           1",
       "1a  E                          P              F       E               E                 E ah1",
       "111111111111111111111111111111111            111111111111111111111111111111111111111111111111"

]
levels.append(level_3)

total_level_width = len(levels[0][0]) * PLATFORM_WIDTH
total_level_height = len(levels[0]) * PLATFORM_HEIGHT
