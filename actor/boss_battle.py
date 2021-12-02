import enum

import pygame
import actor


class BOSSBattleStatus(enum.IntEnum):

    Station = 0
    Fight = 1
    Die = 2
    DieOver = 3


class BattleBOSS(pygame.sprite.Sprite):

    # 加载死亡行为

    def __init__(self):
        """
        初始化
        """
        pygame.sprite.Sprite.__init__(self)
        self.status = BOSSBattleStatus.Station
        self.die = actor.DirAction("BOSS\\die", "",4, 10, False)
        # 战斗行为
        self.fight = actor.DirAction("BOSS\\fight", "", 4, 6, False)
        # 站立行为
        self.station = actor.DirAction("BOSS\\station", "", 4, 4, True)
        self.hp = 20
        self.pos_x = 600
        self.pos_y = 500

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 增加或减少的生命值（可正 可负
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(BOSSBattleStatus.Die)

    def set_status(self, status):
        """
        修的战斗状态
        :param status:  状态值
        :return:
        """
        self.status = status
        if status == BOSSBattleStatus.Fight:
            self.fight.reset()
        elif status == BOSSBattleStatus.Die:
            self.die.reset()
        elif status == BOSSBattleStatus.Station:
            self.station.reset()

    def action_over(self) -> bool:
        """
        判断一个行为是否结束
        :return: 是否结束
        """
        if self.status == BOSSBattleStatus.Fight:
            return self.fight.is_end()
        elif self.status == BOSSBattleStatus.Die:
            if self.die.is_end():
                self.status = BOSSBattleStatus.DieOver
            return self.die.is_end()
        elif self.status == BOSSBattleStatus.Station:
            return self.station.is_end()
        elif self.status == BOSSBattleStatus.DieOver:
            return True

    def draw(self, surface):
        """
        绘制函数
        :param surface: 背景图片
        """
        dir = 2
        if self.status == BOSSBattleStatus.Station:
            image = self.station.get_current_image(dir)

        elif self.status == BOSSBattleStatus.Fight:
            image = self.fight.get_current_image(dir)

        elif self.status == BOSSBattleStatus.Die:
            image = self.die.get_current_image(dir)

        elif self.status == BOSSBattleStatus.DieOver:

            image = self.die.get_current_image(dir)

        if image:
            image = pygame.transform.scale(image, (132, 189))
            surface.blit(image, (self.pos_x, self.pos_y))
        pygame.draw.rect(surface, pygame.Color(0, 255, 0), pygame.Rect(700, 500, self.hp, 10))
