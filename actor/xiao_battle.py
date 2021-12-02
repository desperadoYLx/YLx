import enum
import pygame
import actor


class XIAOBattleStatus(enum.IntEnum):
    """
   状态
    """
    Station = 0
    Fight = 1
    Escape = 2
    EscapeOver = 3
    Die = 4
    DieOver = 5


class BattleXIAO(pygame.sprite.Sprite):
    """
    战斗中
    """
    def __init__(self, hp: int):
        """
        初始化战斗
        :param hp: 生命值
        """
        pygame.sprite.Sprite.__init__(self)  # 调用父类（Sprite）构造函数
        # 魔法战斗
        self.magic_fight = actor.DirAction("xiao\\fight", "", 4, 8, False)
        # 死亡和逃跑
        self.magic_die_escape = actor.DirAction("xiao\\die", "", 4, 4, False)
        # 站立行为
        self.station = actor.DirAction("xiao\\station", "", 4, 4, True)

        self.status = XIAOBattleStatus.Station
        self.hp = hp
        self.pos_x = 250
        self.pos_y = 200

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 被攻击掉的生命值，可正 可负
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(XIAOBattleStatus.Die)

    def set_status(self, status):
        """
        修改战斗状态
        :param status: 状态值
        """
        self.status = status
        if status == XIAOBattleStatus.Fight:
            self.magic_fight.reset()
        elif status == XIAOBattleStatus.Station:
            self.station.reset()
        elif status == XIAOBattleStatus.Escape:
            self.magic_die_escape.reset()
        elif status == XIAOBattleStatus.Die:
            self.magic_die_escape.reset()

    def action_over(self) -> bool:
        """
        行为是否结束
        :return: 是否结束
        """
        if self.status == XIAOBattleStatus.Station:
            return self.station.is_end()
        elif self.status == XIAOBattleStatus.Fight:
            return self.magic_fight.is_end()
        elif self.status == XIAOBattleStatus.Escape:
            if self.magic_die_escape.is_end():
                self.status = XIAOBattleStatus.EscapeOver
            return self.magic_die_escape.is_end()
        elif self.status == XIAOBattleStatus.Die:
            if self.magic_die_escape.is_end():
                self.status = XIAOBattleStatus.DieOver
            return self.magic_die_escape.is_end()

    def draw(self, surface: pygame.Surface):
        """
        绘制函数
        :param surface: 背景
        """
        dir = 0
        if self.status == XIAOBattleStatus.Station:

            image = self.station.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))
        elif self.status == XIAOBattleStatus.Fight:
            image = self.magic_fight.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))

        elif self.status == XIAOBattleStatus.Die:
            image = self.magic_die_escape.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))

        elif self.status == XIAOBattleStatus.DieOver:
            image = self.magic_die_escape.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))

        elif self.status == XIAOBattleStatus.Escape:
            image = self.magic_die_escape.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))

        elif self.status == XIAOBattleStatus.EscapeOver:
            image = self.magic_die_escape.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))

        pygame.draw.rect(surface, pygame.Color(0, 255, 0),pygame.Rect(400, 300, self.hp, 10))
