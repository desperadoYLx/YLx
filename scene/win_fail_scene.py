"""
村庄的场景
"""
import os
import pygame
from pytmx import pytmx

from scene import TiledScene, FadeScene, SceneStatus, SceneResult
from pygame.constants import QUIT, KEYDOWN, K_y


class WinFailScene:
    """
    村庄场景
    """

    def __init__(self, state):
        if state == SceneResult.Win:
            image = pygame.image.load("resource/img/0WIN.png")
            sound_path = os.path.join("resource", "music", "WIN.mp3")
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(1)
        if state == SceneResult.Fail:
            image = pygame.image.load("resource/img/shibai.png")
            sound_path = os.path.join("resource", "music", "lost.mp3")
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(1)
        self.image = pygame.transform.scale(image, (1100, 750))

    def run(self,surface):
        """
        场景的运行
        :return:
        """
        clock = pygame.time.Clock()
        scene_exit = False

        while not scene_exit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    scene_exit = True
            surface.blit(self.image, (0, 0))
            clock.tick(20)
            pygame.display.update()
