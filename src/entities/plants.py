# -*- coding: utf-8 -*-
"""植物实体与注册表。"""
import math
import random

import pygame

from src.core import constants
from src.entities.projectile import Pea, TrackedPea
from src.entities.sun import Sun


class Plant:
    sun_price = 0
    cooldown = 450
    alone = True
    anim_key = None        # 动画资源键（首帧即卡面图）
    name = None
    upgrade_to = None      # 升级目标植物类（原 update 字段）

    def __init__(self, ctx, pos, game):
        self.ctx = ctx
        self.game = game
        self.x = pos[0]
        self.y = pos[1]
        self.x_offset = 13
        self.y_offset = 5
        self.fps = 4
        self.images = ctx.assets.anim(self.anim_key)
        self.image_index = 0
        self.blood = 300
        self.col = game.col_road[pos[0]]
        self.row = game.row_road[pos[1]]
        self.rect = pygame.Rect(self.x, self.y, 65, 75)
        self.tick = 0
        self.interval = 80

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_price(cls):
        return cls.sun_price

    @classmethod
    def get_cooldown(cls):
        return cls.cooldown

    @classmethod
    def get_alone(cls):
        return cls.alone

    def check(self):
        """本行是否存在可攻击的僵尸。"""
        for zombie in self.game.zombies_inroad[self.row]:
            if self.x - 30 <= zombie.x <= 700:
                return True
        return False

    def action(self):
        pass

    def switch_img(self):
        if self.tick % self.fps == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        self.ctx.screen.blit(self.images[self.image_index],
                             (self.x + self.x_offset, self.y + self.y_offset))
        self.tick += 1

    def draw(self):
        self.switch_img()
        self.action()

    def hurt(self, damage):
        self.blood -= damage
        self.ctx.assets.random_sound('zombie_eat').play()
        if self.blood < 0:
            self.game.lawns[self.row - 1][self.col - 1].eradicate()
            self.ctx.assets.sound('plant_dead').play()
            return True
        return False


class Sunflower(Plant):
    sun_price = constants.SUNFLOWER_PRICE
    anim_key = 'sunflower'
    name = '向日葵'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.y_offset = 3
        self.spawn_timer = random.randint(180, 720)

    def action(self):
        self.spawn_timer -= 1
        if self.spawn_timer == 0:
            self.game.suns.append(
                Sun(self.ctx, 50, (self.x + 44, self.y + 25), self.game))
            self.spawn_timer = random.randint(1200, 1800)


class PeaShooter(Plant):
    sun_price = constants.PEASHOOTER_PRICE
    anim_key = 'peashooter'
    name = '豌豆射手'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.damage = 20

    def action(self):
        if self.check() and self.tick % self.interval == 0:
            self.game.peas.append(
                Pea(self.ctx, self.x, self.y, self.game, self.damage))


class Repeater(Plant):
    sun_price = constants.REPEATER_PRICE
    anim_key = 'repeater'
    name = '双发射手'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.damage = 20

    def action(self):
        if self.check() and self.tick % self.interval in (0, 10):
            self.game.peas.append(
                Pea(self.ctx, self.x, self.y, self.game, self.damage))


class GatlingPea(Plant):
    sun_price = constants.GATLINGPEA_PRICE
    cooldown = 3000
    alone = False
    anim_key = 'gatling'
    name = '机枪射手'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.y_offset = -5
        self.damage = 20

    def action(self):
        if self.check() and self.tick % self.interval in (0, 10, 20, 30):
            self.game.peas.append(
                Pea(self.ctx, self.x, self.y, self.game, self.damage))


class SpicyChili(Plant):
    sun_price = constants.SPICYCHILI_PRICE
    cooldown = 3000
    anim_key = 'jalapeno'
    name = '火爆辣椒'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.damage = 1800
        self.booming = False
        self.boom_images = ctx.assets.anim('fire')
        self.boom_index = 0

    def draw(self):
        if not self.booming:
            self.ctx.screen.blit(self.images[math.floor(self.image_index)],
                                 (self.x + 10, self.y - 15))
            self.image_index += 0.25
            if self.image_index == len(self.images):
                self.booming = True
                self.ctx.assets.sound('jalapeno').play()
                for zombie in self.game.zombies_inroad[self.row]:
                    if zombie.blood > 0:
                        zombie.blood -= self.damage
                        if zombie.blood <= 0:
                            zombie.die_images = self.ctx.assets.anim('zombie_death_ash')
                            zombie.dead = 2
        else:
            self.ctx.screen.blit(self.boom_images[math.floor(self.boom_index)],
                                 (25, self.y - 40))
            self.boom_index += 0.25
            if self.boom_index == len(self.boom_images):
                self.game.lawns[self.row - 1][self.col - 1].eradicate()


class NutsWall(Plant):
    sun_price = constants.NUTSWALL_PRICE
    cooldown = 1800
    anim_key = 'wallnut'
    name = '坚果'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.blood = 5000


