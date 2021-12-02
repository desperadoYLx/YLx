import pygame

from actor import DirAction
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT


class XIAO(pygame.sprite.Sprite):
    """
    角色
    """

    def __init__(self):
        """
        构造函数
        """
        pygame.sprite.Sprite.__init__(self)
        self.walk = DirAction("xiao", "", 4, 6, True)
        self.pos_x = 0
        self.pos_y = 0
        self.hp = 200
        self.dir = 0
        self.rect = pygame.Rect(self.pos_x + 34, self.pos_y + 180, 10, 10)

    def reset_pos(self, x: int, y: int):
        """
        重置位置信息
        :param x: x坐标
        :param y: y坐标
        :return:
        """
        self.pos_x = x-190
        self.pos_y = y-180
        self.rect = pygame.Rect(self.pos_x + 200, self.pos_y + 200, 10, 10)

    def draw(self, surface: pygame.Surface, x: int, y: int):
        image = self.walk.get_current_image(self.dir)
        surface.blit(image, (self.pos_x - x, self.pos_y - y))

    def key_move(self, key: int, obstacle_group: pygame.sprite.Group):
        pos_y = self.pos_y
        pos_x = self.pos_x
        # 计算运动后坐标
        if key == K_UP:
            self.dir = 2
            pos_y = self.pos_y - 10
            pos_x = self.pos_x - 10
        elif key == K_DOWN:
            self.dir = 0
            pos_x = self.pos_x + 10
            pos_y = self.pos_y + 10
        elif key == K_LEFT:
            self.dir = 1
            pos_x = self.pos_x - 10
            pos_y = self.pos_y + 10
        elif key == K_RIGHT:
            self.dir = 3
            pos_x = self.pos_x + 10
            pos_y = self.pos_y - 10
        else:
            return None

        self.rect = pygame.Rect(pos_x +200, pos_y + 200, 30, 10)
        collide_list = pygame.sprite.spritecollide(self, obstacle_group, False)

        if len(collide_list) > 0:
            self.rect = pygame.Rect(self.pos_x + 200, self.pos_y + 200, 30, 10)
            return None
        else:
            return self.__move__()

    # 0 下 1 左  2 上 3 右
    def __move__(self):
        if self.dir == 2:
            x = -20
            y = -20

        elif self.dir == 0:
            x = 20
            y = 20

        elif self.dir == 1:
            x = -20
            y = 20
        else:
            x = 20
            y = -20

        self.pos_y += y
        self.pos_x += x
        self.rect = pygame.Rect(self.pos_x + 200, self.pos_y + 200, 30, 10)
        return [x, y]
