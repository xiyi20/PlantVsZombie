# -*- coding: utf-8 -*-
"""弹丸：直线豌豆与追踪弹。"""
import math

import pygame

from src.core import constants
from src.entities.base import Entity


class Pea(Entity):
    def __init__(self, ctx, x, y, game, damage=20):
        super().__init__(ctx)
        self.x = x + 35
        self.y = y + 5
        self.game = game
        self.damage = damage
        self.speed = constants.PEA_SPEED
        self.images = ctx.assets.anim('pea')
        self.rect = pygame.Rect(self.x, self.y, 23, 10)
        ctx.assets.random_sound('shoot').play()

    def draw(self):
        if self.tick % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.ctx.screen.blit(self.images[self.image_index], (self.x, self.y))
        self.tick += 1
        self.x += self.speed
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), 10)
        for zombie in self.game.zombies_inroad[self.game.row_road[self.y - 5]]:
            if self.attack(zombie):
                break
        if self.x >= self.destroy_pos and self in self.game.peas:
            self.game.peas.remove(self)

    def attack(self, zombie):
        if zombie.rect.colliderect(self.rect) and zombie.blood > 0:
            zombie.blood -= self.damage
            self.ctx.assets.random_sound(zombie.hit_group).play()
            self.game.peas.remove(self)
            if zombie.blood <= 0:
                zombie.dead = 1
            return True
        return False


class TrackedPea(Pea):
    """猫尾草弹：朝最近的僵尸追踪飞行。"""

    def __init__(self, ctx, x, y, game, damage=20):
        super().__init__(ctx, x, y, game, damage)
        self.speed = 150
        self.sina = 1
        self.cosa = 1

    def draw(self):
        if self.tick % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.ctx.screen.blit(self.images[self.image_index], (self.x, self.y))
        self.tick += 1
        if self.game.zombies:
            target = self.game.zombies[0]
            tx = target.x + 80
            ty = target.y + 85
            distance = math.sqrt((tx - self.x) ** 2 + (ty - self.y) ** 2)
            self.sina = (tx - self.x) / distance
            self.cosa = (ty - self.y) / distance
        self.x += self.speed / 60 * self.sina
        self.y += self.speed / 60 * self.cosa
        self.rect = pygame.Rect(
            self.x, self.y, self.images[0].get_width(), 10)
        for zombie in self.game.zombies:
            if self.attack(zombie):
                break
        if (self.x >= self.destroy_pos or self.y < 0 or self.y > 600) \
                and self in self.game.peas:
            self.game.peas.remove(self)
