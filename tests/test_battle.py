import pytest

from data import Cache
from entities import CompetitivePokemon
from pkm_sim.battle_env.battle import Battle
from pkm_sim.battle_env.pokemon import BattlePokemon

cache = Cache()

pika = cache.get_pokemon_from_cache('pikachu')
bulba = cache.get_pokemon_from_cache('bulbasaur')

pkm_1 = BattlePokemon(CompetitivePokemon(
    name=pika.name,
    types=pika.types,
    base_stats=pika.base_stats,
    abilities=pika.abilities,
    id=pika.id,
    height=pika.height,
    weight=pika.weight,
    move_list=pika.move_list,
    img_url=pika.img_url,
    ability="Static",
    item="Light Ball",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["thunderbolt", "quick-attack", "iron-tail", "volt-switch"]
))

pkm_2 = BattlePokemon(CompetitivePokemon(
    name=bulba.name,
    types=bulba.types,
    base_stats=bulba.base_stats,
    abilities=bulba.abilities,
    id=bulba.id,
    height=bulba.height,
    weight=bulba.weight,
    move_list=bulba.move_list,
    img_url=bulba.img_url,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spatk": 252, "spdef": 4, "spd": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

def test_battle_initialization():
    battle = Battle()
    assert battle.turn_number == 0
    assert len(battle.field.slot_pkm) == 2  # Assuming two sides in the battle
    assert all(slot is None for side in battle.field.slot_pkm for slot in side)