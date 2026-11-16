# -*- coding: utf-8 -*-
"""实体基类。"""
from src.core.context import GameContext


class Entity:
    def __init__(self, ctx: GameContext) -> None:
        self.ctx = ctx
        self.x = None
        self.y = None
        self.images = None
        self.tick = 0
        self.image_index = 0
        self.destroy_pos = ctx.screen.get_width() - 30

    def draw(self):
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.ctx.screen.blit(self.images[self.image_index], (self.x, self.y + 20))
        self.tick += 1
