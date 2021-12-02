import pygame

from actor import Action
from dialog.djj_dialog import DJJDialog



class DJJ(pygame.sprite.Sprite):
    """
    类
    """

    def __init__(self, pos_x: int, pos_y: int):
        """
        初始化角色
        :param pos_x: x坐标
        :param pos_y: y坐标
        """
        pygame.sprite.Sprite.__init__(self)
        # 保存位置信息
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 83
        self.height = 120
        # 当前区域位置
        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)
        self.dialog = DJJDialog()
        self.stop = False
        self.action = Action('djj', 'djj-0000', 4, True)

    def draw(self, surface, x: int, y: int):
        """
        绘制函数
        :param x:
        :param surface: 背景绘制区域
        :return:
        """
        image = self.action.get_current_image()
        if self.stop:
            surface.blit(self.dialog.surface, (20, 550))
        # header = pygame.transform.scale(image, (83, 124))
        if x < 0 :
            x = 0
        if y < 0:
            y = 0
        surface.blit(image, (self.pos_x -x, self.pos_y-y ))

        # if (self.pos_x > 400 and self.pos_x < 500) :
        #     self.pos_x -= 4

    def collide(self, actor):
        if pygame.sprite.collide_rect(self, actor):
            self.stop = True
        else:
            self.stop = False
