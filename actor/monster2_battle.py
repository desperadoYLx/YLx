import enum

import pygame
import actor


class Monster2BattleStatus(enum.IntEnum):
    """
    """
    Station = 0
    Fight = 1
    Die = 2
    DieOver = 3


class BattleMonster2(pygame.sprite.Sprite):
    """
    战斗的
    """

    # 加载死亡行为

    def __init__(self):
        """
        初始化
        """
        pygame.sprite.Sprite.__init__(self)
        self.status = Monster2BattleStatus.Station
        self.die = actor.Action1("monster1\\die", "0106-37f24957-0000", 10, False)
        # 战斗行为
        self.fight = actor.DirAction("monster1\\fight", "", 4, 7, False)
        # 站立行为
        self.station = actor.DirAction("monster1\\station", "", 4, 4, True)
        self.hp = 20
        self.pos_x = 450
        self.pos_y = 400

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 增加或减少的生命值（可正 可负
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(Monster2BattleStatus.Die)

    def set_status(self, status):
        """
        修改战斗状态
        :param status:  状态值
        :return:
        """
        self.status = status
        if status == Monster2BattleStatus.Fight:
            self.fight.reset()
        elif status == Monster2BattleStatus.Die:
            self.die.reset()
        elif status == Monster2BattleStatus.Station:
            self.station.reset()

    def action_over(self) -> bool:
        """
        判断一个行为是否结束
        :return: 是否结束
        """
        if self.status == Monster2BattleStatus.Fight:
            return self.fight.is_end()
        elif self.status == Monster2BattleStatus.Die:
            if self.die.is_end():
                self.status = Monster2BattleStatus.DieOver
            return self.die.is_end()
        elif self.status == Monster2BattleStatus.Station:
            return self.station.is_end()

    def draw(self, surface):
        """
        绘制函数
        :param surface: 背景图片
        """
        dir = 2
        if self.status == Monster2BattleStatus.Station:
            image = self.station.get_current_image(dir)

        elif self.status == Monster2BattleStatus.Fight:
            image = self.fight.get_current_image(dir)

        elif self.status == Monster2BattleStatus.Die:
            image = self.die.get_current_image()

        elif self.status == Monster2BattleStatus.DieOver:

            image = self.die.get_current_image()

        if image:
            image = pygame.transform.scale(image, (290, 200))
            surface.blit(image, (self.pos_x, self.pos_y))
        pygame.draw.rect(surface, pygame.Color(0, 255, 0), pygame.Rect(570, 430, self.hp, 10))
