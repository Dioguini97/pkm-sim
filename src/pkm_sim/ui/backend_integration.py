"""
Backend integration REAL para pkm_sim.

Este ficheiro faz a ponte entre a UI do Pygame e a tua lógica de batalha.
Usa a tua classe Battle para gerir tudo!
"""
from typing import List, Dict, Any, Optional
import uuid

# Imports do teu backend
from pkm_sim.battle_env.entities.field import Field, BattleSlot
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.move import BattleMove
from pkm_sim.battle_env.turn import Turn, Action
from pkm_sim.battle_env.battle import Battle
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon
from utils import ActionType


class BattleBackend:
    """
    Interface entre a UI do Pygame e o teu sistema de batalha.

    Usa a tua classe Battle para gerir o estado e executar turnos.
    """

    def __init__(self):
        self.active_battles: Dict[str, Dict[str, Any]] = {}

    def create_battle(
            self,
            player_party: List[BattlePokemon],
            opponent_party: List[BattlePokemon],
            player_team_order: Optional[List[int]] = None,
            opponent_team_order: Optional[List[int]] = None
    ) -> str:
        """
        Cria uma nova batalha usando a tua classe Battle.

        Args:
            player_party: Lista completa de BattlePokemon do jogador (até 6)
            opponent_party: Lista completa de BattlePokemon do oponente (até 6)
            player_team_order: Ordem dos 4 Pokémon que vão batalhar [0,1,2,3]
            opponent_team_order: Ordem dos 4 Pokémon do oponente

        Returns:
            battle_id: UUID da batalha criada
        """
        battle_id = str(uuid.uuid4())

        # Criar Battle com as parties completas (6 pokemon cada)
        battle = Battle(parties=[player_party, opponent_party])

        # Se ordem específica foi fornecida, sobrescrever
        if player_team_order is not None:
            battle.teams[0] = [player_party[i] for i in player_team_order[:4]]
        if opponent_team_order is not None:
            battle.teams[1] = [opponent_party[i] for i in opponent_team_order[:4]]

        # Configurar Field inicial com os 2 primeiros de cada team
        battle.field.slots[0][0].pokemon = battle.teams[0][0]
        battle.field.slots[0][1].pokemon = battle.teams[0][1] if len(battle.teams[0]) > 1 else None
        battle.field.slots[1][0].pokemon = battle.teams[1][0]
        battle.field.slots[1][1].pokemon = battle.teams[1][1] if len(battle.teams[1]) > 1 else None

        # Configurar bench (restantes pokemon)
        battle.field.bench_pkm = [
            battle.teams[0][2:],  # Player bench
            battle.teams[1][2:]  # Opponent bench
        ]

        # Guardar estado da batalha
        self.active_battles[battle_id] = {
            'battle': battle,
            'battle_log': [],
            'winner': None
        }

        return battle_id

    def execute_turn(
            self,
            battle_id: str,
            player_actions: List[Dict[str, Any]],
            opponent_actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Executa um turno completo da batalha.

        Args:
            battle_id: ID da batalha
            player_actions: Lista de ações do jogador
                [{'action_type': 'move', 'user_slot': (0,0), 'move_name': 'tackle', 'target_slots': [(1,0)]}]
            opponent_actions: Lista de ações do oponente

        Returns:
            result: Dicionário com resultado do turno
        """
        battle_wrapper = self.active_battles[battle_id]
        battle = battle_wrapper['battle']

        # Converter ações do UI para objetos Action
        actions = []

        # Processar ações do jogador
        for action_dict in player_actions:
            action = self._create_action_from_dict(action_dict, battle.field)
            if action:
                actions.append(action)

        # Processar ações do oponente
        for action_dict in opponent_actions:
            action = self._create_action_from_dict(action_dict, battle.field)
            if action:
                actions.append(action)

        # Criar Turn e executar usando o teu sistema
        battle.number_of_turns += 1
        turn = Turn(
            turn_number=battle.number_of_turns,
            field_state=battle.field,
            actions=actions
        )

        # Executar turno
        turn_result = turn.execute_turn()

        # Processar resultado e converter para formato UI
        result = self._process_turn_result(battle_id, turn_result)

        # Verificar se batalha terminou usando método do Battle
        if battle.is_battle_over():
            result['battle_ended'] = True
            # Determinar vencedor
            if battle.have_all_fainted(battle.teams[0]):
                result['winner'] = 'opponent'
                battle_wrapper['winner'] = 'opponent'
            else:
                result['winner'] = 'player'
                battle_wrapper['winner'] = 'player'

        return result
        result['winner'] = battle['winner']

        return result


    def _create_action_from_dict(
        self,
        action_dict: Dict[str, Any],
        field: Field
    ) -> Optional[Action]:
        """
        Converte dicionário de ação da UI para objeto Action.

        action_dict format:
            {
                'action_type': 'move' | 'switch',
                'user_slot': (side, index),
                'move_name': str,  # para moves
                'target_slots': [(side, index), ...],  # para moves
                'switch_in': BattlePokemon  # para switches
            }
        """
        action_type_str = action_dict['action_type']
        user_side, user_index = action_dict['user_slot']
        user_slot = field.slots[user_side][user_index]

        if action_type_str == 'move':
            # Encontrar BattleMove
            move_name = action_dict['move_name']
            battle_move = user_slot.pokemon.get_move(move_name)

            # Encontrar targets
            target_slots = []
            for target_side, target_index in action_dict['target_slots']:
                target_slot = field.slots[target_side][target_index]
                target_slots.append(target_slot)

            return Action(
                user_slot=user_slot,
                action_type=ActionType.MOVE,
                battle_move=battle_move,
                target_slot=target_slots
            )

        elif action_type_str == 'switch':
            switch_in = action_dict['switch_in']
            return Action(
                user_slot=user_slot,
                action_type=ActionType.SWITCH,
                switch_in=switch_in
            )

        return None


    def _process_turn_result(
            self,
            battle_id: str,
            turn_result: dict
    ) -> Dict[str, Any]:
        """
        Processa resultado do turno e converte para formato da UI.
        """
        battle = self.active_battles[battle_id]
        messages = []
        hp_changes = []
        status_changes = []
        fainted = []

        # Processar switches
        for switch in turn_result.get('switches', []):
            messages.append(switch)

        # Processar moves
        for move_result in turn_result.get('moves', []):
            # Adicionar mensagens do move
            if 'messages' in move_result:
                messages.extend(move_result['messages'])

            # Registrar mudanças de HP
            if 'hp_change' in move_result:
                hp_changes.append(move_result['hp_change'])

        # Processar Pokémon desmaiados
        for faint_msg in turn_result.get('fainting', []):
            messages.append(faint_msg)
            fainted.append(faint_msg)

        # Guardar no log da batalha
        battle_wrapper = self.active_battles[battle_id]
        battle_wrapper['battle_log'].extend(messages)

        return {
            'messages': messages,
            'hp_changes': hp_changes,
            'status_changes': status_changes,
            'fainted': fainted,
            'battle_ended': False,
            'winner': None
        }


    def get_battle_state(self, battle_id: str) -> Dict[str, Any]:
        """
        Retorna o estado completo da batalha para a UI.

        Returns:
            {
                'player_active': [BattlePokemon, ...],
                'opponent_active': [BattlePokemon, ...],
                'player_bench': [BattlePokemon, ...],
                'opponent_bench': [BattlePokemon, ...],
                'field_conditions': {...},
                'turn_number': int,
                'battle_log': [str, ...]
            }
        """
        battle_wrapper = self.active_battles[battle_id]
        battle = battle_wrapper['battle']
        field = battle.field

        return {
            'player_active': [
                slot.pokemon for slot in field.slots[0]
                if not slot.is_empty()
            ],
            'opponent_active': [
                slot.pokemon for slot in field.slots[1]
                if not slot.is_empty()
            ],
            'player_bench': field.bench_pkm[0],
            'opponent_bench': field.bench_pkm[1],
            'field_conditions': {
                'weather': field.weather,
                'terrain': field.terrain,
                'gravity': field.gravity,
                'trick_room': field.trick_room,
                'side_conditions': field.side_conditions
            },
            'turn_number': battle.number_of_turns,
            'battle_log': battle_wrapper['battle_log']
        }


    def switch_pokemon(
            self,
            battle_id: str,
            side: int,
            slot_index: int,
            pokemon_to_switch_in: BattlePokemon
    ) -> Dict[str, Any]:
        """
        Troca um Pokémon no meio da batalha (forçada, ex: após desmaio).

        Returns:
            {'success': bool, 'message': str}
        """
        battle_wrapper = self.active_battles[battle_id]
        battle = battle_wrapper['battle']

        # Usar método switch do Battle
        team_ind = side
        # Encontrar index do pokemon no team
        slot_ind = slot_index

        battle.switch_pokemon(team_ind, slot_ind, pokemon_to_switch_in)

        return {
            'success': True,
            'message': f'Go, {pokemon_to_switch_in.pokemon.name}!'
        }


    def get_available_moves(
            self,
            battle_id: str,
            side: int,
            slot_index: int
    ) -> List[Dict[str, Any]]:
        """
        Retorna lista de moves disponíveis para um Pokémon.

        Returns:
            [{'name': str, 'pp': int, 'max_pp': int, 'type': str, 'power': int}, ...]
        """
        battle_wrapper = self.active_battles[battle_id]
        battle = battle_wrapper['battle']
        pokemon = battle.field.slots[side][slot_index].pokemon

        if not pokemon:
            return []

        moves = []
        for battle_move in pokemon.battle_moves:
            moves.append({
                'name': battle_move.move.name,
                'pp': battle_move.pp_remaining,
                'max_pp': battle_move.move.pp,
                'type': battle_move.move.move_type,
                'power': battle_move.move.power,
                'accuracy': battle_move.move.accuracy,
                'category': battle_move.move.damage_class
            })

        return moves


class PokemonDatabase:
    """
    Interface para criar e gerir Pokémon.
    """

    def __init__(self):
        pass

    def create_pokemon_instance(
            self,
            species: str,
            level: int,
            moves: List[str],
            ability: Optional[str] = None,
            nature: Optional[str] = None,
            evs: Optional[Dict[str, int]] = None,
            ivs: Optional[Dict[str, int]] = None,
            item: Optional[str] = None
    ) -> BattlePokemon:
        """
        Cria uma instância de BattlePokemon.

        Args:
            species: Nome do Pokémon (ex: 'pikachu')
            level: Nível do Pokémon
            moves: Lista de nomes de moves
            ability: Nome da ability
            nature: Nome da nature
            evs: Dicionário de EVs {'hp': 252, 'atk': 252, ...}
            ivs: Dicionário de IVs {'hp': 31, 'atk': 31, ...}
            item: Nome do item segurado

        Returns:
            BattlePokemon pronto para batalha
        """
        # Valores default
        if evs is None:
            evs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}
        if ivs is None:
            ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}

        # Criar CompetitivePokemon
        comp_pokemon = CompetitivePokemon(
            level=level,
            moves=moves,
            ability=ability,
            nature=nature,
            evs=evs,
            ivs=ivs,
            item=item,
            name=species
        )

        # Criar BattlePokemon
        battle_pokemon = BattlePokemon(comp_pokemon)

        return battle_pokemon

    def pokemon_to_dict(self, pokemon: BattlePokemon) -> Dict[str, Any]:
        """
        Converte BattlePokemon para dicionário para a UI.
        """
        return {
            'id': id(pokemon),  # Usar ID do objeto como identificador único
            'species': pokemon.pokemon.pkm.name,
            'name': pokemon.pokemon.name,
            'level': pokemon.pokemon.level,
            'current_hp': pokemon.current_hp,
            'max_hp': pokemon.hp_total,
            'stats': {
                'hp': pokemon.hp_total,
                'atk': pokemon.stats['atk'],
                'def': pokemon.stats['def'],
                'spa': pokemon.stats['spa'],
                'spd': pokemon.stats['spd'],
                'spe': pokemon.stats['spe']
            },
            'types': pokemon.pokemon.pkm.types,
            'ability': pokemon.pokemon.ability,
            'nature': pokemon.pokemon.nature,
            'item': pokemon.pokemon.item,
            'status': pokemon.status.name if pokemon.status else None,
            'moves': [
                {
                    'name': bm.move.name,
                    'type': bm.move.move_type,
                    'category': bm.move.damage_class,
                    'power': bm.move.power,
                    'accuracy': bm.move.accuracy,
                    'pp': bm.pp_remaining,
                    'max_pp': bm.move.pp
                }
                for bm in pokemon.battle_moves
            ]
        }

    def get_all_pokemon_species(self) -> List[str]:
        """
        Retorna lista de todas as espécies de Pokémon disponíveis.

        TODO: Implementar baseado na tua fonte de dados (API, cache, etc)
        """
        # Placeholder - substitui com tua implementação real
        return [
            'pikachu', 'charizard', 'blastoise', 'venusaur',
            'gengar', 'dragonite', 'mewtwo', 'snorlax'
        ]


# Singleton instances
_battle_backend = BattleBackend()
_pokemon_db = PokemonDatabase()


def get_battle_backend() -> BattleBackend:
    """Obtém instância singleton do battle backend."""
    return _battle_backend


def get_pokemon_database() -> PokemonDatabase:
    """Obtém instância singleton do pokemon database."""
    return _pokemon_db


# Helper functions para conversão UI <-> Backend
def create_mock_team(species_list: List[str]) -> List[BattlePokemon]:
    """
    Cria uma equipa mock para testes.

    Args:
        species_list: Lista de espécies de Pokémon

    Returns:
        Lista de BattlePokemon
    """
    db = get_pokemon_database()
    team = []

    for species in species_list:
        pokemon = db.create_pokemon_instance(
            species=species,
            level=50,
            moves=['tackle', 'quick-attack', 'thunder-shock', 'iron-tail'],
            nature='jolly',
            evs={'hp': 252, 'spe': 252, 'atk': 4}
        )
        team.append(pokemon)

    return team


def battle_pokemon_to_ui_dict(pokemon: BattlePokemon) -> Dict[str, Any]:
    """
    Converte BattlePokemon para formato esperado pela UI.
    """
    db = get_pokemon_database()
    return db.pokemon_to_dict(pokemon)