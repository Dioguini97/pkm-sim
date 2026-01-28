"""
Teste básico para validar a arquitetura Move/BattleMove
"""
import pytest
from unittest.mock import MagicMock
from api.models import Move
from pkm_sim.battle_env.entities.move import BattleMove
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon


class TestBattleMove:
    """Testes para a classe BattleMove"""

    def test_battlemove_initialization(self):
        """Testa inicialização de BattleMove"""
        # Mock de Move
        mock_move = MagicMock(spec=Move)
        mock_move.name = "Thunderbolt"
        mock_move.pp = 15
        mock_move.power = 90
        mock_move.accuracy = 100
        mock_move.priority = 0

        # Criar BattleMove
        battle_move = BattleMove(mock_move)

        assert battle_move.move == mock_move
        assert battle_move.pp_remaining == 15
        assert str(battle_move) == "Thunderbolt (15/15)"

    def test_consume_pp(self):
        """Testa consumo de PP"""
        mock_move = MagicMock(spec=Move)
        mock_move.name = "Thunderbolt"
        mock_move.pp = 15

        battle_move = BattleMove(mock_move)

        # Consumir 1 PP
        assert battle_move.consume_pp(1) == True
        assert battle_move.pp_remaining == 14

        # Consumir mais PP
        assert battle_move.consume_pp(5) == True
        assert battle_move.pp_remaining == 9

        # Consumir quando não há PP suficiente
        assert battle_move.consume_pp(20) == False
        assert battle_move.pp_remaining == 9

    def test_restore_and_reset_pp(self):
        """Testa restauração de PP"""
        mock_move = MagicMock(spec=Move)
        mock_move.name = "Thunderbolt"
        mock_move.pp = 15

        battle_move = BattleMove(mock_move)
        battle_move.consume_pp(10)
        assert battle_move.pp_remaining == 5

        # Restaurar 3 PP
        battle_move.restore_pp(3)
        assert battle_move.pp_remaining == 8

        # Reset completo
        battle_move.reset_pp()
        assert battle_move.pp_remaining == 15


class TestBattlePokemonWithBattleMove:
    """Testes para integração BattlePokemon com BattleMove"""

    def test_get_move_returns_battlemove(self):
        """Testa que get_move retorna BattleMove"""
        # Mock de CompetitivePokemon com moves
        mock_cpokemon = MagicMock(spec=CompetitivePokemon)
        mock_cpokemon.name = "Pikachu"
        mock_cpokemon.base_stats = {
            'hp': 35, 'atk': 55, 'def': 40,
            'spatk': 50, 'spdef': 50, 'spd': 90
        }
        mock_cpokemon.types = ['electric']
        mock_cpokemon.moves = []

        # Criar BattlePokemon e injetar battle_moves
        battle_pokemon = BattlePokemon(mock_cpokemon)

        # Mock Move e BattleMove
        mock_move = MagicMock(spec=Move)
        mock_move.name = "Thunderbolt"
        mock_move.pp = 15

        battle_move = BattleMove(mock_move)
        battle_pokemon.battle_moves = [battle_move]

        # Testar get_move
        retrieved_move = battle_pokemon.get_move("Thunderbolt")
        assert isinstance(retrieved_move, BattleMove)
        assert retrieved_move.move.name == "Thunderbolt"

    def test_get_move_raises_error(self):
        """Testa que get_move levanta erro para move inexistente"""
        mock_cpokemon = MagicMock(spec=CompetitivePokemon)
        mock_cpokemon.base_stats = {
            'hp': 35, 'atk': 55, 'def': 40,
            'spatk': 50, 'spdef': 50, 'spd': 90
        }
        mock_cpokemon.types = ['electric']
        mock_cpokemon.moves = []

        battle_pokemon = BattlePokemon(mock_cpokemon)
        battle_pokemon.battle_moves = []

        with pytest.raises(ValueError):
            battle_pokemon.get_move("NonexistentMove")


class TestActionIntegration:
    """Testes para integração de Action com BattleMove"""

    def test_action_with_battlemove(self):
        """Testa criação de Action com BattleMove"""
        from pkm_sim.battle_env.turn import Action

        # Mock de BattlePokemon
        mock_user = MagicMock(spec=BattlePokemon)
        mock_user.pokemon.name = "Pikachu"

        # Mock de BattleMove
        mock_move = MagicMock(spec=Move)
        mock_move.name = "Thunderbolt"

        battle_move = BattleMove(mock_move)

        # Criar Action
        action = Action(
            player=0,
            user=mock_user,
            battle_move=battle_move,
            switch=None,
            transformation=None,
            action_type='attack',
            target=1
        )

        assert action.battle_move == battle_move
        assert action.player == 0
        assert action.action_type == 'attack'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
