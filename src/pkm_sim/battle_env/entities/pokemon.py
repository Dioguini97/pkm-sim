import math
import random

from api.models import Move
from pkm_sim.battle_env.entities.move import BattleMove
from pkm_sim.battle_env.entities.status import Status, Effect
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon
from utils import from_name_to_api_read, stage_multipliers, Transformation
from data import Cache

CACHE = Cache()


class BattlePokemon:
    def __init__(self, pokemon: CompetitivePokemon):
        self.pokemon = pokemon
        self.hp_total = pokemon.raw_stats['hp']
        self.status: Status|None = None
        self.effects = []
        self.stats = {
            'atk': pokemon.raw_stats['atk'],
            'def': pokemon.raw_stats['def'],
            'spa': pokemon.raw_stats['spa'],
            'spd': pokemon.raw_stats['spd'],
            'spe': pokemon.raw_stats['spe']
        }
        self.stat_stages = {
            'atk': 0,
            'def': 0,
            'spa': 0,
            'spd': 0,
            'spe': 0,
            'acc': 0,
            'eva': 0,
            'crit': 0
        }
        self.current_hp = self.hp_total
        self.is_protected = False # Indica se o Pokémon está protegido (ex: usando Protect) Pode ser retirado se perceber que nao faz sentido
        self.perish_count = None
        self.battle_moves = self.get_info_moves(pokemon.moves)
        self.ailment = None

    def get_name(self):
        return self.pokemon.name if self.pokemon.nickname != self.pokemon.name else self.pokemon.nickname

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def faint(self):
        self.current_hp = 0
        self.status = Status.FAINTED

    def apply_damage(self, damage: int):
        self.current_hp = max(0, self.current_hp - damage)

    def heal(self, amount: int):
        self.current_hp = min(self.hp_total, self.current_hp + amount)

    def get_info_moves(self, moves: list) -> list[BattleMove]:
        """Obtém lista de BattleMove a partir dos nomes de moves."""
        battle_moves = []
        for move_name in moves:
            move_name = from_name_to_api_read(move_name.lower())
            move = CACHE.get_move_from_cache(move_name)
            battle_moves.append(BattleMove(move))

        return battle_moves

    def get_move(self, move_name: str) -> BattleMove:
        """Obtém um BattleMove pelo nome."""
        for battle_move in self.battle_moves:
            if battle_move.move.name == move_name:
                return battle_move
        raise ValueError(f"Move {move_name} not found in battle moves.")

    def reset_stat_changes(self):
        for change in self.stat_stages:
            self.stat_stages[change] = 0
        for stat in self.stats:
            self.stats[stat] = self.pokemon.raw_stats[stat]

    def __str__(self):
        return f"{self.pokemon.name} - HP: {self.current_hp}/{self.hp_total} - Status: {self.status if self.status else 'Healthy'}"

    def apply_stat_stage(self, stat_name: str, stages: int):
        """Aplica mudança de stat ao Pokémon."""
        if self.stat_stages[stat_name] == 6:
            print(f'{self.pokemon.name} {stat_name} cant go any higher.')
        elif self.stat_stages[stat_name] == -6:
            print(f'{self.pokemon.name} {stat_name} cant go any lower.')
        else:
            if stat_name in self.stat_stages:
                self.stat_stages[stat_name] += stages
                # Limitar mudanças de stat entre -6 e +6
                self.stat_stages[stat_name] = max(-6, min(6, self.stat_stages[stat_name]))
            else:
                raise ValueError(f"Stat {stat_name} does not exist.")

    def get_stat(self, stat_name: str):
        """Obtém o valor atual de uma stat, considerando as mudanças de stat."""
        stage = self.stat_stages.get(stat_name, 0)
        multiplier = stage_multipliers.get(stage, 1.0)
        base_stat = self.pokemon.raw_stats.get(stat_name, 0)
        return math.floor(base_stat * multiplier)

    def get_raw_stat(self, stat_name: str):
        """Obtém o valor base (raw) de uma stat, sem considerar mudanças de stat."""
        return self.pokemon.raw_stats.get(stat_name, 0)

    def apply_status(self, status: Status):
        if self.is_status:
            print(f'{self.pokemon.name} already has a status condition.')
        else:
            self.status = status

    def set_effect(self, effect: Effect):
        self.effects.append(effect)

    def is_status(self):
        return True if self.status is not None else False

    def get_higher_atk_stat(self):
        """Retorna a stat de ataque mais alta (atk ou spa)"""
        atk = self.get_stat('atk')
        spa = self.get_stat('spa')
        if atk > spa:
            return 'atk'
        elif atk < spa:
            return 'spa'
        else:
            return random.choice(['atk', 'spa'])

    def tranform(self, transformation: Transformation):
        pass # TODO

    def get_types(self):
        return self.pokemon.pkm.types

