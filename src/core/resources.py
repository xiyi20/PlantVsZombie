# -*- coding: utf-8 -*-
"""资源管理器：命名键访问素材，路径基于项目根目录（或 exe 所在目录）解析。"""
import random
import sys
from pathlib import Path

import pygame

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parents[2]


def _p(rel: str) -> str:
    """将相对路径转换为绝对路径字符串（pygame 需要 str）。"""
    return str((BASE_DIR / rel).as_posix())


# 单张图片
IMAGE_MANIFEST = {
    'lawn_mower': 'img/widget/lawn_mower.png',
    'potato_boom': 'img/potato_mine/boom.gif',
    'potato_mash': 'img/potato_mine/mash.gif',
    'cherry_boom': 'img/cherry_bomb/boom.png',
    'mask': 'img/widget/mask.png',
    'coin_silver': 'img/widget/level/coin_silver.png',
    'coin_gold': 'img/widget/level/coin_gold.png',
    'diamond': 'img/widget/level/Diamond.png',
    'coin_bank': 'img/widget/level/coinbank.png',
    'menu_button': 'img/widget/hud/button.png',
    'shop_bg': 'img/menu/Store.png',
    'shop_dialog': 'img/menu/dialog.png',
    'thorn': 'img/catnip/thorn.png',
    'card_slot': 'img/widget/card_slot.png',
    'icon': 'img/icon.png',
    'bg_day': 'img/scene/day.jpg',
    'moneybag': 'img/widget/level/moneybag.png',
    'plant_shop': 'img/widget/hud/plant_shop.png',
    'shovel_slot': 'img/widget/hud/shovel_slot.png',
    'shovel': 'img/widget/hud/shovel.png',
    'progress_level': 'img/widget/progress/FlagMeterLevelProgress.png',
    'progress_empty': 'img/widget/progress/FlagMeterEmpty.png',
    'progress_flag1': 'img/widget/progress/FlagMeterParts1.png',
    'progress_flag2': 'img/widget/progress/FlagMeterParts2.png',
    'seedchooser_bg': 'img/widget/level/SeedChooser_Background.png',
    'seedchooser_btn': 'img/widget/level/SeedChooser_Button.png',
    'lose': 'img/widget/lose.png',
    'sold_out': 'img/widget/shop/Store_SoldOutLabel.png',
    # 主界面
    'title_screen': 'img/menu/titlescreen.jpg',
    'popcap_logo': 'img/menu/PopCap_Logo.png',
    'pvz_logo': 'img/menu/PvZ_Logo.png',
    'load_bar_dirt': 'img/menu/LoadBar_dirt.png',
    'load_bar_grass': 'img/menu/LoadBar_grass.png',
    'sod_roll_cap': 'img/menu/SodRollCap.png',
    'main_center': 'img/menu/center.png',
    'main_bg': 'img/menu/SelectorScreen_BG.png',
    'main_left': 'img/menu/left.png',
    'main_right': 'img/menu/right.png',
    'wood_sign1': 'img/menu/SelectorScreen_WoodSign1.png',
    'wood_sign2': 'img/menu/SelectorScreen_WoodSign2.png',
    'wood_sign2_press': 'img/menu/SelectorScreen_WoodSign2_press.png',
    'leaves': 'img/menu/SelectorScreen_Leaves.png',
    'leaf1': 'img/menu/SelectorScreen_Leaf4.png',
    'leaf2': 'img/menu/SelectorScreen_Leaf5.png',
    'leaf3': 'img/menu/SelectorScreen_Leaf3.png',
    'leaf4': 'img/menu/SelectorScreen_Leaf1.png',
    'flower1': 'img/menu/SelectorScreen_Flower1.png',
    'flower2': 'img/menu/SelectorScreen_Flower2.png',
    'flower3': 'img/menu/SelectorScreen_Flower3.png',
    'help0': 'img/menu/SelectorScreen_Help1.png',
    'help1': 'img/menu/SelectorScreen_Help2.png',
    'option0': 'img/menu/SelectorScreen_Options1.png',
    'option1': 'img/menu/SelectorScreen_Options2.png',
    'exit0': 'img/menu/SelectorScreen_Quit1.png',
    'exit1': 'img/menu/SelectorScreen_Quit2.png',
    'adventure0': 'img/menu/SelectorScreen_StartAdventure_Button.png',
    'adventure1': 'img/menu/SelectorScreen_StartAdventure_Highlight.png',
    'small0': 'img/menu/SelectorScreen_Survival_button.png',
    'small1': 'img/menu/SelectorScreen_Survival_highlight.png',
    'challenge0': 'img/menu/SelectorScreen_Challenges_button.png',
    'challenge1': 'img/menu/SelectorScreen_Challenges_highlight.png',
    'survival0': 'img/menu/SelectorScreen_Vasebreaker_button.png',
    'survival1': 'img/menu/SelectorScreen_vasebreaker_highlight.png',
    'shop0': 'img/menu/SelectorScreen_Store.png',
    'shop1': 'img/menu/SelectorScreen_StoreHighlight.png',
    'says': 'img/menu/says.png',
    'says_bg': 'img/menu/saysbg.jpg',
    'back_menu0': 'img/menu/return.png',
    'back_menu1': 'img/menu/return1.png',
    'rename': 'img/menu/rename.png',
    # 暂停菜单
    'options_bg': 'img/widget/hud/options_menuback.png',
    'return_btn0': 'img/widget/hud/options_backtogamebutton0.png',
    'return_btn1': 'img/widget/hud/options_backtogamebutton1.png',
    'slider_slot': 'img/widget/hud/options_sliderslot.png',
    'slider_knob': 'img/widget/hud/options_sliderknob2.png',
}

