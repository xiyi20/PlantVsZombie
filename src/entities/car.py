# -*- coding: utf-8 -*-
"""小推车（保命道具）。"""
import pygame

from src.entities.base import Entity


class Car(Entity):
    def __init__(self, ctx, x, y, game):
        super().__init__(ctx)
        self.speed = 4
        self.x = x
        self.y = y
        self.game = game
        self.active = False
        self.can_play = True
        self.image = ctx.assets.image('lawn_mower')
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())

    def draw(self):
        for zombie in self.game.zombies_inroad[self.game.row_road[self.y - 35]]:
            if self.rect.colliderect(zombie.rect):
                zombie.dead = 1
                self.active = True
        if self.active:
            self.x += self.speed
            if self.can_play:
                self.ctx.assets.sound('car').play()
                self.can_play = False
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())
        self.ctx.screen.blit(self.image, (self.x, self.y))
        if self.x >= self.destroy_pos:
            self.game.cars.remove(self)
