# -*- coding: utf-8 -*-
"""应用装配：初始化 pygame、资源与各界面对象，启动主菜单。"""
import pygame

from src.core import constants
from src.core.config import AppConfig
from src.core.context import GameContext
from src.core.resources import AssetManager, BASE_DIR
from src.game import Game
from src.ui.main_menu import MainMenu
from src.ui.menu import Menu
from src.ui.shop import Shop


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption(constants.CAPTION)
    clock = pygame.time.Clock()

    assets = AssetManager()
    assets.load_all()
    pygame.display.set_icon(assets.image('icon'))

    config = AppConfig(BASE_DIR / 'config.json')
    ctx = GameContext(assets, config, screen, clock)

    game = Game(ctx)
    menu = Menu(ctx, game)
    main_menu = MainMenu(ctx, game, menu)
    main_menu.seller = Shop(ctx)
    game.menu = menu
    game.main_menu = main_menu

    main_menu.run()


if __name__ == '__main__':
    main()
