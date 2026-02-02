from __future__ import annotations
import math
import random
from calendar import day_abbr
from typing import TYPE_CHECKING

from api.models import Move
from pkm_sim.battle_env import damage_calculation
from pkm_sim.battle_env.entities.status import Status
from utils import get_type_effectiveness, stage_multipliers_acc_eva, MoveTarget

if TYPE_CHECKING:
    from pkm_sim.battle_env.entities.field import BattleSlot



class BattleMove:
    """
    Representa um Move durante uma batalha.
    Similar a BattlePokemon, encapsula o estado dinâmico (PP restante)
    e fornece métodos para executar efeitos do move no combate.
    """

    def __init__(self, move: Move):
        self.move = move  # Dados estáticos do move
        self.pp_remaining = self.max_pp(move.pp ) # PP consumível durante a batalha
        self.atk_stat_used = self.get_atk_stat_used()
        self.def_stat_used = self.get_def_stat_used()
        self.stat_changes = self.stat_changes()

    def __repr__(self):
        return f"BattleMove({self.move.name}, PP: {self.pp_remaining}/{self.move.pp})"

    def __str__(self):
        return f"{self.move.name} ({self.pp_remaining}/{self.move.pp})"

    def consume_pp(self, amount: int = 1):
        """Consome PP do move. Retorna True se conseguiu consumir."""
        if self.pp_remaining >= amount | self.move.pp > 0:
            self.pp_remaining = max(self.pp_remaining - amount, 0)
        else:
            raise Exception(f"Not enough PP to consume for move {self.move.name}.")

    def restore_pp(self, amount: int):
        """Restaura PP do move até ao máximo."""
        self.pp_remaining = min(self.move.pp, self.pp_remaining + amount)

    def reset_pp(self):
        """Restaura PP ao máximo."""
        self.pp_remaining = self.move.pp

    def get_accuracy(self):
        """Retorna a accuracy do move."""
        return self.move.accuracy

    def get_atk_stat_used(self):
        """Retorna a stat usada para ataque do move."""
        if self.move.damage_class == 'special':
            return 'spa'
        elif self.move.damage_class == 'physical':
            if self.move.name in ['body-press']:
                return 'def'
            return 'atk'
        else:
            return None

    def get_def_stat_used(self):
        """Retorna a stat usada para defesa do move."""
        if self.move.damage_class == 'special':
            if self.move.name in ['psyshock', 'psystrike']:
                return 'def'
            return 'spd'
        elif self.move.damage_class == 'physical':
            return 'def'
        else:
            return None

    def calculate_power(self):
        """Retorna o poder do move."""
        if self.move.power is not None:
            return self.move.power
        else:
            pass #TODO: implementar casos especiais de power (e.g., Eruption, Flail, etc)

    def have_ailment(self):
        """Retorna se o move pode causar um status condition."""
        return self.move.ailment != 'none'

    def stat_changes(self):
        changes = {}
        if self.move.category == 'damage+raise':
            changes['user'] = self.move.stat_changes
        if self.move.category == 'damage+lower':
            changes['target'] = self.move.stat_changes
        return changes

    # def _check_move_accuracy(self, user, target) -> bool:
    #     """Verifica se o move acerta baseado em accuracy e evasion."""
    #     if self.move.accuracy is None:
    #         return True  # Moves com accuracy None sempre acertam
    #     micle_berry = 1
    #     modifier = 1
    #
    #     # Calcular modificador de accuracy baseado em stages
    #     acc_stage = user.stat_changes.get('acc', 0)
    #     eva_stage = target.stat_changes.get('eva', 0)
    #
    #     # Limitar stages entre -6 e 6
    #     stage_diff = max(-6, min(6, acc_stage - eva_stage))
    #
    #     # Aplicar multiplicador de stage (importado de utils)
    #     stage_multiplier = stage_multipliers_acc_eva.get(stage_diff, 1.0)
    #
    #
    #     micle_berry = 1.2 if user.pokemon.item == 'micle-berry' else 1.0
    #     # TODO : verificar se a berry ja foi usada, pois este boost so se aplica com o seu consumo e uma unica vez no proximo move
    #     # TODO modifier, e.g., weather effects, abilities, etc snow cloak
    #
    #     modified_accuracy = self.move.accuracy * stage_multiplier * micle_berry
    #
    #     # Verificar hit
    #     return random.randint(1, 100) <= math.floor(modified_accuracy)
    #

    def _calculate_damage(self, user, target, field) -> int:
        """Calcula o dano do move.
        user: BattleSlot
        target: BattlePokemon
        field: Field
        """
        # Se move não tem poder, retorna 0 (move de status ou sem efeito de dano)
        move_power = self.calculate_power()

        critical_hit = self._is_critical_hit(user.pokemon.stat_stages['crit'] + self.move.crit_rate)

        if critical_hit:
            attacker_stat = max(user.pokemon.stats[self.get_atk_stat_used()], user.pokemon.pokemon.raw_stats[self.get_atk_stat_used()])
            defender_stat = min(target.stats[self.get_def_stat_used()], target.pokemon.raw_stats[self.get_def_stat_used()])
        else:
            attacker_stat = user.pokemon.stats[self.get_atk_stat_used()]
            defender_stat = target.stats[self.get_def_stat_used()]

        # Verficar se é Physical e se está burned
        burn = 1
        if self.move.damage_class == 'physical' and user.status == Status.BURN:
            burn = 0.5

        # Calcular multiplicadores
        target_multiplier = self._calculate_target_multiplier(user, field)

        stab = 1.5 if self.move.move_type in user.pokemon.get_types() else 1.0

        # Type effectiveness
        type_multiplier = 1.0
        for target_type in target.get_types():
            type_multiplier *= get_type_effectiveness(self.move.move_type, target_type)

        # Aplicar cálculo de dano
        damage = damage_calculation(
            attacker_stat=attacker_stat,
            defender_stat=defender_stat,
            move_power=move_power,
            targets=target_multiplier,
            PB=1,
            weather=1,
            GLAIVE_RUSH=1,
            critical_hit=critical_hit,
            stab=stab,
            type_=type_multiplier,
            burn=burn,
            other=1,
            z_move=1
        )

        print(f'The {user.pokemon.get_name()} used {self.move.name} on {target.get_name()}')
        print(f'Used is {attacker_stat} in target\'s {defender_stat} with {move_power} power and a target multiplier of {target_multiplier}.')
        print(f'Critical? {critical_hit} with {stab} stab power and {type_multiplier} effectiveness')
        print(f'Did {damage} damage')


        return max(1, damage)

    def _calculate_target_multiplier(self, user: BattleSlot, field):
        if self.move.target in [MoveTarget.ALL_OPPONENTS.value, MoveTarget.ALL_OTHER_POKEMON.value]: # Spread moves
            user_side_number = field.get_ally_is_fainted_int(user.side, user.index)
            foe_side_number = field.get_foe_effective_slot_number(user.side)
            if self.move.target == MoveTarget.ALL_OTHER_POKEMON.value:
                return 1 if user_side_number + foe_side_number == 1 else 0.75
            else:
                return 1 if foe_side_number == 1 else 0.75
        else:
            return 1
    #
    # def _apply_ailment(self):
    #     pass
    #
    # def _apply_secondary_effects(self, user, target, field: Field, result: dict):
    #     # TODO deve ser para apagar
    #     """Aplica efeitos secundários do move (stat changes, ailments, etc)."""
    #     # Aplicar stat changes
    #     if self.move.stat_changes:
    #         for stat_change in self.move.stat_changes:
    #             if random.randint(1, 100) <= self.move.effect_chance:
    #                 stat_name, stages = stat_change
    #                 self._apply_stat_change(target, stat_name, stages, result)
    #
    #     # Aplicar status condition (ailment)
    #     if self.move.ailment != 'none' and self.move.ailment is not None:
    #         if random.randint(1, 100) <= self.move.ailment_chance:
    #             self._apply_status_condition(target, self.move.ailment, result)
    #
    # def _apply_drain_effect(self, user, damage: int, result: dict):
    #     """Aplica efeito de drain (e.g., Leech Seed, Giga Drain)."""
    #     drain_amount = max(1, (damage * self.move.drain) // 100)
    #     user.heal(drain_amount)
    #     result['effects_applied'].append(f"{user.pokemon.name} recovered {drain_amount} HP!")
    #
    # def _apply_healing_effect(self, user, result: dict):
    #     """Aplica efeito de healing (e.g., Recover, Roost)."""
    #     heal_amount = max(1, (user.hp_total * self.move.healing) // 100)
    #     user.heal(heal_amount)
    #     result['effects_applied'].append(f"{user.pokemon.name} recovered {heal_amount} HP!")
    #
    # def _apply_stat_change(self, user, target, result: dict):
    #     """Aplica mudança de stat ao alvo."""
    #     if self.move.category == 'damage+raise': # Move que dá damage ao target mas afeta as stats do user
    #         user.apply_stat_change()
    #
    # def _apply_status_condition(self, target, condition: str, result: dict):
    #     """Aplica status condition ao alvo."""
    #     target.status_conditions = condition
    #     result['effects_applied'].append(
    #         f"{target.pokemon.name} was hit with {condition}!"
    #     )
    #
    # def _execute_status_move(self, user, target, field: Field, result: dict) -> dict:
    #     """Executa um move de status (sem dano)."""
    #     result['success'] = True
    #     result['message'] = f"{user.pokemon.name} used {self.move.name}!"
    #
    #     # Aplicar efeitos de move de status
    #     # TODO: implementar lógica específica para moves de status
    #     # (setup moves, field setters, etc)
    #
    #     self.consume_pp()
    #     return result
    #
    def _is_critical_hit(self, critical_stage: int) -> bool:
        # Critical hit stages and their corresponding probabilities
        critical_hit_chances = {
            -1: 0,
            0: 1 / 24,  # ~4.17%
            1: 1 / 8,  # 12.5%
            2: 1 / 2,  # 50%
            3: 1.0  # 100%
        }
        chance = critical_hit_chances.get(critical_stage, 1 / 24)
        return random.random() < chance

    def _execute(self, user: BattleSlot, target: BattleSlot, field):

        if (self.move.min_hits is None) & (self.move.max_hits is None):
            damage = self._calculate_damage(user, target.pokemon, field)
            return damage
        else: # multi hits moves
            for hit in range(self.move.min_hits, self.move.max_hits):
                damage = self._calculate_damage(user.pokemon, target.pokemon, field)
                target.pokemon.apply_damage(damage) # Pode ter que se mudar por causa de multi hit moves


    def max_pp(self, raw_pp: int):
        return math.floor(self.move.pp * 1.6)