"""
场景公用的方法 类
"""
import enum

import pygame

from utils.tiled_render import TiledRenderer


class SceneResult(enum.IntEnum):
    Ongoing = 0
    Next = 1
    Fail = 2
    Win = 3
    Quit = 4
    To = 5


class TiledScene:
    """
    场景渲染类
    """

    def __init__(self, path):
        """
        瓦格场景的构造函数
        :param path: 瓦格文件的路径
        """
        self.tiled_path = path
        self.tiled = TiledRenderer(self.tiled_path)
        self.surface = pygame.Surface(self.tiled.pixel_size)
        self.tiled.render_map(self.surface)


class SceneStatus(enum.IntEnum):
    """
    场景的状态
    """
    In = 1  # 渐入
    Normal = 2  # 正常
    Out = 3  # 渐出


class FadeScene:
    def __init__(self, back_image: pygame.image):
        """
        渐变场景构造函数，back_image是整个背景
        """
        self.back_image = back_image
        self.alpha = 0
        self.status = SceneStatus.In

    def set_status(self, status: SceneStatus):
        """
        设置渐变场景的状态值
        :param status: 状态值
        """
        self.status = status
        if status == SceneStatus.In:
            self.alpha = 0
        if status == SceneStatus.Normal:
            self.alpha = 255
        if status == SceneStatus.Out:
            self.alpha = 0

    def get_out(self):
        if self.status == SceneStatus.Out and self.alpha == 255:
            return True
        else:
            return False

    def get_back_image(self, x: int, y: int):
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > self.back_image.get_width() - 1100:
            x = self.back_image.get_width() - 1100
        if y > self.back_image.get_height() - 750:
            y = self.back_image.get_height() - 750

        temp_surface = self.back_image.subsurface((x, y, 1100, 750))

        if self.status == SceneStatus.Normal:
            return temp_surface
        elif self.status == SceneStatus.In:
            temp_surface.set_alpha(self.alpha)
            black_surface = pygame.Surface((1100, 750))  # black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))  # 参数二为位置信息
            self.alpha += 20
            print(self.alpha)
            if self.alpha >= 255:
                self.alpha = 0
                self.status = SceneStatus.Normal
            return black_surface
        elif self.status == SceneStatus.Out:
            temp_surface.set_alpha(255 - self.alpha)
            black_surface = pygame.Surface((1100, 750))  # black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))  # 参数二为位置信息
            self.alpha += 20
            if self.alpha >= 255:
                self.alpha = 255
            return black_surface
