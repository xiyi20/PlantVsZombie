# -*- coding: utf-8 -*-
"""用户配置（config.json）的读写封装。"""
import json
from pathlib import Path


class AppConfig:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.name: str = ''
        self.money: int = 0
        self.game_volume: float = 1.0
        self.menu_volume: float = 0.2
        self.prop: dict = {}
        self._raw: dict = {}
        self.load()

    def load(self) -> None:
        with open(self.path, 'r', encoding='utf-8') as f:
            self._raw = json.load(f)
        self.name = self._raw['user']['name']
        self.money = self._raw['user']['money']
        self.game_volume = self._raw['volume']['game']
        self.menu_volume = self._raw['volume']['menu']
        self.prop = self._raw.get('prop', {})

    def save(self, zone: str, name: str, value, prop: bool = False) -> None:
        if prop:
            self._raw['prop'][zone][name] = value
        else:
            self._raw[zone][name] = value
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self._raw, f, indent=4)
        self.load()
