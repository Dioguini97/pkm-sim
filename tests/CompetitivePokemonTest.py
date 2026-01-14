import pytest
from src.entities.CompetitivePokemon import CompetitivePokemon

def test_competitive_pokemon_initialization():
    ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spatk': 31, 'spdef': 31, 'spd': 31}
    evs = {'hp': 0, 'atk': 252, 'def': 0, 'spatk': 0, 'spdef': 4, 'spd': 252}
    moves = ['Flamethrower', 'Dragon Claw', 'Air Slash', 'Roost']

    charizard = CompetitivePokemon(
        name="Charizard",
        types=["Fire", "Flying"],
        id=6,
        base_stats={
            'hp': 78,
            'atk': 84,
            'def': 78,
            'spatk': 109,
            'spdef': 85,
            'spd': 100
        },
        abilities=["Blaze", "Solar Power"],
        ability="Blaze",
        item="Charizardite X",
        nature="JOLLY",
        ivs=ivs,
        evs=evs,
        moves=moves,
        level=50
    )

    assert charizard.name == "Charizard"
    assert charizard.types == ["Fire", "Flying"]
    assert charizard.ability == "Blaze"
    assert charizard.item == "Charizardite X"
    assert charizard.nature == "JOLLY"
    assert charizard.ivs == ivs
    assert charizard.evs == evs
    assert charizard.moves == moves
    assert charizard.level == 50

    # Check if stats are calculated correctly (values may vary based on nature and formulas)
    assert charizard.base_stats == {
        'hp': 153,
        'atk': 136,
        'def': 98,
        'spatk': 116,
        'spdef': 106,
        'spd': 167
    }