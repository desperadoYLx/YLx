import enum
import pygame
import os

from actor.monster1_battle import BattleMonster1, Monster1BattleStatus
from actor.xiao_battle import BattleXIAO, XIAOBattleStatus
from dialog import blit_text
from pygame.constants import K_y, K_n, K_ESCAPE


class BattleStatus(enum.IntEnum):
    """
    战斗场景状态
    """
    xiao_dialog = 0  # swk对话框状态
    xiao_fight = 1  # swk打斗
    Enemy_fight = 2  # 敌方打斗
    Fail = 3  # 失败
    Win = 4  # 成功
    Escape = 5  # 逃跑


class BattleDialog:
    # 初始化当前状态
    status = BattleStatus.xiao_dialog

    def __init__(self, xiao_hp: int):
        """
        设置战斗场景中的各个属性值
        :param swk_hp: 生命值
        """

        self.xiao = BattleXIAO(xiao_hp)
        self.monster = BattleMonster1()
        # 背景相关初始化
        dialog_file = os.path.join('resource', 'img', 'dialog', '001 (17).png')
        self.dialog = pygame.image.load(dialog_file)
        self.dialog.set_alpha(255)

        self.dialog_width = self.dialog.get_width()
        self.dialog_height = self.dialog.get_width()
        # 对话相关文本和字体
        font_path = os.path.join('resource', 'font', '鸿雷板书简体-Regular.TTF')
        self.font = pygame.font.Font(font_path, 30)
        self.text = "歪嘴棒法 Y " \
                    " 逃跑 N "
        self.text2 = "获得胜利 " \
                     " 按 Esc 退出 "
        sound_path = os.path.join("resource", "music", "zhandou.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)
        # 设置显示状态
        self.over_show = False

    def process(self, key_down: bool, pressed_key: int):
        """
        打斗处理
        :param key_down:
        :param pressed_key:
        :return:
        """
        # 死亡结束
        if self.xiao.status == XIAOBattleStatus.DieOver:
            self.status = BattleStatus.Fail
            if key_down and pressed_key == K_ESCAPE:
                self.over_show = True
            return
        # 逃跑结束
        if self.xiao.status == XIAOBattleStatus.EscapeOver:
            self.status = BattleStatus.Escape
            if key_down and pressed_key == K_ESCAPE:
                xsound_path = os.path.join("resource", "music", "disantu.mp3")
                pygame.mixer.music.load(xsound_path)
                pygame.mixer.music.play(-1)
                self.over_show = True
            return
        # 死亡结束
        if self.monster.status == Monster1BattleStatus.DieOver:
            self.status = BattleStatus.Win
            if key_down and pressed_key == K_ESCAPE:
                xsound_path = os.path.join("resource", "music", "disantu.mp3")
                pygame.mixer.music.load(xsound_path)
                pygame.mixer.music.play(-1)
                self.over_show = True
            return

        # 死亡逃跑过程
        if self.xiao.status == XIAOBattleStatus.Die or self.xiao.status == XIAOBattleStatus.Escape:
            self.xiao.action_over()
            return

        # 死亡过程
        if self.monster.status == Monster1BattleStatus.Die:
            self.monster.action_over()
            if self.monster.status == Monster1BattleStatus.DieOver:

                xsound_path = os.path.join("resource", "music", "shengli.mp3")
                pygame.mixer.music.load(xsound_path)
                pygame.mixer.music.play(1)

            return

        #  对话框状态
        if self.status == BattleStatus.xiao_dialog:
            # 打斗
            if key_down and pressed_key == K_y:
                self.status = BattleStatus.xiao_fight
                self.xiao.set_status(XIAOBattleStatus.Fight)
                self.monster.set_status(Monster1BattleStatus.Station)
                self.sound2 = pygame.mixer.Sound('resource/music/Rec dadou1.wav')
                self.sound2.play(0)
            # 逃跑
            if key_down and pressed_key == K_n:
                self.status = BattleStatus.Escape
                self.monster.set_status(Monster1BattleStatus.Station)
                self.xiao.set_status(XIAOBattleStatus.Escape)
        # 打斗
        if self.status == BattleStatus.xiao_fight:
            if self.xiao.action_over():  # 打斗是一个过程，必须打完
                # 切换状态
                self.status = BattleStatus.Enemy_fight
                self.xiao.set_status(XIAOBattleStatus.Station)
                self.monster.set_status(Monster1BattleStatus.Fight)
                # 后减生命值
                self.monster.attack_hp(-10)
                self.xiao.attack_hp(10)
                if self.monster.hp>0:
                    self.sound2 = pygame.mixer.Sound('resource/music/Rec dadou2.wav')
                    self.sound2.play(0)
                return

        if self.status == BattleStatus.Enemy_fight:
            if self.monster.action_over():  # 打斗是一个过程，必须打完
                self.status = BattleStatus.xiao_dialog
                self.xiao.set_status(XIAOBattleStatus.Station)
                self.monster.set_status(Monster1BattleStatus.Station)
                self.xiao.attack_hp(-30)
                return

    def draw(self, surface):
        """
        绘制
        :param surface:  背景
        """
        # 干净的背景

        dialog = self.dialog.copy()
        #  文本的显示是状态来的
        if self.status == BattleStatus.xiao_dialog:
            blit_text(dialog, self.text, (375, 250), self.font)
        if self.monster.status == Monster1BattleStatus.DieOver:
            blit_text(dialog, self.text2, (375, 250), self.font)
        self.xiao.draw(dialog)
        self.monster.draw(dialog)
        surface.blit(dialog, ( 0, 0 ))

