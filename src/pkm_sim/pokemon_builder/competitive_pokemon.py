import math
from typing import Optional

from api.models.pokemon import Pokemon
from utils import natures

class CompetitivePokemon(Pokemon):
    def __init__(self, id: int, name: str, evolution_chain_id: Optional[int], varieties: Optional[list], types: list, base_stats: dict,
                 abilities: list, height: float, weight: float, move_list: list, img_url: str,
                 ability: str, item: str, nature: str, ivs: dict, evs: dict, moves: list, level: int = 50):
        super().__init__(id=id, types=types, name=name, base_stats=base_stats, abilities=abilities,
                         height=height, weight=weight, move_list=move_list, img_url=img_url,
                         evolution_chain_id=evolution_chain_id, varieties=varieties
                         )
        self.ability = ability
        self.item = item
        self.nature = nature.upper()
        self.evs = evs  # Effort Values as a dictionary
        self.moves = moves  # List of moves
        self.ivs = ivs  # Individual Values as a dictionary
        self.level = level
        self.raw_stats = {}
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
        self.raw_stats['hp'] = self.calculate_hp(self.base_stats['hp'], self.ivs.get('hp'), self.evs.get('hp'), self.level)
        self.raw_stats['atk'] = self.calculate_stat(self.base_stats['atk'], self.ivs.get('atk'), self.evs.get('atk'), self.level, natures[self.nature]['atk'])
        self.raw_stats['def'] = self.calculate_stat(self.base_stats['def'], self.ivs.get('def'), self.evs.get('def'), self.level, natures[self.nature]['def'])
        self.raw_stats['spatk'] = self.calculate_stat(self.base_stats['spatk'], self.ivs.get('spatk'), self.evs.get('spatk'), self.level, natures[self.nature]['spatk'])
        self.raw_stats['spdef'] = self.calculate_stat(self.base_stats['spdef'], self.ivs.get('spdef'), self.evs.get('spdef'), self.level, natures[self.nature]['spdef'])
        self.raw_stats['spd'] = self.calculate_stat(self.base_stats['spd'], self.ivs.get('spd'), self.evs.get('spd'), self.level, natures[self.nature]['spd'])

    def __str__(self):
        return f"{self.name} (Level {self.level}) - Nature: {self.nature}, Ability: {self.ability}, Item: {self.item}\n" \
               f"Stats: HP: {self.base_stats}\n"
