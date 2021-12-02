import os
import pygame
from pytmx import pytmx

from actor.djj import DJJ
from actor.longweidajun import LWDJ
from actor.longweis import LWS
from actor.longweix import LWX
from actor.monster1 import Monster1
from actor.zuoji import ZUOJI
from dialog.battle_dialog import BattleDialog
from dialog.longwei_dialog import LWDialog
from dialog.xiao1_dialog import XIAO1Dialog
from dialog.xiao4_dialog import XIAO4Dialog
from scene import TiledScene, FadeScene, SceneStatus, SceneResult
from actor.god import God
from actor.xiao import XIAO
from scene import TiledScene, FadeScene
from pygame.constants import QUIT, KEYDOWN, K_y


class DISANDIAN:
    """
    寺庙场景
    """

    def __init__(self, surface: pygame.Surface, xiao):
        """
        寺庙场景初始化
        :param surface: 窗口绘制的surface
        """
        self.screen = surface
        tiled_path = os.path.join("resource", "tmx", "disandian.tmx")
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)
        self.lwx_group = []
        self.lws_group = []
        self.lwdj_group = []
        self.monster1 = None
        self.duihua1 = None
        self.duihua2 = None
        self.duihua4 = None
        self.djj = None
        self.zuoji = None
        self.obstacle_group = pygame.sprite.Group()
        self.xiao = xiao
        self.pos_x = 0
        self.pos_y = 0
        self.n = 0
        self.sound = pygame.mixer.Sound('resource/music/Rec 0015.wav')
        self.monster_group = pygame.sprite.Group()
        sound_path = os.path.join("resource", "music", "disantu.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)
        # 临时surface
        self.init_actor()
        self.temp_surface = pygame.Surface((1100, 750))
        self.battle_dialog = None

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
                if group.name == 'actor':
                    for obj in group:
                        if obj.name == 'xiao':
                            self.xiao.reset_pos(obj.x, obj.y)
                            self.pos_x = obj.x - 550
                            self.pos_y = obj.y - 375
                if group.name == 'longweix':
                    for obj in group:
                        if obj.name == 'LW':
                            lwx = LWX(obj.x + 300, obj.y + 250)
                            self.lwx_group.append(lwx)
                if group.name == 'longweidj':
                    for obj in group:
                        if obj.name == 'LW':
                            lwx = LWDJ(obj.x - 50, obj.y - 70)
                            self.lwdj_group.append(lwx)
                if group.name == 'DUIHUA':
                    for obj in group:
                        self.duihua1 = pygame.sprite.Sprite()
                        self.duihua1.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if group.name == 'DUIHUA2':
                    for obj in group:
                        self.duihua2 = pygame.sprite.Sprite()
                        self.duihua2.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if group.name == 'DUIHUA4':
                    for obj in group:
                        self.duihua4 = pygame.sprite.Sprite()
                        self.duihua4.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if group.name == 'longweis':
                    for obj in group:
                        if obj.name == 'LWS':
                            lws = LWS(obj.x + 320, obj.y + 300)
                            self.lws_group.append(lws)
                if group.name == 'jiangjun':
                    for obj in group:
                        if obj.name == 'DJJ':
                            self.djj = DJJ(obj.x - 50, obj.y - 50)
                if group.name == 'ZUOJI':
                    for obj in group:
                        if obj.name == 'Z1':
                            self.zuoji = ZUOJI(obj.x - 50, obj.y - 50)
                if group.name == 'monster':
                    for obj in group:
                        if obj.name == 'M1':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group.add(monster)
                        if obj.name == 'monster1':
                            self.monster1 = Monster1(obj.x - 100, obj.y - 200)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 孙悟空绘制
        for lwx in self.lwx_group:
            lwx.draw(self.temp_surface, self.pos_x, self.pos_y)

        for lws in self.lws_group:
            lws.draw(self.temp_surface, self.pos_x, self.pos_y)
        for lwdj in self.lwdj_group:
            lwdj.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.xiao.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.djj.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.zuoji.draw(self.temp_surface, self.pos_x, self.pos_y)
        if self.battle_dialog and not self.battle_dialog.over_show:
            self.battle_dialog.draw(self.temp_surface)

        if self.battle_dialog is None:
            self.monster1.draw(self.temp_surface, self.pos_x, self.pos_y - 100)
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
                if self.zuoji.stop and pressed_key == K_y:
                    self.fade.set_status(SceneStatus.Out)  # 设置状态为渐出
                    self.zuoji.stop = False

            if self.fade.get_out():
                self.scene_result = SceneResult.Next
                scene_exit = True  # 渐出效果执行完毕

            collide_list = pygame.sprite.collide_rect(self.duihua1, self.xiao)
            collide_list2 = pygame.sprite.collide_rect(self.duihua2, self.xiao)
            collide_list4 = pygame.sprite.collide_rect(self.duihua4, self.xiao)
            # 场景处于渐出状态时，土地公不与孙悟空进行碰撞检查
            if self.fade.status != SceneStatus.Out:
                self.zuoji.collide(self.xiao)
            self.create_battle_dialog()

            # 打斗处理
            if self.battle_dialog and not self.battle_dialog.over_show:
                self.battle_dialog.process(key_down, pressed_key)
                self.xiao.hp = self.battle_dialog.xiao.hp

            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))

            self.djj.collide(self.xiao)


            if collide_list:
                self.screen.blit(XIAO1Dialog().surface, (0, 0))

            if collide_list2:
                self.screen.blit(LWDialog().surface, (20, 600))
                if  self.n == 0:
                    self.sound.play(0)
                    self.n = 1

            if collide_list4:
                self.screen.blit(XIAO4Dialog().surface, (20, 600))

            pygame.display.update()
            clock.tick(10)
        return scene_exit

    def create_battle_dialog(self):
        """
        创建打斗场景
        """
        collide_flag = True
        if self.battle_dialog is None:
            collide_flag = True
        elif self.battle_dialog.over_show:

            collide_flag = True

        if collide_flag:
            collide_list = pygame.sprite.spritecollide(self.xiao, self.monster_group, True)
            if collide_list:
                self.battle_dialog = BattleDialog(self.xiao.hp)
