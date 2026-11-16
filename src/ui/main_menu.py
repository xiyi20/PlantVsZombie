# -*- coding: utf-8 -*-
"""主菜单 + 加载界面 + 改名界面。"""
import sys

import pygame
from pygame.locals import K_a, K_z


class MainMenu:
    def __init__(self, ctx, game, menu):
        self.ctx = ctx
        self.game = game
        self.menu = menu
        assets = ctx.assets
        self.seller = None  # 由 App 注入 Shop 实例
        self.loading = True
        self.load = 250
        self.angle = 0

        # 加载界面
        self.title_screen = assets.image('title_screen')
        self.popcap = pygame.transform.scale(assets.image('popcap_logo'), (150, 150))
        self.pvz_logo = assets.image('pvz_logo')
        self.load_bar_dirt = assets.image('load_bar_dirt')
        self.load_bar_grass = assets.image('load_bar_grass')
        self.sod_roll_cap = assets.image('sod_roll_cap')

        # 主界面
        self.center = assets.image('main_center')
        self.bg = pygame.transform.scale(assets.image('main_bg'), (800, 600))
        self.left = assets.image('main_left')
        self.right = assets.image('main_right')
        self.hello = assets.image('wood_sign1')
        self.save0 = assets.image('wood_sign2')
        self.save1 = assets.image('wood_sign2_press')
        self.save = self.save1
        self.save_rect = self.save1.get_rect(topleft=(20, 135))
        self.grass = assets.image('leaves')
        self.leaf1 = assets.image('leaf1')
        self.leaf2 = assets.image('leaf2')
        self.leaf3 = assets.image('leaf3')
        self.leaf4 = assets.image('leaf4')
        self.flower1 = assets.image('flower1')
        self.flower2 = assets.image('flower2')
        self.flower3 = assets.image('flower3')
        self.help0 = assets.image('help0')
        self.help1 = assets.image('help1')
        self.help = self.help0
        self.help_rect = self.help0.get_rect(topleft=(648, 525))
        self.option0 = assets.image('option0')
        self.option1 = assets.image('option1')
        self.option = self.option0
        self.option_rect = self.option0.get_rect(topleft=(563, 487))
        self.exit0 = assets.image('exit0')
        self.exit1 = assets.image('exit1')
        self.exit = self.exit0
        self.exit_rect = self.exit0.get_rect(topleft=(720, 515))
        self.rename_img = assets.image('rename')

        # 游戏模式按钮
        self.adventure0 = assets.image('adventure0')
        self.adventure1 = assets.image('adventure1')
        self.adventure = self.adventure0
        self.adventure_rect = pygame.Rect(
            404, 55, self.adventure.get_width(), self.adventure.get_height() - 25)
        self.small0 = assets.image('small0')
        self.small1 = assets.image('small1')
        self.small = self.small0
        self.small_rect = pygame.Rect(
            405, 185, self.small.get_width(), self.small.get_height() - 50)
        self.challenge0 = assets.image('challenge0')
        self.challenge1 = assets.image('challenge1')
        self.challenge = self.challenge0
        self.challenge_rect = pygame.Rect(
            412, 275, self.challenge.get_width(), self.challenge.get_height() - 45)
        self.survival0 = assets.image('survival0')
        self.survival1 = assets.image('survival1')
        self.survival = self.survival0
        self.survival_rect = pygame.Rect(
            450, 340, self.survival.get_width(), self.survival.get_height() - 45)
        self.shop0 = assets.image('shop0')
        self.shop1 = assets.image('shop1')
        self.shop = self.shop0
        self.shop_rect = self.shop.get_rect(topleft=(400, 480))

        # 帮助界面
        self.help_flag = True
        self.words = assets.image('says')
        self.words_bg = pygame.transform.scale(assets.image('says_bg'), (800, 600))
        self.back_menu0 = assets.image('back_menu0')
        self.back_menu1 = assets.image('back_menu1')
        self.back_menu = self.back_menu0
        self.back_menu_rect = self.back_menu0.get_rect(topleft=(322, 520))

        # 用户信息
        self.naming = True
        self.name = ctx.config.name
        self.typing = self.name
        self.confirm_rect = pygame.Rect(190, 331, 204, 44)
        self.cancel_rect = pygame.Rect(410, 331, 204, 44)
        self.running = True

    def play_music(self):
        self.ctx.assets.sound('main_menu_bgm').play(-1)
        self.ctx.assets.sound('main_menu_bgm').set_volume(self.ctx.config.menu_volume)

    def run(self):
        """启动流程：加载画面 → 主菜单循环。"""
        ctx = self.ctx
        self.play_music()

        def update_loading():
            ctx.screen.blits([
                (self.title_screen, (0, 0)),
                (self.pvz_logo, (60, 30)),
                (self.popcap, (-10, -10)),
                (self.load_bar_dirt, ((800 - self.load_bar_dirt.get_width()) // 2, 500)),
                (self.load_bar_grass, ((800 - self.load_bar_grass.get_width()) // 2, 480)),
            ])

        while self.loading and self.load <= 533:
            update_loading()
            ctx.screen.blit(ctx.assets.font('menu').render(
                '请等待加载', True, (255, 215, 0)), (345, 510))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in (pygame.KEYUP, pygame.MOUSEBUTTONUP):
                    self.loading = False
                    break
            roll_cap = pygame.transform.rotate(self.sod_roll_cap, self.angle)
            new_rect = roll_cap.get_rect(center=(self.load, 470))
            ctx.screen.blit(roll_cap, new_rect.topleft)
            self.angle -= 0.3
            self.load += 0.2
            pygame.display.flip()
        update_loading()
        ctx.screen.blit(ctx.assets.font('menu').render(
            '任意操作以开始游戏', True, (255, 215, 0)), (295, 510))
        pygame.display.flip()
        while not pygame.event.get():
            pass
        self.draw()

    def _update(self):
        ctx = self.ctx
        ctx.screen.blits([
            (self.bg, (0, 0)),
            (self.center, (90, 270)),
            (self.left, (0, -70)),
            (self.right, (70, 40)),
            (self.hello, (20, 0)),
            (self.save, (20, 135)),
            (self.grass, (0, 538)),
            (self.leaf1, (220, 562)),
            (self.leaf3, (255, 550)),
            (self.leaf2, (248, 572)),
            (self.leaf4, (287, 565)),
            (ctx.assets.font('menu').render(
                self.name, True, (255, 215, 0)), (150, 90)),
        ])
        ctx.screen.blits([
            (self.adventure, (405, 55)),
            (self.small, (405, 168)),
            (self.challenge, (412, 255)),
            (self.survival, (410, 325)),
            (self.shop, (400, 480)),
            (self.flower1, (682, 415)),
            (self.flower2, (637, 435)),
            (self.flower3, (735, 457)),
            (self.option, (563, 487)),
            (self.help, (648, 525)),
            (self.exit, (720, 515)),
        ])

    def _click(self, mode):
        ctx = self.ctx
        val = self.name if mode == 0 else self.typing
        if not val:
            ctx.assets.sound('invalid').play()
            return False
        ctx.assets.sound('dave_click').play()
        return True

    def set_name(self):
        ctx = self.ctx
        self.naming = True
        while self.naming:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    length = len(self.typing)
                    if event.key == 8 and length > 0:
                        self.typing = self.typing[:-1]
                    elif event.key in range(K_a, K_z + 1) and length <= 10:
                        self.typing += chr(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirm_rect.collidepoint(event.pos):
                        if self._click(1):
                            ctx.config.save('user', 'name', self.typing)
                            self.name = self.typing
                            self.naming = False
                    elif self.cancel_rect.collidepoint(event.pos):
                        if self._click(0):
                            self.typing = self.name
                            self.naming = False
                ctx.screen.blits([
                    (self.rename_img, (154, 104)),
                    (pygame.transform.scale(ctx.assets.image('menu_button'), (204, 44)), (190, 331)),
                    (pygame.transform.scale(ctx.assets.image('menu_button'), (204, 44)), (410, 331)),
                    (ctx.assets.font('menu').render('确定', True, (0, 255, 0)), (270, 340)),
                    (ctx.assets.font('menu').render('取消', True, (0, 255, 0)), (490, 340)),
                    (ctx.assets.font('menu').render(self.typing, True, (255, 215, 0)), (205, 256)),
                ])
                pygame.display.flip()

    def update_button(self, rect, state, default, hover, pos):
        if rect.collidepoint(pos):
            if state == default:
                self.ctx.assets.sound('dave_click').play()
            return hover
        return default

    def helper(self):
        ctx = self.ctx
        self.help_flag = True
        ctx.assets.sound('paper').play()
        while self.help_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_menu_rect.collidepoint(event.pos):
                        self.help_flag = False
                else:
                    if event.type == pygame.MOUSEMOTION:
                        self.back_menu = self.update_button(
                            self.back_menu_rect, self.back_menu,
                            self.back_menu0, self.back_menu1, event.pos)
                    ctx.screen.blits([
                        (self.words_bg, (0, 0)),
                        (self.words, (85, 80)),
                        (self.back_menu, (322, 520)),
                        (ctx.assets.font('menu').render(
                            '返回主页', True, (255, 215, 0)), (355, 528)),
                    ])
                    pygame.display.flip()

    def draw(self):
        ctx = self.ctx
        self.running = True
        while self.running:
            self._update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.adventure = self.update_button(
                        self.adventure_rect, self.adventure,
                        self.adventure0, self.adventure1, event.pos)
                    self.small = self.update_button(
                        self.small_rect, self.small,
                        self.small0, self.small1, event.pos)
                    self.challenge = self.update_button(
                        self.challenge_rect, self.challenge,
                        self.challenge0, self.challenge1, event.pos)
                    self.survival = self.update_button(
                        self.survival_rect, self.survival,
                        self.survival0, self.survival1, event.pos)
                    self.option = self.update_button(
                        self.option_rect, self.option,
                        self.option0, self.option1, event.pos)
                    self.help = self.update_button(
                        self.help_rect, self.help,
                        self.help0, self.help1, event.pos)
                    self.exit = self.update_button(
                        self.exit_rect, self.exit,
                        self.exit0, self.exit1, event.pos)
                    self.save = self.update_button(
                        self.save_rect, self.save,
                        self.save0, self.save1, event.pos)
                    self.shop = self.update_button(
                        self.shop_rect, self.shop,
                        self.shop0, self.shop1, event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.adventure_rect.collidepoint(event.pos):
                        self.game.reset()
                        self.game.run()
                    if self.survival_rect.collidepoint(event.pos):
                        self.game.running = True
                        if not self.game.started:
                            self.game.reset()
                        self.game.run(loop=True)
                    elif self.save_rect.collidepoint(event.pos):
                        ctx.assets.sound('menu_click').play()
                        self.set_name()
                    elif self.shop_rect.collidepoint(event.pos):
                        ctx.assets.sound('menu_click').play()
                        self.seller.open()
                    elif self.exit_rect.collidepoint(event.pos):
                        ctx.assets.sound('menu_click').play()
                        pygame.quit()
                        sys.exit()
                    elif self.help_rect.collidepoint(event.pos):
                        ctx.assets.sound('menu_click').play()
                        self.helper()
                    elif self.option_rect.collidepoint(event.pos):
                        ctx.assets.sound('menu_click').play()
                        self.menu.open()
                if self.name == '':
                    self.set_name()
            pygame.display.flip()
