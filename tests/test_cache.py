from api.models import Pokemon, Move
from src.data import Cache

CACHE = Cache()

def test_cache_return_false_if_pokemon_not_in_cache():

    assert not CACHE.is_pokemon_in_cache("missing-pokemon")

def test_should_add_pokemon_if_not_in_cache():

    test_pkm = Pokemon(
        name="test-pokemon",
        id=999,
        types=["test-type"],
        base_stats={'hp': 100, 'attack': 100, 'defense': 100, 'special-attack': 100, 'special-defense': 100, 'speed': 100},
        abilities=['test-ability'],
        height=10,
        weight=100,
        move_list=['test-move', 'another-test-move'],
        img_url='http://example.com/test-pokemon.png'
    )

    CACHE.add_pokemon_to_cache(test_pkm)

    assert CACHE.is_pokemon_in_cache("test-pokemon")

def test_should_not_add_pokemon_if_already_in_cache():

    test_pkm = Pokemon(
        name="test-pokemon",
        id=998,
        types=["normal"],
        base_stats={},
        abilities=[],
        height=10,
        weight=0,
        move_list=[],
        img_url=''
    )

    CACHE.add_pokemon_to_cache(test_pkm) # Attempt to add again

    assert CACHE.is_pokemon_in_cache("test-pokemon")
    assert CACHE.get_pokemon_from_cache("test-pokemon").id == 999  # ID should remain as the first added one

def test_cache_return_false_if_move_not_in_cache():

    assert not CACHE.is_move_in_cache("missing-move")

def test_should_add_move_if_not_in_cache():

    test_move = Move(
        name='test-move',
        power= 100,
        accuracy= 100,
        move_type= 'test-type',
        effect_chance= 0,
        damage_class= 'physical',
        pp= 15,
        stat_changes= [],
        entries= 'This is a test move.',
        id=0,
        priority=0,
        target='selected-pokemon',
        ailment='none',
        ailment_chance=0,
        category='damage',
        crit_rate=0,
        drain=0,
        flinch_chance=0,
        healing=0,
        min_hits=None,
        max_hits=None,
        min_turns=None,
        max_turns=None,
        stat_chance=0
    )

    CACHE.add_move_to_cache(test_move)

    assert CACHE.is_move_in_cache("test-move")

def test_should_get_pkm_species_from_cache_with_4_attributes():
    test_pkm = CACHE.get_pokemon_species_from_cache("applin")
    assert test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("flapple")
    assert not test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("appletun")
    assert not test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("dipplin")
    assert test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("hydrapple")
    assert not test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("pikachu")
    assert test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("electabuzz")
    assert test_pkm.does_it_evolve

    test_pkm = CACHE.get_pokemon_species_from_cache("parasect")
    assert not test_pkm.does_it_evolve

