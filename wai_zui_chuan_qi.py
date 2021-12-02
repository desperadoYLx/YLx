"""
主函数
初始化pygame
运行场景
退出pygame
"""
import sys

import pygame
from actor.xiao import XIAO
from scene import SceneResult
from scene.dierdian_secne import DIERDIAN
from scene.qishidian_scene import QishidianScene
from scene.disandian_secne import DISANDIAN
from scene.zhongmu_secne import ZHONGMU
from scene.win_fail_scene import WinFailScene
from scene.kaishi1_scene import Kaishi1Scene

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1100, 750),0, 32)
    # pygame.FULLSCREEN
    pygame.display.set_caption('歪嘴传奇')
    xiao = XIAO()

    game_list = ['QishidianScene', 'DIERDIAN','DISANDIAN','ZHONGMU']
    # 'QishidianScene', 'DIERDIAN','DISANDIAN','ZHONGMU'
    for item in game_list:
        item_scene = globals()[item](screen, xiao)
        item_scene.run()
        if item_scene.scene_result == SceneResult.Fail:
            final_result = SceneResult.Fail
            break
        if item_scene.scene_result == SceneResult.Win:
            final_result = SceneResult.Win
            break
        if item_scene.scene_result == SceneResult.Quit:
            final_result = SceneResult.Fail
            break
        # if item_scene.scene_result == SceneResult.Next:
        #     item_scene = globals()['Kaishi1Scene'](screen, xiao)
        #     item_scene.run()
        #     final_result = SceneResult.Ongoing
        #     break
    win_fail_scene = WinFailScene(final_result)
    win_fail_scene.run(screen)
    # #第一个场景
    # village_scene = VillageScene(screen, swk)
    # village_scene.run()
    # #第二个场景
    # temple_scene = TempleScene(screen, swk)
    # temple_scene.run()
    # pygame.quit()
    # sys.exit()
    #
    # village_scene = QishidianScene(screen)
    # village_scene.run()
    #
    # #第二个场景
    # temple_scene = DIERDIAN(screen, xiao)
    # temple_scene.run()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
