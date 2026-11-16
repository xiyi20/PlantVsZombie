# -*- coding: utf-8 -*-
"""游戏内暂停/选项菜单。"""
import sys

import pygame

from src.core import constants


class Menu:
    def __init__(self, ctx, game):
        self.ctx = ctx
        self.game = game
        assets = ctx.assets
        self.pause_sound = assets.sound('pause')
        self.panel = assets.image('options_bg')
        self.return_img0 = assets.image('return_btn0')
        self.return_img1 = assets.image('return_btn1')
        self.return_img = self.return_img0
        self.return_img_rect = self.return_img.get_rect(topleft=(220, 432))
        self.slider_slot = assets.image('slider_slot')
        self.pointer = assets.image('slider_knob')
        self.button = pygame.transform.scale(assets.image('menu_button'), (200, 41))
        self.again_rect = pygame.Rect(295, 333, 200, 41)
        self.main_menu_rect = pygame.Rect(295, 375, 200, 41)
        self.running = False
        self.button_down = False
        self.volume_down = False
        self.is_point = False
        self.pointer_rect = None
        self.point_pos = (ctx.config.menu_volume / constants.VOLUME_STEP + 350, 208)

    def _update(self, y=452):
        ctx = self.ctx
        screen = ctx.screen
        screen.blits([
            (self.panel, (188.5, 51)),
            (self.return_img, (220, 432)),
            (ctx.assets.font('menu').render(
                '音乐', True, (107, 109, 145)), (300, 210)),
            (self.slider_slot, (350, 218)),
            (self.pointer, self.point_pos),
            (ctx.assets.font('title').render(
                '返回', True, (0, 216, 0)), (350, y)),
        ])
        if self.game.started:
            screen.blits([
                (self.button, (295, 333)),
                (ctx.assets.font('menu').render(
                    '重新开始', True, (0, 216, 0)), (352, 340)),
                (self.button, (295, 375)),
                (ctx.assets.font('menu').render(
                    '主菜单', True, (0, 216, 0)), (365, 383)),
            ])
        self.pointer_rect = self.pointer.get_rect(topleft=self.point_pos)
        pygame.display.flip()

    def open(self):
        """打开菜单并阻塞直到关闭（原 draw）。"""
        ctx = self.ctx
        game = self.game
        self.running = True
        if game.started:
            self.point_pos = (ctx.config.game_volume / constants.VOLUME_STEP + 350, 208)
            self.pause_sound.play()
            game.paused = True
        else:
            self.point_pos = (ctx.config.menu_volume / constants.VOLUME_STEP + 350, 208)
        while self.running:
            self._update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.volume_down = True
                    if self.return_img_rect.collidepoint(event.pos):
                        ctx.assets.sound('button_click').play()
                        self.button_down = True
                        self.return_img = self.return_img1
                        self._update(454)
                    elif self.pointer_rect.collidepoint(event.pos):
                        self.is_point = True
                    elif game.started and self.again_rect.collidepoint(event.pos):
                        game.running = False
                        game.reset()
                        game.run()
                    elif game.started and self.main_menu_rect.collidepoint(event.pos):
                        game.running = False
                        game.started = False
                        pygame.mixer.music.stop()
                        game.main_menu.play_music()
                        game.main_menu.draw()
                    else:
                        self.is_point = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.volume_down = False
                    self.is_point = False
                    if self.return_img_rect.collidepoint(event.pos) and self.button_down:
                        self.running = False
                        self.button_down = False
                        zone = 'game' if game.started else 'menu'
                        if game.started:
                            game.paused = False
                        ctx.config.save(
                            'volume', zone,
                            constants.VOLUME_STEP * (self.point_pos[0] - 350))
                elif event.type == pygame.MOUSEMOTION:
                    if self.volume_down and self.is_point:
                        x = min(max(361, event.pos[0]), 474)
                        self.point_pos = (x - 10, 208)
                self.return_img = self.return_img0
        if not game.started:
            ctx.assets.sound('main_menu_bgm').set_volume(ctx.config.menu_volume)
        else:
            pygame.mixer.music.set_volume(ctx.config.game_volume)
