"""
村庄的场景
"""
import os
import pygame
from pytmx import pytmx

from actor.boss import BOSS
from actor.diren1 import DIREN1
from actor.monster2 import Monster2
from actor.monster3 import Monster3
from dialog.battle_dialog2 import BattleDialog2
from dialog.battle_dialog3 import BattleDialog3
from dialog.battle_dialogx import BattleDialogX
from dialog.boss_dialog import BOSSDialog
from dialog.xiao3_dialog import XIAO3Dialog
from dialog.xiao4_dialog import XIAO4Dialog
from dialog.xiao5_dialog import XIAO5Dialog
from dialog.xiao6_dialog import XIAO6Dialog
from scene import TiledScene, FadeScene, SceneStatus, SceneResult
from actor.god import God
from actor.xiao import XIAO
from scene import TiledScene, FadeScene
from pygame.constants import QUIT, KEYDOWN, K_y, K_n


class ZHONGMU:

    def __init__(self, surface: pygame.Surface, xiao):
        """
        寺庙场景初始化
        :param surface: 窗口绘制的surface
        """
        self.battle_dialog = None
        self.battle_dialog2 = None
        self.battle_dialog3 =None
        self.screen = surface
        tiled_path = os.path.join("resource", "tmx", "zhongmu.tmx")
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)
        self.n = 0
        self.sound = pygame.mixer.Sound('resource/music/Rec 0002.wav')
        self.obstacle_group = pygame.sprite.Group()
        self.xiao = xiao
        self.pos_x = 0
        self.pos_y = 0
        self.duihua3 = None
        self.duihua4 = None
        self.duihua5 = None
        self.monster3 = None
        self.boss = None
        self.monster2_group = []
        self.diren_group = []
        self.boss_group = pygame.sprite.Group()
        self.monster2d_group = pygame.sprite.Group()
        self.monster3d_group = pygame.sprite.Group()
        self.init_actor()
        sound_path = os.path.join("resource", "music", "zhongmu.mp3")
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

                if group.name == 'actor':
                    for obj in group:
                        if obj.name == 'xiao':
                            self.xiao.reset_pos(obj.x, obj.y)
                            self.pos_x = obj.x - 550
                            self.pos_y = obj.y - 375

                if group.name == 'DUIHUA3':
                    for obj in group:
                        self.duihua3 = pygame.sprite.Sprite()
                        self.duihua3.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if group.name == 'DUIHUA4':
                    for obj in group:
                        self.duihua4 = pygame.sprite.Sprite()
                        self.duihua4.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if group.name == 'DUIHUA5':
                    for obj in group:
                        self.duihua5 = pygame.sprite.Sprite()
                        self.duihua5.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

                if group.name == 'monster2':
                    for obj in group:
                        if obj.name == 'M':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster2d_group.add(monster)
                        if obj.name == 'monster2':
                            monster2 = Monster2(obj.x - 100, obj.y - 100)
                            self.monster2_group.append(monster2)
                if group.name == 'monster3':
                    for obj in group:
                        if obj.name == 'M3':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster3d_group.add(monster)
                        if obj.name == 'monster3':
                            self.monster3 = Monster3(obj.x - 100, obj.y - 200)

                if group.name == 'BOSS':
                    for obj in group:
                        if obj.name == 'B':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.boss_group.add(monster)
                        if obj.name == 'diren':
                            diren = DIREN1(obj.x - 100, obj.y - 100)
                            self.diren_group.append(diren)
                        if obj.name == 'boss':
                            self.boss = BOSS(obj.x - 90, obj.y - 250)


    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 孙悟空绘制
        if self.battle_dialog is None:
            for monster2 in self.monster2_group:
                monster2.draw(self.temp_surface, self.pos_x, self.pos_y)

        if self.battle_dialog3 is None:
            for diren in self.diren_group:
                diren.draw(self.temp_surface, self.pos_x, self.pos_y)
            self.boss.draw(self.temp_surface, self.pos_x, self.pos_y - 100)

        self.xiao.draw(self.temp_surface, self.pos_x, self.pos_y)

        if self.battle_dialog and not self.battle_dialog.over_show:
            self.battle_dialog.draw(self.temp_surface)

        if self.battle_dialog2 and not self.battle_dialog2.over_show:
            self.battle_dialog2.draw(self.temp_surface)

        if self.battle_dialog3 and not self.battle_dialog3.over_show:
            self.battle_dialog3.draw(self.temp_surface)

        if self.battle_dialog2 is None:
            self.monster3.draw(self.temp_surface, self.pos_x, self.pos_y - 100)
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
                # if self.god.stop and pressed_key == K_y:
                #     self.fade.set_status(SceneStatus.Out)  # 设置状态为渐出
                #     self.god.stop = False
                # if self.god.stop and pressed_key == K_n:
                #     self.scene_result = SceneResult.Fail
                #     scene_exit = True
            if self.fade.get_out():
                self.scene_result = SceneResult.Next
                scene_exit = True  # 渐出效果执行完毕
            collide_list = pygame.sprite.collide_rect(self.duihua3, self.xiao)
            collide_list1 = pygame.sprite.collide_rect(self.duihua4, self.xiao)
            collide_list2 = pygame.sprite.collide_rect(self.duihua5, self.xiao)

            # 场景处于渐出状态时，土地公不与孙悟空进行碰撞检查
            # if self.fade.status != SceneStatus.Out:
            #     self.god.collide(self.xiao)
            self.create_battle_dialog()
            self.create_battle_dialog2()
            self.create_battle_dialog3()
            # 打斗处理
            if self.battle_dialog and not self.battle_dialog.over_show:
                self.battle_dialog.process(key_down, pressed_key)
                self.xiao.hp = self.battle_dialog.xiao.hp

            if self.battle_dialog2 and not self.battle_dialog2.over_show:
                self.battle_dialog2.process(key_down, pressed_key)
                self.xiao.hp = self.battle_dialog2.xiao.hp

            if self.battle_dialog3 and not self.battle_dialog3.over_show:
                self.battle_dialog3.process(key_down, pressed_key)
                self.xiao.hp = self.battle_dialog3.xiao.hp

            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))
            if collide_list:
                self.screen.blit(XIAO3Dialog().surface, (0, 0))
            if collide_list1:
                self.screen.blit(XIAO5Dialog().surface, (0, 0))

            if collide_list2:
                self.screen.blit(BOSSDialog().surface, (0, 0))
                self.screen.blit(XIAO6Dialog().surface, (0, 600))
                if self.n == 0:
                    self.sound.play(0)
                    self.n = 1
            if self.battle_dialog3 and self.battle_dialog3.over_show:
                if self.xiao.hp <= 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.xiao.hp >0 and self.battle_dialog3.over_OVER:

                    self.scene_result = SceneResult.Win
                    scene_exit = True
                elif self.xiao.hp >0 and not self.battle_dialog3.over_OVER:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
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
            collide_list = pygame.sprite.spritecollide(self.xiao, self.monster2d_group, True)
            if collide_list:
                self.battle_dialog = BattleDialog2(self.xiao.hp)

    def create_battle_dialog2(self):
        """
        创建打斗场景
        """
        collide_flag = True
        if self.battle_dialog2 is None:
            collide_flag = True
        elif self.battle_dialog2.over_show:

            collide_flag = True

        if collide_flag:
            collide_list = pygame.sprite.spritecollide(self.xiao, self.monster3d_group, True)
            if collide_list:
                self.battle_dialog2 = BattleDialog3(self.xiao.hp)

    def create_battle_dialog3(self):
        """
        创建打斗场景
        """
        collide_flag = True
        if self.battle_dialog3 is None:
            collide_flag = True
        elif self.battle_dialog3.over_show:

            collide_flag = True

        if collide_flag:
            collide_list = pygame.sprite.spritecollide(self.xiao, self.boss_group, True)
            if collide_list:
                self.battle_dialog3 = BattleDialogX(self.xiao.hp)
