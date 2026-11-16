# -*- coding: utf-8 -*-
"""商店：购买道具植物。"""
import sys

import pygame


class Goods:
    def __init__(self, ctx, x, y, gid, name, image_path, price, state):
        self.ctx = ctx
        self.x = x
        self.y = y
        self.gid = gid
        self.name = name
        self.state = state
        self.image = pygame.transform.scale(
            ctx.assets.load_image(image_path), (50, 70))
        self.price = price
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        ctx = self.ctx
        y = self.y + self.image.get_height()
        pygame.draw.rect(ctx.screen, (252, 235, 98), pygame.Rect(
            self.x, y, self.image.get_width() + 10, 20))
        ctx.screen.blits([
            (self.image, (self.x, self.y)),
            (ctx.assets.font('score').render(
                f'${self.price}', True, (0, 0, 0)), (self.x, y + 1)),
        ])
        if not self.state:
            ctx.screen.blit(ctx.assets.image('sold_out'), (self.x - 10, self.y))


class Shop:
    def __init__(self, ctx):
        self.ctx = ctx
        self.running = True
        self.dialog_flag = True
        self.image = ctx.assets.image('shop_bg')
        self.dialog_img = ctx.assets.image('shop_dialog')
        self.dialog_button = ctx.assets.image('menu_button')
        self.main_menu_rect = pygame.Rect(377, 512, 121, 70)
        self.confirm_rect = self.dialog_button.get_rect(topleft=(275, 380))
        self.cancel_rect = self.dialog_button.get_rect(topleft=(415, 380))
        self.goods = []
        col = 0
        for key, prop in ctx.config.prop.items():
            self.goods.append(Goods(
                ctx, 380 + 80 * col, 315, key,
                prop['name'], prop['image'], prop['price'], prop['state']))
            col += 1

    def dialog(self, goods: Goods):
        ctx = self.ctx
        self.dialog_flag = True
        while self.dialog_flag:
            ctx.screen.blits([
                (self.dialog_img, ((800 - self.dialog_img.get_width()) / 2,
                                   (600 - self.dialog_img.get_height()) / 2)),
                (ctx.assets.font('menu').render(
                    f'确定花费{goods.price}$', True, (107, 109, 145)), (300, 240)),
                (ctx.assets.font('menu').render(
                    f'购买{goods.name}吗', True, (107, 109, 145)), (300, 270)),
                (self.dialog_button, (275, 380)),
                (self.dialog_button, (415, 380)),
                (ctx.assets.font('menu').render(
                    '确定', True, (0, 216, 0)), (310, 391)),
                (ctx.assets.font('menu').render(
                    '取消', True, (0, 216, 0)), (450, 391)),
            ])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirm_rect.collidepoint(event.pos):
                        if self.money >= goods.price:
                            goods.state = 0
                            ctx.config.save('user', 'money', self.money - goods.price)
                            ctx.config.save(goods.gid, 'state', 0, prop=True)
                            self.money = ctx.config.money
                            self.dialog_flag = False
                        else:
                            ctx.assets.sound('invalid').play()
                    elif self.cancel_rect.collidepoint(event.pos):
                        self.dialog_flag = False

    def open(self):
        ctx = self.ctx
        ctx.config.load()
        self.money = ctx.config.money
        self.running = True
        while self.running:
            ctx.screen.blits([
                (self.image, (0, 0)),
                (ctx.assets.font('menu').render(
                    '主菜单', True, (105, 152, 217)), (400, 537)),
                (ctx.assets.image('coin_bank'), (650, 560)),
                (ctx.assets.font('score').render(
                    str(self.money), True, (255, 215, 0)), (695, 568)),
            ])
            for goods in self.goods:
                goods.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu_rect.collidepoint(event.pos):
                        self.running = False
                    for goods in self.goods:
                        if goods.rect.collidepoint(event.pos):
                            if goods.state:
                                self.dialog(goods)
                            else:
                                ctx.assets.sound('invalid').play()
                            break
