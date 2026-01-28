import math
from utils import natures
from data import Cache

CACHE = Cache()

class CompetitivePokemon:
    def __init__(self, name: str, ability: str, nature: str, moves: list,
                 ivs: dict=None, evs: dict=None, item: str=None, level: int = 50,nickname: str=None):
        self.name = name
        self.nickname = nickname
        if nickname is None:
            self.nickname = self.name
        self.ability = ability
        self.item = item
        self.nature = nature.upper()
        self.evs = evs  # Effort Values as a dictionary
        self.moves = moves  # List of moves
        self.ivs = ivs  # Individual Values as a dictionary
        self.level = level
        self.raw_stats = {}
        if ivs is None:
            self.ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}
        if evs is None:
            self.evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
        self.pkm = CACHE.get_pokemon_from_cache(self.name)
        self.calculate_all_stats()


    def calculate_stat(self, base: int, iv: int, ev: int, level: int, nature_modifier: float) -> int:
        """Calculate a stat based on the formula used in Pokémon games."""
        stat = math.floor(math.floor(math.floor((2 * base + iv + (ev // 4)) * level / 100) + 5) * nature_modifier)
        return stat

    def calculate_hp(self, base: int, iv: int, ev: int, level: int) -> int:
        """Calculate HP stat based on the formula used in Pokémon games."""
        hp = math.floor((2 * base + iv + (ev // 4)) * level / 100) + level + 10
        return hp

    def calculate_all_stats(self):
        self.raw_stats['hp'] = self.calculate_hp(self.pkm.base_stats['hp'], self.ivs.get('hp'), self.evs.get('hp'), self.level)
        self.raw_stats['atk'] = self.calculate_stat(self.pkm.base_stats['atk'], self.ivs.get('atk'), self.evs.get('atk'), self.level, natures[self.nature]['atk'])
        self.raw_stats['def'] = self.calculate_stat(self.pkm.base_stats['def'], self.ivs.get('def'), self.evs.get('def'), self.level, natures[self.nature]['def'])
        self.raw_stats['spa'] = self.calculate_stat(self.pkm.base_stats['spa'], self.ivs.get('spa'), self.evs.get('spa'), self.level, natures[self.nature]['spa'])
        self.raw_stats['spd'] = self.calculate_stat(self.pkm.base_stats['spd'], self.ivs.get('spd'), self.evs.get('spd'), self.level, natures[self.nature]['spd'])
        self.raw_stats['spe'] = self.calculate_stat(self.pkm.base_stats['spe'], self.ivs.get('spe'), self.evs.get('spe'), self.level, natures[self.nature]['spe'])

    def __str__(self):
        return f"{self.name} (Level {self.level}) - Nature: {self.nature}, Ability: {self.ability}, Item: {self.item}\n" \
               f"Stats: HP: {self.base_stats}\n"

