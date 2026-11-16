# -*- coding: utf-8 -*-
"""游戏主场景：波次推进、种植/铲除交互、渲染与主循环。"""
import random
import sys

import pygame

from src.core import constants
from src.entities.card import Card
from src.entities.car import Car
from src.entities.coin import GoldCoin
from src.entities.lawn import Lawn
from src.entities.plants import DEFAULT_PLANTS, PLANT_REGISTRY
from src.entities.sun import Sun
from src.entities.zombies import (
    NormalZombie, ConeheadZombie, BucketheadZombie, FootballZombie,
)

ERADICATE = 'eradicate'


class Game:
    def __init__(self, ctx):
        self.ctx = ctx
        self.menu = None        # 由 App 注入
        self.main_menu = None   # 由 App 注入
        assets = ctx.assets
        self.background = pygame.transform.scale(
            assets.image('bg_day'), (1400, 600))
        self.moneybag = assets.image('moneybag')
        self.moneybag_rect = None
        self.plant_shop = assets.image('plant_shop')
        self.shovel_slot = assets.image('shovel_slot')
        self.shovel = assets.image('shovel')
        self.menu_button = assets.image('menu_button')
        self.menu_rect = self.menu_button.get_rect(topleft=(680, 0))
        self.progress1 = assets.image('progress_level')
        self.progress2 = pygame.transform.scale(
            assets.image('progress_empty'), (175, 30))
        self.progress_flag1 = assets.image('progress_flag1')
        self.progress_flag2 = assets.image('progress_flag2')
        self.seedchooser_bg = pygame.transform.scale(
            assets.image('seedchooser_bg'), (475, 513))
        self.seedchooser_btn = assets.image('seedchooser_btn')
        self.coin_bank = assets.image('coin_bank')
        self.end_rect = pygame.Rect(310, 241, 40, 40)
        self.shovel_pos = (447, -3)
        self.plant_pos = (-100, -100)
        self.col_road = constants.COL_ROAD
        self.row_road = constants.ROW_ROAD
        self.zombie_road = constants.ZOMBIE_ROAD
        self.reset()

    def reset(self):
        """重置一局的所有状态（原 init）。"""
        ctx = self.ctx
        ctx.config.load()
        self.money = ctx.config.money
        self.first = True
        self.tick = 0
        self.cur_sun = 25
        self.running = True
        self.selecting = True
        self.started = False
        self.animation = False
        self.alpha = 0
        self.won = False
        self.won_flag = False
        self.won_pos = [550, 350]
        self.zombie_rule = {}
        self.zombie_types = [NormalZombie]
        self.zombie_time = dict(constants.ZOMBIE_TIME)
        self.wave = 0
        self.last_wave = -1
        self.waves = list(self.zombie_time.keys())
        self.cur_score = 0
        self.end_score = sum(self.zombie_time.values())
        self.shovel_active = False
        self.cur_plant = None
        self.last_card = None
        self.loop = False
        self.paused = False
        self.zombies_inroad = {i: [] for i in range(1, 6)}
        self.plants_inroad = {i: [] for i in range(1, 6)}
        self.cards = []
        self.peas = []
        self.lawns = [[Lawn(ctx, 20 + constants.LAWN_WIDTH * x,
                            95 + constants.LAWN_HEIGHT * y, self)
                       for x in range(9)] for y in range(5)]
        self.plants = []
        self.suns = []
        self.zombies = []
        self.cars = [Car(ctx, -30, y + 35, self) for y in self.row_road.keys()]
        self.coins = []
        # 可选卡：默认植物 + 已购买的道具植物
        self.plant_cards = {cls.__name__: cls for cls in DEFAULT_PLANTS}
        for key, prop in ctx.config.prop.items():
            if prop['state'] == 0:
                self.plant_cards[key] = PLANT_REGISTRY[key]

    # ---------- 选卡界面 ----------
    def select_plant(self):
        ctx = self.ctx
        cur_cards = 0
        pygame.mixer.music.load(ctx.assets.bgm_choose)
        pygame.mixer.music.play(-1)
        self.cards = []
        col, row = 0, 0
        for plant_cls in self.plant_cards.values():
            if col == 9:
                row += 1
            self.cards.append(Card(
                ctx, plant_cls, self, 13 + 50 * (col % 9), 122 + 72 * row))
            col += 1
        self.selecting = True
        self.update()
        while self.selecting:
            ctx.screen.blits([
                (self.background, (-220, 0)),
                (self.plant_shop, (10, 0)),
                (self.seedchooser_bg, (0, 87)),
                (self.seedchooser_btn, (300, 550)),
                (ctx.assets.font('score').render(
                    str(self.cur_sun), True, (0, 0, 0)), (26, 62)),
                (ctx.assets.font('menu').render(
                    '一起摇滚吧!', True, (255, 215, 0)), (320, 558)),
            ])
            for card in self.cards:
                card.draw()
            self.hover()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            if card.active:
                                card.x = card.last_x
                                card.y = card.last_y
                                card.active = False
                                cur_cards -= 1
                                cur = 0
                                for cur_card in self.cards:
                                    if cur_card.y == 7:
                                        cur_card.x = 90 + 50 * cur
                                        cur += 1
                            elif not card.active and cur_cards < 7:
                                card.last_x = card.x
                                card.last_y = card.y
                                card.x = 90 + 50 * cur_cards
                                card.y = 7
                                card.active = True
                                cur_cards += 1
                            else:
                                ctx.assets.sound('invalid').play()
                            break
                    if pygame.Rect(320, 558, 156, 42).collidepoint(event.pos):
                        self.cards = [c for c in self.cards if c.y == 7]
                        self.selecting = False
                        self.paused = False

    # ---------- 胜利流程 ----------
    def win(self):
        ctx = self.ctx
        if self.animation:
            mask = pygame.Surface(
                (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            mask.set_alpha(self.alpha)
            mask.fill((255, 255, 255))
            ctx.screen.blit(mask, (0, 0))
            self.alpha += 2
            if self.alpha > 255:
                self.running = False
                self.main_menu.play_music()
                self.main_menu.draw()
        else:
            if self.won_flag:
                self.won_pos[0] += (310 - self.won_pos[0]) / 100
                self.won_pos[1] += (241 - self.won_pos[1]) / 100
            ctx.screen.blit(self.moneybag, self.won_pos)
            self.moneybag_rect = self.moneybag.get_rect(topleft=self.won_pos)
            if self.moneybag_rect.colliderect(self.end_rect):
                y_pos = [0, 1, 2, 1, 0]
                for i in range(5):
                    coin = GoldCoin(ctx, self.won_pos[0] - 55 + 45 * i,
                                    self.won_pos[1] - 18 * y_pos[i], self)
                    coin.pick = True
                    self.coins.append(coin)
                self.started = False
                self.animation = True

    # ---------- 渲染 ----------
    def update(self):
        ctx = self.ctx
        assets = ctx.assets
        ctx.screen.blits([
            (self.background, (-220, 0)),
            (self.plant_shop, (10, 0)),
            (self.shovel_slot, (456, 0)),
            (self.menu_button, (680, 0)),
            (assets.font('score').render(
                str(self.cur_sun), True, (0, 0, 0)), (26, 62)),
            (assets.font('menu').render(
                '菜单', True, (0, 255, 0)), (717, 12)),
            (self.progress2, (600, 570)),
            (self.progress1, (645, 568)),
            (self.progress_flag2, (605, 577)),
            (self.progress_flag1, (748, 575)),
            (assets.font('wave').render(
                '第 ' + str(self.wave) + ' 波', True, (0, 216, 0)), (670, 579)),
        ])
        shovel_pos = self.shovel_pos if self.shovel_active else (447, -3)
        for car in self.cars:
            car.draw()
        ctx.screen.blit(self.coin_bank, (35, 570))
        ctx.screen.blit(assets.font('score').render(
            str(self.money), True, (255, 215, 0)), (80, 578))
        for card in self.cards:
            card.draw()
        for plant in self.plants:
            plant.draw()
        for i in range(1, 6):
            for zombie in self.zombies_inroad[i]:
                zombie.draw()
        for sun in self.suns:
            sun.draw()
        for pea in self.peas:
            pea.draw()
        for coin in self.coins:
            coin.draw()
        ctx.screen.blit(self.shovel, shovel_pos)
        if self.cur_plant and self.cur_plant != ERADICATE:
            ctx.screen.blit(
                assets.anim(self.cur_plant.anim_key)[0], self.plant_pos)

    # ---------- 逻辑推进 ----------
    def logical(self):
        ctx = self.ctx
        assets = ctx.assets
        # 波次变化：解锁新僵尸类型；无尽模式第 20 波重新选卡
        if self.wave != self.last_wave:
            self.last_wave = self.wave
            if self.wave == 2:
                self.zombie_types.append(ConeheadZombie)
            elif self.wave == 4:
                self.zombie_types.append(BucketheadZombie)
            elif self.wave == 7:
                self.zombie_types.append(FootballZombie)
            elif self.wave == 20:
                self.paused = True
                self.select_plant()
        if self.tick in self.zombie_time:
            self.wave += 1
            interval = 180 if self.tick < 15000 else 90
            if self.tick == self.waves[-1] and self.loop:
                self.waves.append(self.waves[-1] + 4800)
                self.zombie_time[self.waves[-1]] = 30
            for i in range(self.zombie_time[self.tick]):
                self.zombie_rule[self.tick + interval * i] = 1
        if self.tick in self.zombie_rule:
            if self.first:
                assets.sound('zombie_coming').play()
                self.first = False
            zombie_cls = random.choice(self.zombie_types)
            self.zombies.append(zombie_cls(
                ctx, 20 + 96 * random.randint(0, 4), self))
        if self.tick % 1200 == 0:
            self.suns.append(Sun(
                ctx, 50, (random.randrange(60, 750), random.randrange(50, 450)),
                self, falling=True))
        if self.zombies and random.randrange(1000) == 0:
            assets.random_sound('zombie_groan').play()
        # 胜利
        if self.cur_score == self.end_score and not self.loop:
            self.won = True
        # 失败
        for zombie in self.zombies:
            if zombie.x <= -120:
                pygame.mixer.music.pause()
                self.paused = True
                for sound in assets.group('zombie_eat'):
                    sound.play()
                for sound in assets.group('lose'):
                    sound.play()
                lose = assets.image('lose')
                ctx.screen.blit(pygame.transform.scale(
                    assets.image('mask'),
                    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)), (0, 0))
                ctx.screen.blit(lose, (
                    (ctx.screen.get_width() - lose.get_width()) / 2,
                    (ctx.screen.get_height() - lose.get_height()) / 2))

    def hover(self):
        ctx = self.ctx
        pos = pygame.mouse.get_pos()
        for card in self.cards:
            if card.rect.collidepoint(pos):
                color = (0, 0, 0) if (card.cur_time == 0 and
                                      self.cur_sun >= card.plant.get_price()) \
                    or self.selecting else (255, 0, 0)
                pos = (card.x, card.y + 71)
                text_surface = ctx.assets.font('hover').render(
                    card.plant.get_name(), True, color)
                text_rect = text_surface.get_rect(topleft=pos)
                pygame.draw.rect(ctx.screen, (252, 235, 98), text_rect)
                ctx.screen.blit(text_surface, pos)
                break

    def play_music(self):
        pygame.mixer.music.load(self.ctx.assets.random_bgm())
        pygame.mixer.music.set_volume(self.ctx.config.game_volume)
        pygame.mixer.music.play(-1)

    # ---------- 主循环 ----------
    def run(self, loop=False):
        ctx = self.ctx
        assets = ctx.assets
        self.loop = loop
        assets.sound('main_menu_bgm').stop()
        self.started = True
        if self.selecting:
            self.select_plant()
        assets.sound('ready_set_plant').play()
        for img in assets.anim('ready_set_plant'):
            self.update()
            ctx.screen.blit(img, ((800 - img.get_width()) / 2,
                                  (600 - img.get_height()) / 2))
            pygame.display.flip()
            pygame.time.wait(500)
        self.play_music()
        while self.running:
            if not self.paused:
                self.update()
                self.hover()
                self.logical()
                if self.won:
                    self.win()
                self.tick += 1
            for event in pygame.event.get():
                if not self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self._handle_left_click(event.pos)
                        elif event.button == 3:
                            self._handle_right_click(event.pos)
                    elif event.type == pygame.MOUSEMOTION:
                        if self.cur_plant and self.cur_plant != ERADICATE:
                            self.plant_pos = (event.pos[0] - 30, event.pos[1] - 40)
                        else:
                            self.plant_pos = (-100, -100)
                        if self.shovel_active:
                            self.shovel_pos = (event.pos[0] - 30, event.pos[1] - 40)
                        else:
                            self.shovel_pos = (463, 9)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu.open()
            pygame.display.flip()
            ctx.clock.tick(60)

    def _handle_left_click(self, pos):
        ctx = self.ctx
        assets = ctx.assets
        for sun in self.suns:
            if sun.rect.collidepoint(pos):
                sun.pick = True
                assets.sound('pickup').play()
                break
        for coin in self.coins:
            if coin.rect.collidepoint(pos):
                coin.pick = True
                break
        if self.won and self.moneybag_rect and \
                self.moneybag_rect.collidepoint(pos):
            self.won_flag = True
            pygame.mixer.music.stop()
            assets.sound('win').play()
        if self.shovel.get_rect(topleft=(464, 9)).collidepoint(pos):
            if self.last_card:
                self.last_card.selected = False
            self.cur_plant = ERADICATE
            assets.sound('shovel').play()
            self.shovel_active = True
        elif self.menu_rect.collidepoint(pos):
            self.menu.open()
        for card in self.cards:
            if card.rect.collidepoint(pos):
                if self.cur_sun >= card.price and card.cur_time == 0:
                    if card.selected:
                        self.last_card = None
                        card.selected = False
                        self.cur_plant = None
                    else:
                        if self.last_card:
                            self.last_card.selected = False
                        assets.sound('plant_slot').play()
                        card.selected = True
                        self.last_card = card
                        self.cur_plant = card.plant
                else:
                    assets.sound('invalid').play()
                break
        for row in self.lawns:
            for lawn in row:
                x, y = lawn.get_pos()
                p = self.lawns[self.row_road[y] - 1][self.col_road[x] - 1]
                if not lawn.rect.collidepoint(pos):
                    continue
                if self.cur_plant == ERADICATE and p.plant:
                    if p.plant.sun_price != 0:
                        self.suns.append(
                            Sun(ctx, p.plant.sun_price // 2, (x, y), self))
                    p.eradicate()
                    assets.random_sound('plant').play()
                    self.shovel_active = False
                    self.cur_plant = None
                elif self.cur_plant == ERADICATE:
                    self.shovel_active = False
                    self.cur_plant = None
                elif self.cur_plant and self.cur_plant != ERADICATE and \
                        self.last_card.cur_time == 0 and \
                        self.cur_sun >= self.cur_plant.get_price():
                    if lawn.planting(self.cur_plant, (x, y)):
                        self.cur_sun -= self.cur_plant.get_price()
                        self.cur_plant = None
                        self.last_card.cur_time = self.last_card.cool_time
                        self.last_card.selected = False
                break

    def _handle_right_click(self, pos):
        for zombie in self.zombies:
            if zombie.rect.collidepoint(pos):
                zombie.dead = 1
        if self.cur_plant == ERADICATE and self.shovel_active:
            self.shovel_active = False
            self.cur_plant = None