class PotatoMine(Plant):
    sun_price = constants.POTATOMINE_PRICE
    cooldown = 1800
    anim_key = 'potato_armed'
    name = '土豆地雷'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.x = pos[0] + 30
        self.y = pos[1] + 45
        self.damage = 1800
        self.active = False
        self.booming = False
        self.boom_time = 0
        self.boom_image = ctx.assets.image('potato_boom')
        self.mash_image = ctx.assets.image('potato_mash')
        self.underground_images = ctx.assets.anim('potato_underground')
        self.armed_images = ctx.assets.anim('potato_armed')
        self.images = self.underground_images
        self.rect = pygame.Rect(
            pos[0], pos[1],
            self.armed_images[0].get_width(), self.armed_images[0].get_height())

    def draw(self):
        if not self.booming:
            if self.tick % 13 == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            if self.tick == 900:
                self.active = True
                self.ctx.assets.sound('potato_active').play()
                self.x -= 18
                self.y -= 20
                self.images = self.armed_images
            self.ctx.screen.blit(self.images[self.image_index], (self.x, self.y))
            self.tick += 1
            if self.active:
                for zombie in self.game.zombies_inroad[self.row]:
                    if self.rect.colliderect(zombie.rect):
                        self.booming = True
                        self.ctx.assets.sound('potato_boom').play()
                        for target in self.game.zombies_inroad[self.row]:
                            if -45 < target.x - self.x < 45 and target.blood > 0:
                                target.blood -= self.damage
                                if target.blood <= 0:
                                    target.dead_animation = False
                                    target.dead = 1
                        break
        else:
            if self.boom_time <= 60:
                self.ctx.screen.blits([
                    (self.mash_image, (self.x - 30, self.y - 25)),
                    (self.boom_image, (self.x - 45, self.y - 55)),
                ])
                self.boom_time += 1
            else:
                self.game.lawns[self.row - 1][self.col - 1].eradicate()


class CherryBomb(Plant):
    sun_price = constants.CHERRYBOMB_PRICE
    cooldown = 3000
    anim_key = 'cherry'
    name = '樱桃炸弹'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.damage = 1800
        self.booming = False
        self.boom_time = 0
        self.boom_image = ctx.assets.image('cherry_boom')
        self.boom_rect = pygame.Rect(self.x - 70, self.y - 30, 200, 130)

    def draw(self):
        if not self.booming:
            self.ctx.screen.blit(self.images[math.floor(self.image_index)],
                                 (self.x - 10, self.y - 5))
            self.image_index += 0.25
            if self.image_index == len(self.images):
                self.booming = True
                self.ctx.assets.sound('cherry_boom').play()
                for zombie in self.game.zombies:
                    if self.boom_rect.colliderect(zombie.rect) and zombie.blood > 0:
                        zombie.blood -= self.damage
                        if zombie.blood <= 0:
                            zombie.die_images = self.ctx.assets.anim('zombie_death_ash')
                            zombie.dead = 2
        else:
            if self.boom_time <= 30:
                self.ctx.screen.blit(self.boom_image, (self.x - 70, self.y - 30))
                self.boom_time += 1
            else:
                self.game.lawns[self.row - 1][self.col - 1].eradicate()


class Torchwood(Plant):
    sun_price = constants.TORCHWOOD_PRICE
    anim_key = 'torchwood'
    name = '火炬树桩'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.x_offset = 16
        self.y_offset = -10
        self.fire_pea_images = ctx.assets.anim('fire_pea')
        self.rect = pygame.Rect(self.x + 20, self.y, 55, 80)

    def action(self):
        for pea in self.game.peas:
            if self.rect.colliderect(pea.rect):
                pea.damage = 65
                pea.images = self.fire_pea_images


class Catnip(Plant):
    sun_price = constants.CATNIP_PRICE
    cooldown = 3000
    anim_key = 'catnip_normal'
    name = '猫尾草'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.fps = 7
        self.x_offset = -10
        self.damage = 20
        self.shoot_images = [ctx.assets.image('thorn')]

    def check(self):
        """返回第一个可攻击的僵尸（跨行追踪）。"""
        for zombie in self.game.zombies:
            if zombie.x <= 700:
                return zombie
        return None

    def action(self):
        if self.check() and self.tick % self.interval in (0, 10):
            pea = TrackedPea(self.ctx, self.x - 15, self.y - 5,
                             self.game, self.damage)
            pea.images = self.shoot_images
            self.game.peas.append(pea)


class FireCatnip(Catnip):
    sun_price = constants.FIRECATNIP_PRICE
    cooldown = 3000
    alone = False
    upgrade_to = None
    anim_key = 'catnip_fire'
    name = '火球猫尾草'

    def __init__(self, ctx, pos, game):
        super().__init__(ctx, pos, game)
        self.damage = 65
        self.interval = 140
        self.shoot_images = ctx.assets.anim('fire_pea')

    def action(self):
        if self.check() and self.tick % self.interval in (0, 25):
            pea = TrackedPea(self.ctx, self.x - 15, self.y - 5,
                             self.game, self.damage)
            pea.images = self.shoot_images
            self.game.peas.append(pea)


# 升级关系（原 update 字段）
Repeater.upgrade_to = GatlingPea
Catnip.upgrade_to = FireCatnip

# 注册表：config.json 的 prop 键 → 植物类
PLANT_REGISTRY = {
    cls.__name__: cls for cls in (
        Sunflower, PeaShooter, Repeater, SpicyChili, NutsWall,
        PotatoMine, CherryBomb, Torchwood, GatlingPea, Catnip, FireCatnip,
    )
}

# 默认可选卡植物（顺序即卡槽顺序）
DEFAULT_PLANTS = [
    Sunflower, PeaShooter, Repeater, SpicyChili, NutsWall,
    PotatoMine, CherryBomb, Torchwood, GatlingPea,
]
