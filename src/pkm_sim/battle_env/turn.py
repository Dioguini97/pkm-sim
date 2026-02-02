from __future__ import annotations
from pkm_sim.battle_env.entities.field import Field, BattleSlot
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.move import BattleMove
from utils import ActionType, Transformation, DamageClass


class Action:
    def __init__(self, user_slot: BattleSlot | None, action_type: ActionType,
                 battle_move: BattleMove | None = None, target_slot: list[BattleSlot] | None = None,
                 switch_in: BattlePokemon | None = None, transformation: Transformation | None = None):
        self.user_slot = user_slot
        self.action_type = action_type
        self.battle_move = battle_move  # Agora é BattleMove em vez de Move
        self.target_slot = target_slot
        self.transformation = transformation # Tera, Mega, Dynamax, etc.
        self.switch_in = switch_in # Target index in case of multi-target moves (0, 1)

    def __repr__(self):
        move_name = self.battle_move.move.name if self.battle_move else "None"
        return f"Action(Player: {self.player}, User: {self.user.pokemon.name if self.user else 'None'}, Move: {move_name})"


class Turn:
    def __init__(self, turn_number: int, field_state: Field, actions: list[Action]):
        self.turn_number = turn_number
        self.actions = actions
        self.field_state = field_state

    def __repr__(self):
        return f"Turn({self.turn_number}, Actions: {self.actions})"

    def __str__(self):
        return f"Turn {self.turn_number} with actions: {self.actions}"

    def order_actions_for_moves(self) -> list[Action]:
        """Ordena ações de move por prioridade e velocidade."""
        move_actions = [action for action in self.actions if action.battle_move is not None]
        return sorted(
            move_actions,
            key=lambda action: (
                action.battle_move.move.priority,
                action.user_slot.pokemon.stats['spe']
            ),
            reverse=True
        )

    def order_actions_for_switch(self) -> list[Action]:
        switch_actions = [action for action in self.actions if action.action_type == ActionType.SWITCH]
        return sorted(
            switch_actions,
            key=lambda action: (action.user_slot.pokemon.stats['spe']),
            reverse=True
        )

    def execute_turn(self) -> dict:
        """
        Executa um turno completo com todas as 5 fases.
        Retorna dicionário com resultado do turno.
        """
        results = {
            'turn_number': self.turn_number,
            'switches': [],
            'transformations': [],
            'moves': [],
            'fainting': [],
            'end_of_turn_effects': []
        }

        # Phase 1: Switch Phase (ordenado por velocidade)
        self._execute_switch_phase(results)

        # Phase 2: Transformation Phase (ordenado por velocidade)
        #self._execute_transformation_phase(results)

        # Phase 3: Move Phase (ordenado por prioridade e velocidade)
        self._execute_move_phase(results)

        # Phase 4: Fainting Phase (remover Pokémon desmaiados em ordem de velocidade)
        #self._execute_fainting_phase(results)

        # Phase 5: End-of-Turn Effects Phase (aplicar efeitos finais do turno)
        #self._execute_end_of_turn_phase(results)

        return results

    def _execute_switch_phase(self, results: dict):
        """Phase 1: Executa trocas de Pokémon em ordem de velocidade."""
        switch_actions = self.order_actions_for_switch()

        for action in switch_actions:
            self.field_state.switch(action.user_slot, action.switch_in)
            #results['switches'].append(message)

    def _execute_transformation_phase(self):
        """Phase 2: Executa transformações em ordem de velocidade."""
        transform_actions = [action for action in self.actions if action.transformation is not None]
        transform_actions.sort(key=lambda x: x.user.pokemon.base_stats['spd'], reverse=True)

        for action in transform_actions:
            print(f"{action.user.pokemon.name} is transforming into {action.transformation}!")
            # TODO: Aplicar lógica de transformação


    def _execute_move_phase(self, results: dict):
        """Phase 3: Executa moves em ordem de prioridade e velocidade."""
        ordered_move_actions = self.order_actions_for_moves()

        for action in ordered_move_actions:
            if action.battle_move is None:
                continue

            # TODO: Determinar alvo correto baseado em action.target
            # Por agora, assumir alvo é o adversário
            self._execute_move(action)

    def _execute_fainting_phase(self, results: dict):
        """Phase 4: Remove Pokémon desmaiados em ordem de velocidade."""
        fainted_pokemon = []

        # Encontrar Pokémon desmaiados
        for side_index in range(2):
            for slot_index in range(len(self.field_state.slots[side_index])):
                pokemon = self.field_state.slot_pkm[side_index][slot_index]
                if pokemon and pokemon.is_fainted():
                    fainted_pokemon.append((pokemon, side_index, slot_index))

        # Ordenar por velocidade (decrescente)
        fainted_pokemon.sort(
            key=lambda x: x[0].pokemon.base_stats['spd'],
            reverse=True
        )

        # Remover Pokémon desmaiados
        for pokemon, side, slot in fainted_pokemon:
            message = f"{pokemon.pokemon.name} fainted!"
            print(message)
            results['fainting'].append(message)
            self.field_state.slot_pkm[side][slot] = None
            # TODO: Chamar método para desativar ability

    def _execute_end_of_turn_phase(self, results: dict):
        """Phase 5: Aplica efeitos de final de turno (weather, terrain, status)."""
        # TODO: Implementar lógica de end-of-turn effects
        # weather damage, terrain damage, status damage, etc.
        pass

    def _execute_move(self, action: Action):
        move = action.battle_move
        user_slot = action.user_slot

        move.consume_pp() #TODO nao deve consumir se o move não acertar

        for target in action.target_slot:
            if move.move.damage_class == DamageClass.STATUS.value:
                print('Status move')
            else:
                damage = move._execute(user_slot, target, self.field_state)
                target.pokemon.apply_damage(damage)
