from unittest import skip

from pkm_sim.battle_env.entities.field import Field
from pkm_sim.battle_env.turn import Turn, Action
from test_battle import *
from utils import ActionType

team_a = [pkm_1, pkm_2, pkm_3, pkm_4, pkm_5, pkm_6]
team_b = [pkm_7, pkm_8, pkm_9, pkm_10, pkm_11, pkm_12]
def test_turn_execution():

    field = Field(
        bench_pkm=[[pkm_3, pkm_4], [pkm_9, pkm_10]],
        active_pkm=[[pkm_1, pkm_2], [pkm_7, pkm_8]]
    )

    turn = Turn(
        0, field,
        actions=[
            Action(user_slot=field.slots[0][0], action_type=ActionType.SWITCH, switch_in=pkm_4),
            Action(user_slot=field.slots[0][1], action_type=ActionType.ATTACK, battle_move=field.slots[0][1].pokemon.get_move('spore'), target_slot=[field.slots[1][0]]),
            Action(user_slot=field.slots[1][0], action_type=ActionType.ATTACK, battle_move=field.slots[1][0].pokemon.get_move('make-it-rain'), target_slot=[field.slots[0][0], field.slots[0][1]]),
            Action(user_slot=field.slots[1][1], action_type=ActionType.SWITCH, switch_in=pkm_10),
        ]
    )
    turn.execute_turn()
    assert field.slots[0][0].pokemon.get_name() is pkm_4.get_name()
    assert pkm_1.current_hp == pkm_1.hp_total
    assert pkm_2.current_hp < pkm_2.hp_total
    assert pkm_4.current_hp < pkm_4.hp_total
    assert pkm_1.current_hp == pkm_1.hp_total




# =============================================================================
# NOVOS TESTES: Integração de BattleMove e 5 Fases de Turno
# =============================================================================

from unittest.mock import MagicMock
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.move import BattleMove
from api.models import Move

@skip(reason='Feito por IA, nao visto')
class TestTurnPhases:
    """Testes para as 5 fases de turno"""

    @skip(reason='Feito por IA, nao visto')
    def setup_method(self):
        """Setup para cada teste"""
        # Criar campo
        self.field = Field()

        # Criar dois Pokémon mocks
        self.pokemon1 = self._create_mock_battle_pokemon("Pikachu", spd=95)
        self.pokemon2 = self._create_mock_battle_pokemon("Charizard", spd=100)

        # Colocar no field
        self.field.slot_pkm = [[self.pokemon1, None], [self.pokemon2, None]]

    @skip(reason='Feito por IA, nao visto')
    def _create_mock_battle_pokemon(self, name: str, spd: int = 50):
        """Helper para criar BattlePokemon mock"""
        mock_pokemon = MagicMock(spec=BattlePokemon)
        mock_pokemon.pokemon.name = name
        mock_pokemon.pokemon.base_stats = {
            'hp': 100, 'atk': 100, 'def': 100,
            'spatk': 100, 'spdef': 100, 'spd': spd
        }
        mock_pokemon.pokemon.types = ['electric']
        mock_pokemon.current_hp = 100
        mock_pokemon.hp_total = 100
        mock_pokemon.is_fainted.return_value = False
        mock_pokemon.stat_changes = {'acc': 0, 'eva': 0}
        return mock_pokemon

    @skip(reason='Feito por IA, nao visto')
    def test_turn_initialization(self):
        """Testa inicialização de Turn"""
        actions = []
        turn = Turn(turn_number=1, field_state=self.field, actions=actions)

        assert turn.turn_number == 1
        assert turn.field_state == self.field
        assert turn.actions == actions

    @skip(reason='Feito por IA, nao visto')
    def test_order_actions_for_moves(self):
        """Testa ordenação de ações de moves"""
        # Criar dois moves com prioridades diferentes
        mock_move1 = MagicMock(spec=Move)
        mock_move1.name = "Quick Attack"
        mock_move1.priority = 1  # prioridade maior

        mock_move2 = MagicMock(spec=Move)
        mock_move2.name = "Thunderbolt"
        mock_move2.priority = 0  # prioridade menor

        battle_move1 = BattleMove(mock_move1)
        battle_move2 = BattleMove(mock_move2)

        # Criar ações
        action1 = Action(
            player=0, user=self.pokemon1, battle_move=battle_move2,
            switch=None, transformation=None, action_type='attack', target=1
        )
        action2 = Action(
            player=1, user=self.pokemon2, battle_move=battle_move1,
            switch=None, transformation=None, action_type='attack', target=0
        )

        turn = Turn(turn_number=1, field_state=self.field, actions=[action1, action2])

        # Ordenar
        ordered = turn.order_actions_for_moves()

        # Quick Attack (prioridade 1) deve vir primeiro
        assert ordered[0].battle_move.move.name == "Quick Attack"
        assert ordered[1].battle_move.move.name == "Thunderbolt"

    @skip(reason='Feito por IA, nao visto')
    def test_execute_turn_structure(self):
        """Testa que execute_turn retorna estrutura correta"""
        actions = []
        turn = Turn(turn_number=1, field_state=self.field, actions=actions)

        result = turn.execute_turn()

        # Verificar estrutura do resultado
        assert isinstance(result, dict)
        assert 'turn_number' in result
        assert 'switches' in result
        assert 'transformations' in result
        assert 'moves' in result
        assert 'fainting' in result
        assert 'end_of_turn_effects' in result
        assert result['turn_number'] == 1
