from logging import critical

from data import Cache
from entities import CompetitivePokemon, Move
from pkm_sim.battle_env import damage_calculation, is_critical_hit
from utils import get_type_effectiveness, from_name_to_api_read

CACHE = Cache()

class BattlePokemon:
    def __init__(self, pokemon: CompetitivePokemon):
        self.pokemon = pokemon
        self.hp_total = pokemon.base_stats['hp']
        self.status_conditions = None
        self.stats = {
            'atk': pokemon.base_stats['atk'],
            'def': pokemon.base_stats['def'],
            'spatk': pokemon.base_stats['spatk'],
            'spdef': pokemon.base_stats['spdef'],
            'spd': pokemon.base_stats['spd'],
            'acc': 1,
            'eva': 0
        }
        self.stat_changes = {
            'atk': 0,
            'def': 0,
            'spatk': 0,
            'spdef': 0,
            'spd': 0,
            'acc': 0,
            'eva': 0
        }
        self.current_hp = self.hp_total
        self.crit_stage = 0
        self.battle_moves = self.get_info_moves(pokemon.moves)

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def apply_damage(self, damage: int):
        self.current_hp = max(0, self.current_hp - damage)

    def heal(self, amount: int):
        self.current_hp = min(self.pokemon.base_stats['hp'], self.current_hp + amount)

    def attack(self, target: 'BattlePokemon', move: Move):
        used_atk = self.pokemon.base_stats['atk'] if move.damage_class == 'physical' else self.pokemon.base_stats['spatk']
        used_def = target.pokemon.base_stats['def'] if move.damage_class == 'physical' else target.pokemon.base_stats['spdef']

        target_multiplier = 1 if move.target == 'selected-pokemon' else 0.75  # Simplified for single target moves
        critical_hit = is_critical_hit(self.crit_stage + move.crit_rate)
        stab = 1.5 if move.move_type in self.pokemon.types else 1.0
        if len(target.pokemon.types) == 2:
            type_multiplier = get_type_effectiveness(move.move_type, target.pokemon.types[0]) * get_type_effectiveness(move.move_type, target.pokemon.types[1]) # Simplified, should be based on type effectiveness
        else:
            type_multiplier = get_type_effectiveness(move.move_type, target.pokemon.types[0])
        damage = damage_calculation(
            attacker_stat=used_atk, defender_stat=used_def, move_power=move.power, targets=target_multiplier,
            PB=1, weather=1, GLAIVE_RUSH=1, critical_hit=critical_hit, stab=stab, type_=type_multiplier, burn=1, other=1, z_move=1
        )
        target.apply_damage(damage)
        return f"{self.pokemon.name} used {move.name} and dealt {damage} damage to {target.pokemon.name}!"

    def get_info_moves(self, moves: list):
        battle_moves = []
        for move_name in moves:
            move_name = from_name_to_api_read(move_name.lower())
            battle_moves.append(CACHE.get_move_from_cache(move_name))

        return battle_moves

    def get_move(self, move_name: str) -> Move:
        for move in self.battle_moves:
            if move.name == move_name:
                return move
        raise ValueError(f"Move {move_name} not found in battle moves.")