# 动画（帧列表）：键 → 路径模板（用 {} 插帧号）或显式路径列表
ANIM_MANIFEST = {
    'sun': ('img/sun/{}.png', 29),
    'pea': ['img/pea/normal/0.png'],
    'fire_pea': ('img/pea/fire/{}.png', 2),
    'potato_underground': ['img/potato_mine/underground.gif'],
    'zombie_death_normal': ('img/zombie_death/normal/{}.png', 10),
    'zombie_death_ash': ('img/zombie_death/ash/{}.png', 10),
    'zombie_death_head': ('img/zombie_death/normal/head/{}.png', 12),
    'crazy_dave_death': ('img/crazy_dave/dead/{}.png', 7),
    'ready_set_plant': [
        'img/widget/level/StartReady.png',
        'img/widget/level/StartSet.png',
        'img/widget/level/StartPlant.png',
    ],
    # 僵尸
    'zombie_normal_walk': ('img/zombie_normal/walk/{}.png', 18),
    'zombie_normal_eat': ('img/zombie_normal/eat/{}.png', 18),
    'zombie_cone_walk': ('img/zombie_cone/walk/{}.png', 21),
    'zombie_cone_eat': ('img/zombie_cone/eat/{}.png', 11),
    'zombie_bucket_walk': ('img/zombie_bucket/walk/{}.png', 15),
    'zombie_bucket_eat': ('img/zombie_bucket/eat/{}.png', 11),
    'dave_walk': ('img/crazy_dave/walk/{}.png', 11),
    'dave_eat': ('img/crazy_dave/eat/{}.png', 10),
    # 植物
    'sunflower': ('img/sunflower/{}.png', 18),
    'peashooter': ('img/peashooter/{}.png', 13),
    'repeater': ('img/repeater/{}.png', 15),
    'jalapeno': ('img/jalapeno/{}.png', 7),
    'fire': ('img/fire/{}.png', 8),
    'wallnut': ('img/wallnut/{}.png', 16),
    'potato_armed': ('img/potato_mine/{}.png', 8),
    'cherry': ('img/cherry_bomb/{}.png', 7),
    'torchwood': ('img/torchwood/{}.png', 9),
    'gatling': ('img/gatling_pea/{}.png', 13),
    'catnip_fire': ('img/catnip/fire/{}.png', 14),
    'catnip_normal': ('img/catnip/normal/{}.png', 14),
}

SOUND_MANIFEST = {
    'plant_dead': 'aud/bigchomp.ogg',
    'zombie_coming': 'aud/awooga.ogg',
    'potato_active': 'aud/gravestone_rumble.ogg',
    'potato_boom': 'aud/potato_mine.ogg',
    'cherry_boom': 'aud/cherrybomb.ogg',
    'coin_fall': 'aud/moneyfalls.ogg',
    'coin_pick': 'aud/coin.ogg',
    'diamond_fall': 'aud/chime.ogg',
    'diamond_pick': 'aud/diamond.ogg',
    'paper': 'aud/paper.ogg',
    'menu_click': 'aud/grassstep.ogg',
    'button_click': 'aud/buttonclick.ogg',
    'win': 'aud/winmusic.ogg',
    'pause': 'aud/pause.ogg',
    'dave_click': 'aud/bleep.ogg',
    'ready_set_plant': 'aud/readySetPlant.ogg',
    'pickup': 'aud/points.ogg',
    'car': 'aud/lawnmower.ogg',
    'invalid': 'aud/buzzer.ogg',
    'shovel': 'aud/shovel.ogg',
    'plant_slot': 'aud/seedlift.ogg',
    'jalapeno': 'aud/jalapeno.ogg',
    'main_menu_bgm': 'aud/bgm/Laura Shigihara - Crazy Dave.ogg',
}

