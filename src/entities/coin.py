# -*- coding: utf-8 -*-
"""金币、银币、钻石。"""
import pygame

from src.core import constants


class Coin:
    def __init__(self, ctx, x, y, game, coin_type=0):
        self.ctx = ctx
        self.x = x
        self.y = y
        self.val = 50
        self.pick = False
        self.first = True
        self.x_speed = 0
        self.y_speed = 0
        self.game = game
        self.tick = 0
        self.fall_sound = (
            ctx.assets.sound('coin_fall') if coin_type == 0
            else ctx.assets.sound('diamond_fall')
        )
        self.pick_sound = ctx.assets.sound('coin_pick')
        self.image = ctx.assets.image('coin_silver')
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.end_rect = pygame.Rect(48, 580, 20, 20)
        self.fall_sound.play()

    def draw(self):
        if self.pick:
            if self.first:
                self.first = False
                self.pick_sound.play()
                self.x_speed = (10 - self.x) / constants.COIN_SPEED
                self.y_speed = (580 - self.y) / constants.COIN_SPEED
            self.x += self.x_speed
            self.y += self.y_speed
            if self.rect.colliderect(self.end_rect):
                self.pickup()
        self.tick += 1
        self.ctx.screen.blit(self.image, (self.x, self.y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.tick == constants.COIN_LIFE:
            self.game.coins.remove(self)

    def pickup(self):
        self.game.money += self.val
        self.ctx.config.save('user', 'money', self.game.money)
        self.game.coins.remove(self)


class SilverCoin(Coin):
    pass


class GoldCoin(Coin):
    def __init__(self, ctx, x, y, game):
        super().__init__(ctx, x, y, game)
        self.val = 100
        self.image = ctx.assets.image('coin_gold')


class Diamond(Coin):
    def __init__(self, ctx, x, y, game):
        super().__init__(ctx, x, y, game, coin_type=1)
        self.val = 300
        self.pick_sound = ctx.assets.sound('diamond_pick')
        self.image = ctx.assets.image('diamond')
