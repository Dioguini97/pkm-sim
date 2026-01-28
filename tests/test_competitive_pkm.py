import pytest
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon


def test_competitive_pokemon_initialization():
    ivs = {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}
    evs = {'hp': 0, 'atk': 252, 'def': 0, 'spa': 0, 'spd': 4, 'spe': 252}
    moves = ['Flamethrower', 'Dragon Claw', 'Air Slash', 'Roost']

    charizard = CompetitivePokemon(
        name="Charizard",
        ability="Blaze",
        item="Charizardite X",
        nature="JOLLY",
        ivs=ivs,
        evs=evs,
        moves=moves
    )

    assert charizard.name == "Charizard"
    assert charizard.pkm.types == ["fire", "flying"]
    assert charizard.ability == "Blaze"
    assert charizard.item == "Charizardite X"
    assert charizard.nature == "JOLLY"
    assert charizard.ivs == ivs
    assert charizard.evs == evs
    assert charizard.moves == moves
    assert charizard.level == 50

    # Check if stats are calculated correctly (values may vary based on nature and formulas)
    assert charizard.raw_stats == {
        'hp': 153,
        'atk': 136,
        'def': 98,
        'spa': 116,
        'spd': 106,
        'spe': 167
    }


