# -*- coding: utf-8 -*-
"""运行时上下文：把资源、配置、屏幕、时钟集中传递给游戏对象与实体。"""
from dataclasses import dataclass

import pygame

from src.core.config import AppConfig
from src.core.resources import AssetManager


@dataclass
class GameContext:
    assets: AssetManager
    config: AppConfig
    screen: pygame.Surface
    clock: pygame.time.Clock
