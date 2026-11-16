# -*- coding: utf-8 -*-
"""素材目录/文件中文→英文重命名脚本。

用法：
    python tools/rename_assets.py           # dry-run，仅打印将执行的重命名
    python tools/rename_assets.py --apply   # 实际执行重命名

只按显式映射表重命名；映射表未命中的非 ASCII 路径会打印报告并保留原名。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'img'

# 旧目录（相对 img 的 POSIX 风格路径）→ 新目录
DIR_MAP = {
    'img/主界面': 'img/menu',
    'img/僵尸死': 'img/zombie_death',
    'img/僵尸死/普通': 'img/zombie_death/normal',
    'img/僵尸死/普通/头': 'img/zombie_death/normal/head',
    'img/僵尸死/灰烬': 'img/zombie_death/ash',
    'img/双重射手': 'img/repeater',
    'img/向日葵': 'img/sunflower',
    'img/土豆地雷': 'img/potato_mine',
    'img/坚果': 'img/wallnut',
    'img/大爷': 'img/crazy_dave',
    'img/大爷/吃': 'img/crazy_dave/eat',
    'img/大爷/死': 'img/crazy_dave/dead',
    'img/大爷/走': 'img/crazy_dave/walk',
    'img/太阳': 'img/sun',
    'img/普通僵尸': 'img/zombie_normal',
    'img/普通僵尸/吃': 'img/zombie_normal/eat',
    'img/普通僵尸/走': 'img/zombie_normal/walk',
    'img/机枪射手': 'img/gatling_pea',
    'img/樱桃炸弹': 'img/cherry_bomb',
    'img/火': 'img/fire',
    'img/火炬树桩': 'img/torchwood',
    'img/火爆辣椒': 'img/jalapeno',
    'img/猫尾草': 'img/catnip',
    'img/猫尾草/火': 'img/catnip/fire',
    'img/猫尾草/普通': 'img/catnip/normal',
    'img/豆': 'img/pea',
    'img/豆/普通': 'img/pea/normal',
    'img/豆/火豆': 'img/pea/fire',
    'img/豌豆射手': 'img/peashooter',
    'img/路障僵尸': 'img/zombie_cone',
    'img/路障僵尸/吃': 'img/zombie_cone/eat',
    'img/路障僵尸/走': 'img/zombie_cone/walk',
    'img/铁桶僵尸': 'img/zombie_bucket',
    'img/铁桶僵尸/吃': 'img/zombie_bucket/eat',
    'img/铁桶僵尸/走': 'img/zombie_bucket/walk',
    'img/widget/关卡': 'img/widget/level',
    'img/widget/商店': 'img/widget/shop',
    'img/widget/菜单栏': 'img/widget/hud',
    'img/widget/进度': 'img/widget/progress',
    'img/widget/信封': 'img/widget/envelope',
    'img/widget/准备开始': 'img/widget/ready',
    'img/widget/准备开始/年度版': 'img/widget/ready/annual',
    'img/widget/戴夫': 'img/widget/dave',
    'img/widget/菜单的': 'img/widget/option',
    'img/widget/菜单的/选项': 'img/widget/option/items',
    'img/p': 'img/plants_extra',
    'img/z': 'img/zombies_extra',
    'img/z/蹦极僵尸': 'img/zombies_extra/bungee',
    'img/z/冰车僵尸': 'img/zombies_extra/zamboni',
    'img/z/橄榄球僵尸': 'img/zombies_extra/football',
    'img/z/海豚骑士僵尸': 'img/zombies_extra/dolphin',
    'img/z/救生圈僵尸': 'img/zombies_extra/swimmer',
    'img/z/旗帜僵尸': 'img/zombies_extra/flag',
    'img/z/普通僵尸': 'img/zombies_extra/normal',
    'img/z/潜水僵尸': 'img/zombies_extra/scuba',
    'img/z/路障僵尸': 'img/zombies_extra/cone',
    'img/z/铁门僵尸': 'img/zombies_extra/screen',
    'img/z/铁桶僵尸': 'img/zombies_extra/bucket',
    'img/z/小丑僵尸': 'img/zombies_extra/clown',
    'img/z/小鬼僵尸': 'img/zombies_extra/imp',
}

# 旧目录 → { 旧文件名: 新文件名 }
BASENAME_MAP = {
    'img/scene': {
        '白天.jpg': 'day.jpg',
        '白天屋顶.jpg': 'day_roof.jpg',
        '迷雾.jpg': 'fog.jpg',
        '三条.jpg': 'three_lane.jpg',
        '一条.jpg': 'one_lane.jpg',
        '土地.jpg': 'ground.jpg',
        '晚上.jpg': 'night.jpg',
        '晚上屋顶.jpg': 'night_roof.jpg',
        '泳池.jpg': 'pool.jpg',
    },
    'img/widget': {
        '小推车.png': 'lawn_mower.png',
        '遮罩.png': 'mask.png',
        '卡槽.png': 'card_slot.png',
        '失败.png': 'lose.png',
        '大波僵尸.png': 'big_wave.png',
        '弹坑.png': 'crater.png',
        '返回.png': 'back.png',
        '服.gif': 'fu.gif',
        '公告.jpg': 'notice.jpg',
        '关.png': 'gate.png',
        '关卡.png': 'level.png',
        '僵尸介绍.jpg': 'zombie_intro.jpg',
        '奖杯.png': 'trophy.png',
        '介绍僵尸.png': 'intro_zombie.png',
        '介绍植物.png': 'intro_plant.png',
        '迷雾1.png': 'fog1.png',
        '迷雾2.png': 'fog2.png',
        '迷雾3.png': 'fog3.png',
        '迷雾4.png': 'fog4.png',
        '脑子.png': 'brain.png',
        '水.gif': 'water.gif',
        '水晚上.gif': 'water_night.gif',
        '太阳.gif': 'sun.gif',
        '新植物！.jpg': 'new_plant.jpg',
        '选关界面.jpg': 'level_select.jpg',
        '选择查看的僵尸.png': 'selected_zombie.png',
        '阳关计数.png': 'sun_counter.png',
        '已被选.png': 'selected.png',
        '影子.png': 'shadow.png',
        '游戏愉快.png': 'happy_game.png',
        '植物介绍.jpg': 'plant_intro.jpg',
        '最后一波.gif': 'final_wave.gif',
    },
    'img/widget/菜单栏': {
        '按钮.png': 'button.png',
        '铲子.png': 'shovel.png',
        '铲子槽.png': 'shovel_slot.png',
        '植物商店.png': 'plant_shop.png',
    },
    'img/widget/商店': {
        '香蒲.png': 'catnip.png',
        '火焰香蒲.png': 'fire_catnip.png',
    },
    'img/widget/菜单的': {
        '图鉴.png': 'album.png',
        '向日葵奖杯.png': 'sunflower_trophy.png',
    },
    'img/widget/菜单的/选项': {
        '冒险.png': 'adventure.png',
        '你游.png': 'mini_game.png',
        '益智.png': 'puzzle.png',
    },
    'img/widget/准备开始': {
        '中文版.png': 'chinese.png',
    },
    'img/widget/准备开始/年度版': {
        '好.png': 'ok.png',
        '开始.png': 'start.png',
        '开始游戏3.png': 'start_game3.png',
    },
    'img/widget/戴夫': {
        '戴夫.gif': 'dave.gif',
        '戴夫 (2).gif': 'dave2.gif',
    },
    'img/土豆地雷': {
        '爆炸.gif': 'boom.gif',
        '土豆泥.gif': 'mash.gif',
        '在地下.gif': 'underground.gif',
    },
    'img/p': {
        '爆炸坚果.gif': 'exploding_wallnut.gif',
        '冰爆.gif': 'ice_burst.gif',
        '冰豆.gif': 'ice_pea.gif',
        '冰西瓜.GIF': 'icy_watermelon.GIF',
        '缠绕.png': 'vine.png',
        '缠绕水草.gif': 'tangle_kelp.gif',
        '吃.gif': 'eat.gif',
        '大喷菇.gif': 'fume_shroom.gif',
        '大喷菇睡觉.gif': 'fume_shroom_sleep.gif',
        '大喷菇子弹.gif': 'fume_shroom_shot.gif',
        '大蒜.gif': 'garlic.gif',
        '大嘴花.gif': 'chomper.gif',
        '胆小菇.gif': 'scaredy_shroom.gif',
        '胆小菇胆小.gif': 'scaredy_shroom_scared.gif',
        '胆小菇睡觉.gif': 'scaredy_shroom_sleep.gif',
        '弹坑.png': 'crater.png',
        '地刺.gif': 'spike.gif',
        '灯笼花.gif': 'lantern.gif',
        '豆.gif': 'bean.gif',
        '毒液.gif': 'venom.gif',
        '多嘴小蘑菇.gif': 'chat_shroom.gif',
        '多嘴小蘑菇睡觉.gif': 'chat_shroom_sleep.gif',
        '多嘴小蘑菇子弹.gif': 'chat_shroom_shot.gif',
        '钢地刺.gif': 'steel_spike.gif',
        '寒冰菇.gif': 'ice_shroom.gif',
        '寒冰射手.gif': 'snow_pea.gif',
        '寒冰睡觉.gif': 'ice_shroom_sleep.gif',
        '轰隆！.png': 'boom.png',
        '花盆.gif': 'pot.gif',
        '火.gif': 'fire.gif',
        '火爆辣椒.gif': 'jalapeno.gif',
        '火豆.gif': 'fire_pea.gif',
        '火炬树桩.gif': 'torchwood.gif',
        '机枪射手.gif': 'gatling_pea.gif',
        '即将爆炸的末日菇.gif': 'doom_shroom_explode.gif',
        '坚果.gif': 'wallnut.gif',
        '巨型坚果.gif': 'giant_wallnut.gif',
        '咖啡豆.gif': 'coffee_bean.gif',
        '路灯花.gif': 'street_light.gif',
        '猫尾草.gif': 'catnip.gif',
        '迷糊菇.gif': 'daze_shroom.gif',
        '迷糊菇睡觉.gif': 'daze_shroom_sleep.gif',
        '末日菇睡觉.gif': 'doom_shroom_sleep.gif',
        '南瓜头后面.gif': 'pumpkin_back.gif',
        '南瓜头外面.gif': 'pumpkin_front.gif',
        '三叶草.gif': 'clover.gif',
        '三叶草吹.gif': 'clover_blow.gif',
        '三重射手.gif': 'triple_pea.gif',
        '散落.gif': 'scatter.gif',
        '双胞向日葵.gif': 'twins_sunflower.gif',
        '双向射手.gif': 'split_pea.gif',
        '双重射手.gif': 'repeater.gif',
        '水滨菇.gif': 'pool_shroom.gif',
        '水草.gif': 'waterweed.gif',
        '碎了.gif': 'broken.gif',
        '头亮.gif': 'head_light.gif',
        '土豆地雷.gif': 'potato_mine.gif',
        '土豆泥.gif': 'mash.gif',
        '吞噬.gif': 'swallow.gif',
        '吞吞碑.gif': 'grave_buster.gif',
        '豌豆射手.gif': 'peashooter.gif',
        '窝瓜.gif': 'squash.gif',
        '窝瓜跳跃.gif': 'squash_jump.gif',
        '仙人掌.gif': 'cactus.gif',
        '向日葵.gif': 'sunflower.gif',
        '小喷菇.gif': 'puff_shroom.gif',
        '小喷菇睡觉.gif': 'puff_shroom_sleep.gif',
        '星星.gif': 'star.gif',
        '星星果.gif': 'starfruit.gif',
        '阳光菇.gif': 'sun_shroom.gif',
        '阳光菇成年.gif': 'sun_shroom_grown.gif',
        '阳光菇睡觉.gif': 'sun_shroom_sleep.gif',
        '樱桃炸弹.gif': 'cherry_bomb.gif',
    },
    'img/z': {
        '僵尸死.gif': 'zombie_dead.gif',
        '头.gif': 'head.gif',
    },
    'img/z/蹦极僵尸': {'蹦极僵尸.gif': 'bungee.gif'},
    'img/z/冰车僵尸': {'冰车僵尸.gif': 'zamboni.gif'},
    'img/z/橄榄球僵尸': {
        '橄榄球僵尸.gif': 'football.gif',
        '橄榄球僵尸啃食.gif': 'football_eat.gif',
        '橄榄球僵尸死.gif': 'football_dead.gif',
    },
    'img/z/海豚骑士僵尸': {
        '掉入水中.gif': 'splash.gif',
        '海豚游泳.gif': 'dolphin_swim.gif',
        '海豚游泳啃食.gif': 'dolphin_swim_eat.gif',
        '骑海豚死.gif': 'dolphin_dead.gif',
        '跳跃.gif': 'jump.gif',
    },
    'img/z/救生圈僵尸': {
        '救生圈僵尸.gif': 'swimmer.gif',
        '救生圈僵尸啃食.gif': 'swimmer_eat.gif',
        '救生圈僵尸死.gif': 'swimmer_dead.gif',
    },
    'img/z/旗帜僵尸': {
        '旗帜僵尸.gif': 'flag.gif',
        '旗帜僵尸啃食.gif': 'flag_eat.gif',
    },
    'img/z/普通僵尸': {
        '普通僵尸啃食.gif': 'normal_eat.gif',
        '普通僵尸走路.gif': 'normal_walk.gif',
    },
    'img/z/潜水僵尸': {'潜水僵尸.gif': 'scuba.gif'},
    'img/z/路障僵尸': {
        '路障僵尸.gif': 'cone.gif',
        '路障僵尸啃食.gif': 'cone_eat.gif',
    },
    'img/z/铁门僵尸': {
        '铁门僵尸.gif': 'screen.gif',
        '铁门僵尸啃食.gif': 'screen_eat.gif',
    },
    'img/z/铁桶僵尸': {
        '铁桶僵尸.gif': 'bucket.gif',
        '铁桶僵尸啃食.gif': 'bucket_eat.gif',
    },
    'img/z/小丑僵尸': {
        '小丑僵尸.gif': 'clown.gif',
        '准备爆炸.gif': 'about_to_explode.gif',
    },
    'img/z/小鬼僵尸': {
        '小鬼僵尸.gif': 'imp.gif',
        '小鬼啃食.gif': 'imp_eat.gif',
        '小鬼死亡.gif': 'imp_dead.gif',
    },
}


def is_ascii(text: str) -> bool:
    return all(ord(ch) < 128 for ch in text)


def build_moves():
    moves = []
    unmapped = []
    for path in sorted(IMG.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        old_dir = str(Path(rel).parent).replace('\\', '/')
        name = path.name
        new_dir = DIR_MAP.get(old_dir, old_dir)
        new_name = BASENAME_MAP.get(old_dir, {}).get(name, name)
        new_rel = f'{new_dir}/{new_name}'
        if new_rel == rel:
            if not is_ascii(rel):
                unmapped.append(rel)
            continue
        if not is_ascii(new_rel):
            unmapped.append(rel)
            continue
        moves.append((rel, new_rel))
    return moves, unmapped


def main():
    apply = '--apply' in sys.argv
    moves, unmapped = build_moves()
    for old, new in moves:
        print(f'{old}  ->  {new}')
    if unmapped:
        print('\n[未命中映射表，保留原名]')
        for rel in unmapped:
            print('  ' + rel)
    print(f'\n共 {len(moves)} 个重命名，{len(unmapped)} 个未命中。'
          + ('（dry-run，未做任何修改，加 --apply 执行）' if not apply else ''))
    if not apply:
        return

    for old, new in moves:
        src = ROOT / old
        dst = ROOT / new
        dst.parent.mkdir(parents=True, exist_ok=True)
        if str(src).lower() == str(dst).lower() and src.name != dst.name:
            # 仅大小写变化：两步改名，避免 Windows 不敏感文件系统吞掉差异
            tmp = dst.with_name(dst.name + '.tmp_rename')
            src.rename(tmp)
            tmp.rename(dst)
        else:
            src.rename(dst)

    # 清理空的旧目录（自底向上）
    for path in sorted(IMG.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
            print(f'rmdir {path.relative_to(ROOT).as_posix()}')
    print('完成。')


if __name__ == '__main__':
    main()
