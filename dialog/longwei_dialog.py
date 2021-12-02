import os
import pygame

from dialog import blit_text


class LWDialog:
    def __init__(self):
        """
        土地公的对话框构建
        """
        # 1 头像照片
        img_path = os.path.join('resource', 'img', 'longweix', 'LW.png')
        temp_header = pygame.image.load(img_path)
        header_w = temp_header.get_width()
        header_h = temp_header.get_height()
        # 头像缩小一半
        header = pygame.transform.scale(temp_header, (header_w, header_h))
        # 2 对话框图片
        dialog_path = os.path.join('resource', 'img', 'dialog', '0000.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width()
        dialog_h = temp_dialog.get_height()//4
        # 缩小一半
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        # 3 绘制汉字
        font_path = os.path.join('resource', 'font', '鸿雷板书简体-Regular.TTF')
        font = pygame.font.Font(font_path, 21)
        text = " 送龙王大人！！！！！！！" \

        blit_text(dialog, text, (20, 25), font)

        # 4 生成surface并绘制
        if header_h > dialog_h:
            h = header_h
        else:
            h = dialog_h
        w = header_w + dialog_w
        self.surface = pygame.Surface((w, h))  # 黑图片  fill
        # 5 设置关键色，形成透明图片
        self.surface.set_colorkey((0, 0, 0))
        # 6 把头像 对话框绘制上去
        self.surface.blit(header, (0, 0))
        self.surface.blit(dialog, (header_w, 0))

