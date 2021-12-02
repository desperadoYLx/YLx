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


class QishidianScene:
    scene_result = SceneResult.Ongoing

    def __init__(self, surface: pygame.Surface, xiao):
        """
        村庄场景初始化
        :param surface: 窗口绘制的surface
        """

        self.screen = surface
        tiled_path = os.path.join("resource", "tmx", "qishidian.tmx")
        self.tiled = TiledScene(tiled_path)
        self.fade = FadeScene(self.tiled.surface)
        self.zzh = None
        self.obstacle_group = pygame.sprite.Group()
        self.xiao = xiao
        self.pos_x = 0
        self.pos_y = 0
        self.init_actor()
        self.sound = pygame.mixer.Sound('resource/music/Rec 0001.wav')
        self.sound2 = pygame.mixer.Sound('resource/music/Rec hhhh.wav')
        self.n = 0
        self.z = 0
        sound_path = os.path.join("resource", "music", "Mark Petrie - Go Time.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        # 临时surface
        self.temp_surface = self.tiled.surface.copy()

    def init_actor(self):
        """
        初始化角色人物
        return:
        """
        for group in self.tiled.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == 'god':
                    for obj in group:
                        if obj.name == 'zzh':
                            self.zzh = Zzh(obj.x + 220, obj.y + 150)

                if group.name == 'obstacle':
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)

                if group.name == 'actor':
                    for obj in group:
                        if obj.name == 'xiao':
                            self.xiao.reset_pos(obj.x, obj.y)
                            self.pos_x = obj.x - 550
                            self.pos_y = obj.y - 375

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))

        self.zzh.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.xiao.draw(self.temp_surface, self.pos_x, self.pos_y)
        return self.temp_surface

    def run(self):
        """
        场景的运行
        :return:
        """
        while self.tiled.surface.get_width() - 1100 < self.pos_x:
            self.pos_x -= 1
        while self.tiled.surface.get_height() - 750 < self.pos_y:
            self.pos_y -= 1
        scene_exit = False
        clock = pygame.time.Clock()
        while not scene_exit:
            key_down = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.scene_result = SceneResult.Quit
                    scene_exit = True
                if event.type == KEYDOWN:
                    key_down = True
                    pressed_key = event.key
            if key_down:

                temp_pos = self.xiao.key_move(pressed_key, self.obstacle_group)

                if 0 <= self.pos_x <= self.tiled.surface.get_width() - 1100 and 0 <= self.pos_y <= self.tiled.surface.get_height() - 750:
                    if temp_pos:
                        self.pos_x += temp_pos[0]
                        self.pos_y += temp_pos[1]
                elif self.pos_x < 0:
                    self.pos_x += 1
                    while self.pos_x < 0:
                        self.pos_x += 1
                elif self.pos_y < 0:
                    self.pos_y += 1
                    while self.pos_y < 0:
                        self.pos_y += 1
                elif self.tiled.surface.get_width() - 1100 < self.pos_x:
                    self.pos_x -= 1
                    while self.tiled.surface.get_width() - 1100 < self.pos_x:
                        self.pos_x -= 1
                elif self.tiled.surface.get_height() - 750 < self.pos_y:
                    self.pos_y -= 1
                    while self.tiled.surface.get_height() - 750 < self.pos_y:
                        self.pos_y -= 1
                # 如果处于对话中，并且按键Y同意进入第二个场景

                if self.zzh.stop and pressed_key == K_y:
                    self.fade.set_status(SceneStatus.Out)  # 设置状态为渐出
                    self.zzh.stop = False
                if self.zzh.stop and pressed_key == K_n:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                if self.zzh.stop and pressed_key == K_g:
                    self.z = 1
            if self.fade.get_out():
                self.scene_result = SceneResult.Next
                scene_exit = True  # 渐出效果执行完毕

            # 场景处于渐出状态时，土地公不与孙悟空进行碰撞检查
            if self.fade.status != SceneStatus.Out:
                self.zzh.collide(self.xiao)
            if self.zzh.stop and self.n == 0:
                self.sound.play(0)
                self.n = 1
            if self.zzh.stop and self.z == 1:
                self.sound2.play(0)
                self.z = 2
            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))
            if self.zzh.stop and pressed_key == K_g:
                self.screen.blit(XIAO8Dialog().surface, (0, 0))
                self.screen.blit(ZZH2Dialog().surface, (20, 600))

            pygame.display.update()
            clock.tick(10)
        return scene_exit
