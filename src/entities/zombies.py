# -*- coding: utf-8 -*-
"""僵尸实体。"""
import math
import random

import pygame

from src.core import constants
from src.entities.coin import SilverCoin, GoldCoin, Diamond
from src.entities.sun import Sun


class Zombie:
    health = constants.NORMAL_ZOMBIE_HEALTH
    speed = 0.25
    fps = 4
    damage = 100
    x_offset = 10
    y_offset = 20
    rect_offset = 0
    sun_val = 0
    walk_key = 'zombie_normal_walk'
    eat_key = 'zombie_normal_eat'
    die_key = 'zombie_death_normal'
    hit_group = 'splat'

    def __init__(self, ctx, y, game):
        self.ctx = ctx
        self.game = game
        self.y = y
        self.x = constants.ZOMBIE_X
        self.blood = self.health
        self.tick = 0
        self.dead = 0
        self.dead_animation = True
        self.dead_index = 0
        self.row = game.zombie_road[y]
        self.eating = None
        self.eat_count = 0
        self.state = 'walk'
        self.last_state = None
        self.rect = pygame.Rect(
            self.x + self.rect_offset, self.y + 75, 75, 80)
        self.walk_images = ctx.assets.anim(self.walk_key)
        self.eat_images = ctx.assets.anim(self.eat_key)
        self.die_images = ctx.assets.anim(self.die_key)
        self.head_images = ctx.assets.anim('zombie_death_head')
        self.images = None
        self.image_index = 0
        game.zombies_inroad[self.row].append(self)

    def draw(self):
        if self.dead == 0:
            self.state = 'eat' if self.eating else 'walk'
            for plant in self.game.plants_inroad[self.row]:
                if self.rect.colliderect(plant.rect):
                    self.eating = plant
                    self.state = 'eat'
                    self.reset_state()
                    break
            if self.state == 'walk':
                self.images = self.walk_images
                self.x -= self.speed
                self.rect.x = self.x + self.rect_offset
            else:
                self.images = self.eat_images
                if self.game.lawns[self.eating.row - 1][self.eating.col - 1].plant:
                    if self.eat_count % 60 == 0:
                        if self.eating.hurt(self.damage):
                            self.state = 'walk'
                            self.reset_state()
                            self.eating = None
                    self.eat_count += 1
                else:
                    self.eat_count = 60
                    self.state = 'walk'
                    self.reset_state()
                    self.eating = None
            if self.tick % self.fps == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            self.tick += 1
            self.ctx.screen.blit(self.images[self.image_index],
                                 (self.x + self.x_offset, self.y + self.y_offset))
        elif self.dead_animation:
            self.die_animation()
        else:
            self.destroy()

    def reset_state(self):
        if self.last_state != self.state:
            self.image_index = 0
            self.last_state = self.state

    def die_animation(self):
        if self.dead_index < len(self.die_images):
            body_frame = self.die_images[math.floor(self.dead_index)]
            if self.dead == 1:
                head_frame = self.head_images[math.floor(self.dead_index + 0.05)]
                self.ctx.screen.blit(head_frame, (self.x + 60, self.y + 5))
                self.ctx.screen.blit(body_frame, (self.x + 10, self.y + 20))
            elif self.dead == 2:
                self.ctx.screen.blit(body_frame, (self.x + 70, self.y + 55))
            self.dead_index += 0.15
        else:
            self.destroy()
            self.ctx.assets.random_sound('zombie_falling').play()

    def destroy(self):
        choose = random.randrange(100)
        if 0 < choose <= 10:
            coin_cls = None
            if 5 < choose <= 10:
                coin_cls = SilverCoin
            elif 3 < choose <= 5:
                coin_cls = GoldCoin
            elif 0 < choose <= 3:
                coin_cls = Diamond
            self.game.coins.append(
                coin_cls(self.ctx, self.x + 60, self.y + 120, self.game))
        if self.sun_val != 0:
            self.game.suns.append(
                Sun(self.ctx, self.sun_val, (self.x + 45, self.y + 80), self.game))
        self.game.zombies.remove(self)
        self.game.zombies_inroad[self.row].remove(self)
        self.game.cur_score += 1
        self.game.won_pos = [self.x + 30, self.y + 90]


class NormalZombie(Zombie):
    fps = 4.5
    rect_offset = 80


class ConeheadZombie(Zombie):
    health = constants.CONEHEAD_ZOMBIE_HEALTH
    fps = 5.5
    rect_offset = 95
    walk_key = 'zombie_cone_walk'
    eat_key = 'zombie_cone_eat'


class BucketheadZombie(Zombie):
    health = constants.BUCKETHEAD_ZOMBIE_HEALTH
    fps = 5.5
    rect_offset = 75
    walk_key = 'zombie_bucket_walk'
    eat_key = 'zombie_bucket_eat'
    hit_group = 'iron_hit'


class FootballZombie(Zombie):
    health = constants.FOOTBALL_ZOMBIE_HEALTH
    speed = 0.5
    fps = 4.5
    y_offset = 0
    rect_offset = 70
    walk_key = 'dave_walk'
    eat_key = 'dave_eat'
    die_key = 'crazy_dave_death'