SOUND_GROUP_MANIFEST = {
    'zombie_eat': ['aud/chomp.ogg', 'aud/chomp2.ogg', 'aud/chompsoft.ogg'],
    'zombie_groan': [
        'aud/groan.ogg', 'aud/groan2.ogg', 'aud/groan3.ogg',
        'aud/groan4.ogg', 'aud/groan5.ogg', 'aud/groan6.ogg',
        'aud/lowgroan.ogg', 'aud/lowgroan2.ogg',
    ],
    'lose': ['aud/losemusic.ogg', 'aud/scream.ogg'],
    'plant': ['aud/plant.ogg', 'aud/plant2.ogg'],
    'splat': ['aud/splat.ogg', 'aud/splat2.ogg', 'aud/splat3.ogg'],
    'iron_hit': ['aud/shieldhit.ogg', 'aud/shieldhit.ogg'],
    'zombie_falling': ['aud/zombie_falling_1.ogg', 'aud/zombie_falling_1.ogg'],
    'shoot': ['aud/kernelpult.ogg', 'aud/kernelpult2.ogg'],
}

BGM_TRACKS = [
    'aud/bgm/Brainiac Maniac-Laura Shigihara.mp3',
    'aud/bgm/Graze the Roof-Laura Shigihara.mp3',
    'aud/bgm/Grasswalk.mp3',
    'aud/bgm/Loonboon-Laura Shigihara.mp3',
    'aud/bgm/Moongrains-Laura Shigihara.mp3',
    'aud/bgm/Rigor Mormist-Laura Shigihara.mp3',
    'aud/bgm/Ultimate Battle-Laura Shigihara.mp3',
    'aud/bgm/Watery Graves-Laura Shigihara.mp3',
]
BGM_CHOOSE = 'aud/bgm/Choose Your Seeds-Laura Shigihara.mp3'

FONT_MANIFEST = {
    'score': ('font/digit.ttf', 15),
    'price': ('font/digit.ttf', 13),
    'menu': ('font/fzsr.ttf', 22),
    'title': ('font/fzsr.ttf', 48),
    'wave': ('font/fzxs12.ttf', 12),
    'hover': ('font/fzxs12.ttf', 17),
}


class AssetManager:
    """一次性加载全部素材，提供命名访问。"""

    def __init__(self) -> None:
        self.images: dict[str, pygame.Surface] = {}
        self.anims: dict[str, list[pygame.Surface]] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.sound_groups: dict[str, list[pygame.mixer.Sound]] = {}
        self.fonts: dict[str, pygame.font.Font] = {}
        self.bgm_tracks: list[str] = []
        self.bgm_choose: str = ''
        self._extra_images: dict[str, pygame.Surface] = {}

    # ---------- 加载 ----------
    def load_all(self) -> None:
        for key, rel in IMAGE_MANIFEST.items():
            self.images[key] = pygame.image.load(_p(rel))
        for key, spec in ANIM_MANIFEST.items():
            if isinstance(spec, list):
                self.anims[key] = [pygame.image.load(_p(p)) for p in spec]
            else:
                pattern, count = spec
                self.anims[key] = [
                    pygame.image.load(_p(pattern.format(i))) for i in range(count)
                ]
        for key, rel in SOUND_MANIFEST.items():
            self.sounds[key] = pygame.mixer.Sound(_p(rel))
        for key, paths in SOUND_GROUP_MANIFEST.items():
            self.sound_groups[key] = [pygame.mixer.Sound(_p(p)) for p in paths]
        for key, (path, size) in FONT_MANIFEST.items():
            self.fonts[key] = pygame.font.Font(_p(path), size)
        self.bgm_tracks = [_p(p) for p in BGM_TRACKS]
        self.bgm_choose = _p(BGM_CHOOSE)

    # ---------- 访问 ----------
    def image(self, key: str) -> pygame.Surface:
        return self.images[key]

    def anim(self, key: str) -> list[pygame.Surface]:
        return self.anims[key]

    def sound(self, key: str) -> pygame.mixer.Sound:
        return self.sounds[key]

    def group(self, key: str) -> list[pygame.mixer.Sound]:
        return self.sound_groups[key]

    def random_sound(self, key: str) -> pygame.mixer.Sound:
        return random.choice(self.sound_groups[key])

    def font(self, key: str) -> pygame.font.Font:
        return self.fonts[key]

    def load_image(self, rel_path: str) -> pygame.Surface:
        """加载清单之外的图片（如 config.json 中的道具图），带缓存。"""
        if rel_path not in self._extra_images:
            self._extra_images[rel_path] = pygame.image.load(_p(rel_path))
        return self._extra_images[rel_path]

    def random_bgm(self) -> str:
        return random.choice(self.bgm_tracks)
