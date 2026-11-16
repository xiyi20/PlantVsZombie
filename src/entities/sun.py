# -*- coding: utf-8 -*-
"""阳光实体。"""
import pygame

from src.core import constants
from src.entities.base import Entity


class Sun(Entity):
    def __init__(self, ctx, val, pos, game, falling=False):
        super().__init__(ctx)
        self.val = val
        self.x = pos[0]
        self.y = pos[1]
        self.cur_y = 50
        self.target_y = pos[1]
        self.game = game
        self.falling = falling
        self.life = constants.SUN_LIFE
        self.pick = False
        self.images = ctx.assets.anim('sun')
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        self.end_rect = pygame.Rect(0, 0, 20, 20)

    def draw(self):
        if not self.pick:
            if self.falling and self.tick % 2 == 0 and self.cur_y < self.target_y:
                self.cur_y += 1.5
                self.y = self.cur_y
            else:
                self.y = self.cur_y if self.falling else self.target_y
        else:
            self.x += (-self.x) / constants.SUN_SPEED
            self.y += (-10 - self.y) / constants.SUN_SPEED
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
        if self.rect.colliderect(self.end_rect):
            self.pickup()
        if self.tick % 4 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.tick += 1
        if self.tick == self.life:
            self.game.suns.remove(self)
        self.ctx.screen.blit(self.images[self.image_index], (self.x, self.y + 20))

    def pickup(self):
        self.game.cur_sun += self.val
        self.game.suns.remove(self)
