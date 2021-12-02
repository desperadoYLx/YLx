import pygame
from actor import DirAction


class DIREN1(pygame.sprite.Sprite):


    def __init__(self, x, y):
        """
        初始化函数
        :param x: 全局x坐标
        :param y: 全局y坐标
        """
        pygame.sprite.Sprite.__init__(self)  # 调用基类构造函数
        self.walk = DirAction("diren\\station", "", 4, 4, True)
        self.width = 90
        self.height = 111
        self.speed = 5  # x、y方向同一速度
        self.dir = 0  # 方向
        self.step_count = 0  # 记步
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.stop = False

    def draw(self, surface, x, y):
        """
        绘制函数
        :param surface: 背景
        :param x: 窗口x坐标
        :param y: 窗口y坐标
        :return:
        """
        image = self.walk.get_current_image(self.dir)

        image = pygame.transform.scale(image, (180, 216))
        surface.blit(image, (self.pos_x - x, self.pos_y - y))
        # self.__move__()


    def __move__(self):
        if self.stop:
            return
        self.step_count += 1
        if self.dir == 0:  # 右下
            self.pos_x += self.speed
            self.pos_y += self.speed
        elif self.dir == 1:  # 左下
            self.pos_x -= self.speed
            self.pos_y += self.speed
        elif self.dir == 2:  # 左上
            self.pos_x -= self.speed
            self.pos_y -= self.speed
        elif self.dir == 3:  # 右上
            self.pos_x += self.speed
            self.pos_y -= self.speed

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        if self.step_count == 25:
            self.step_count = 0
            if self.dir == 0:
                self.dir = 2
            elif self.dir == 2:
                self.dir = 0
            elif self.dir == 1:
                self.dir = 3
            elif self.dir == 3:
                self.dir = 1

    def collide(self, actor):
        if pygame.sprite.collide_rect(self, actor):
            self.stop = True
        else:
            self.stop = False
