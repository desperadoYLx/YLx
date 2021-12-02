"""
村庄的场景
"""
import os
import pygame
from pytmx import pytmx
from scene import TiledScene, FadeScene, SceneStatus, SceneResult
from actor.god import God
from actor.xiao import XIAO
from scene import TiledScene, FadeScene
from pygame.constants import QUIT, KEYDOWN, K_y, K_n


class DIERDIAN:
    """
    寺庙场景
    """
    def __init__(self, surface: pygame.Surface, xiao):
        """
        寺庙场景初始化
        :param surface: 窗口绘制的surface
        """
        self.screen = surface
        tiled_path = os.path.join("resource", "tmx", "dierdian.tmx")
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        self.obstacle_group = pygame.sprite.Group()
        self.xiao = xiao
        self.pos_x = 0
        self.pos_y = 0
        self.init_actor()
        sound_path = os.path.join("resource", "music", "Varien - Future Funk.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)
        # 临时surface
        self.temp_surface = pygame.Surface((1100, 750))

    def init_actor(self):
        """
        初始化角色人物
        return:
        """
        for group in self.tiled.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == 'obstacle':
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)
                if group.name == 'god':
                    for obj in group:
                        if obj.name == 'god':
                            self.god = God(obj.x, obj.y)
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
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 孙悟空绘制
        self.god.draw(self.temp_surface, self.pos_x, self.pos_y)
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
                    while  self.pos_x < 0:
                        self.pos_x += 1
                elif self.pos_y < 0:
                    self.pos_y += 1
                    while  self.pos_y < 0:
                        self.pos_y += 1
                elif self.tiled.surface.get_width() - 1100 < self.pos_x:
                    self.pos_x -= 1
                    while self.tiled.surface.get_width() - 1100 < self.pos_x:
                        self.pos_x -= 1
                elif self.tiled.surface.get_height() - 750< self.pos_y:
                    self.pos_y -= 1
                    while self.tiled.surface.get_height() - 750 < self.pos_y:
                        self.pos_y -= 1
                # 如果处于对话中，并且按键Y同意进入第二个场景
                if self.god.stop and pressed_key == K_y:
                    self.fade.set_status(SceneStatus.Out)  # 设置状态为渐出
                    self.god.stop = False
                if self.god.stop and pressed_key == K_n:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
            if self.fade.get_out():
                self.scene_result = SceneResult.Next
                scene_exit = True  # 渐出效果执行完毕

            # 场景处于渐出状态时，土地公不与孙悟空进行碰撞检查
            if self.fade.status != SceneStatus.Out:
                self.god.collide(self.xiao)

            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))

            pygame.display.update()
            clock.tick(10)
        return scene_exit

