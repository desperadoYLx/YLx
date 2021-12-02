import enum

import pygame
import actor


class Monster1BattleStatus(enum.IntEnum):

    Station = 0
    Fight = 1
    Die = 2
    DieOver = 3


class BattleMonster1(pygame.sprite.Sprite):



    def __init__(self):
        """
        初始化
        """
        pygame.sprite.Sprite.__init__(self)
        self.status = Monster1BattleStatus.Station
        self.die = actor.Action1("monster1\\die", "0106-37f24957-0000", 10, False)
        # 战斗行为
        self.fight = actor.DirAction("monster1\\fight", "", 4, 7, False)
        # 站立行为
        self.station = actor.DirAction("monster1\\station", "", 4, 4, True)
        self.hp = 20
        self.pos_x = 500
        self.pos_y = 300

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 增加或减少的生命值（可正 可负
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(Monster1BattleStatus.Die)

    def set_status(self, status):
        """
        修改战斗状态
        :param status:  状态值
        :return:
        """
        self.status = status
        if status == Monster1BattleStatus.Fight:
            self.fight.reset()
        elif status == Monster1BattleStatus.Die:
            self.die.reset()
        elif status == Monster1BattleStatus.Station:
            self.station.reset()

    def action_over(self) -> bool:
        """
        判断一个行为是否结束
        :return: 是否结束
        """
        if self.status == Monster1BattleStatus.Fight:
            return self.fight.is_end()
        elif self.status == Monster1BattleStatus.Die:
            if self.die.is_end():
                self.status = Monster1BattleStatus.DieOver
            return self.die.is_end()
        elif self.status == Monster1BattleStatus.Station:
            return self.station.is_end()
        elif self.status == Monster1BattleStatus.DieOver:
            return True

    def draw(self, surface):
        """
        绘制函数
        :param surface: 背景图片
        """
        dir = 2
        if self.status == Monster1BattleStatus.Station:
            image = self.station.get_current_image(dir)

        elif self.status == Monster1BattleStatus.Fight:
            image = self.fight.get_current_image(dir)

        elif self.status == Monster1BattleStatus.Die:
            image = self.die.get_current_image()

        elif self.status == Monster1BattleStatus.DieOver:

            image = self.die.get_current_image()

        if image:
            image = pygame.transform.scale(image, (290, 200))
            surface.blit(image, (self.pos_x, self.pos_y))
        pygame.draw.rect(surface, pygame.Color(0, 255, 0), pygame.Rect(630, 330, self.hp, 10))
