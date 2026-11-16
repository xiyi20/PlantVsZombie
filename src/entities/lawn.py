# -*- coding: utf-8 -*-
"""草坪格子。"""
import pygame

from src.core import constants


class Lawn:
    def __init__(self, ctx, x, y, game):
        self.ctx = ctx
        self.game = game
        self.plant = None
        self.x = x
        self.y = y
        self.row = game.row_road[y]
        self.rect = pygame.Rect(x, y, constants.LAWN_WIDTH, constants.LAWN_HEIGHT)

    def get_pos(self):
        return self.x, self.y

    def planting(self, plant_cls, pos):
        def set_plant():
            self.plant = plant_cls(self.ctx, pos, self.game)
            self.game.plants.append(self.plant)
            self.game.plants_inroad[self.row].append(self.plant)
            self.ctx.assets.random_sound('plant').play()

        if not self.plant and plant_cls.get_alone():
            set_plant()
            return True
        if self.plant and self.plant.upgrade_to is plant_cls:
            self.game.plants.remove(self.plant)
            self.game.plants_inroad[self.row].remove(self.plant)
            set_plant()
            return True
        return False

    def eradicate(self):
        if self.plant:
            self.game.plants.remove(self.plant)
            self.game.plants_inroad[self.row].remove(self.plant)
            self.plant = None
