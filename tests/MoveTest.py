from api.PokeAPI import PokeAPIService
from src.entities.Move import Move

poke_api_service = PokeAPIService()

def test_should_return_move():
    move = poke_api_service.get_move('body-press')
    assert move.name == 'Body Press'
    assert move.api_name == 'body-press'
    assert move.id == 776
    assert move.power == 80
    assert move.accuracy == 100
    assert move.move_type == 'fighting'
    assert move.effect_chance is None
    assert move.damage_class == 'physical'
    assert move.pp == 10
    assert move.priority == 0
    assert move.stat_changes == []
    assert move.target == 'selected-pokemon'
    assert move.entries.startswith("The user attacks by slamming its body into the target")

def test_should_return_move2():
    move = poke_api_service.get_move('shadow-ball')
    assert move.name == 'Shadow Ball'
    assert move.api_name == 'shadow-ball'
    assert move.id == 247
    assert move.power == 80
    assert move.accuracy == 100
    assert move.move_type == 'ghost'
    assert move.effect_chance == 20
    assert move.damage_class == 'special'
    assert move.pp == 15
    assert move.priority == 0
    assert move.stat_changes == [['spdef', -1]]
    assert move.target == 'selected-pokemon'
    assert move.entries.startswith("An attack that may")