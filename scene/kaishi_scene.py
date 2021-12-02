import os
import sys
import pygame
import self as self
from pygame.constants import QUIT
import os
import pygame
from pygame.constants import QUIT, KEYDOWN, K_y, K_n, K_g
from actor.xiao import XIAO
from actor.zzh import Zzh
from dialog.xiao8_dialog import XIAO8Dialog
from dialog.zzh2_dialog import ZZH2Dialog
from scene import TiledScene
from pytmx import pytmx
from pygame.constants import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from scene import TiledScene, FadeScene, SceneStatus, SceneResult


from scene import SceneResult


class KaishiScene:
    scene_result = SceneResult.Ongoing

    # pygame 初始化
    pygame.init()

    back_img_path = os.path.join('../resource', 'kaishi.jpg')


    background = pygame.image.load(back_img_path)

    screen = pygame.display.set_mode((1100, 750), 0, 32)
    pygame.display.set_caption('PyGame 我的背景图片')
    # icon_path = os.path.join('./resource', 'image', 'berry.png')
    # icon = pygame.image.load(icon_path)
    # pygame.display.set_icon(icon)
    scene_exit = False
    pressed_key = None
    while not scene_exit:
        key_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                scene_result = SceneResult.Quit
                scene_exit = True
            if event.type == KEYDOWN:
                key_down = True
                pressed_key = event.key
        if key_down:
            if pressed_key == K_y:
                self.scene_result = SceneResult.Next
            # 渐出效果执行完毕

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (350, 250))


        pygame.display.update()
