# -*- coding: utf-8 -*-
"""植物卡片。"""
import pygame

from src.core import constants


class Card:
    def __init__(self, ctx, plant, game, x, y=7):
        self.ctx = ctx
        self.plant = plant
        self.game = game
        self.price = plant.get_price()
        self.cool_time = plant.get_cooldown()
        self.cur_time = 0
        self.interval = constants.CARD_HEIGHT / self.cool_time
        self.selected = False
        self.active = False
        self.last_x = None
        self.last_y = None
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        assets = ctx.assets
        self.cool_image = assets.image('mask')
        self.slot_image = pygame.transform.scale(
            assets.image('card_slot'),
            (constants.CARD_WIDTH, constants.CARD_HEIGHT))
        self.thumb_image = pygame.transform.scale(
            assets.anim(plant.anim_key)[0],
            (constants.CARD_IMG_SIZE, constants.CARD_IMG_SIZE))

    def draw(self):
        self.rect = pygame.Rect(
            self.x, self.y, constants.CARD_WIDTH, constants.CARD_HEIGHT)
        screen = self.ctx.screen
        screen.blit(self.slot_image, (self.x, self.y))
        screen.blit(self.thumb_image, (self.x + 4, self.y + 12))
        color = (255, 0, 0) if (self.price > self.game.cur_sun
                                and not self.game.selecting) else (0, 0, 0)
        screen.blit(self.ctx.assets.font('price').render(
            str(self.price), True, color), (self.x + 2, self.y + 55))
        if self.selected:
            screen.blit(self.cool_image, (self.x, self.y + 1))
        if self.cur_time != 0:
            screen.blit(pygame.transform.scale(
                self.cool_image,
                (constants.CARD_WIDTH, int(self.cur_time * self.interval))),
                (self.x, self.y))
            self.cur_time -= 1
