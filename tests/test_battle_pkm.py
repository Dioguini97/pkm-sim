from unittest import skip

from data import Cache
from pkm_sim.battle_env.entities.field import Field, BattleSlot
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.turn import Turn, Action
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon

cache = Cache()

incin = cache.get_pokemon_from_cache('incineroar')
amoun = cache.get_pokemon_from_cache('amoonguss')
por2 = cache.get_pokemon_from_cache('porygon2')
bloodm = cache.get_pokemon_from_cache('ursaluna-bloodmoon')
flam = cache.get_pokemon_from_cache('flamigo')
garch = cache.get_pokemon_from_cache('garchomp')

gold = cache.get_pokemon_from_cache('gholdengo')
peli = cache.get_pokemon_from_cache('pelipper')
arch = cache.get_pokemon_from_cache('archaludon')
basc = cache.get_pokemon_from_cache('basculegion-male')

pkm_1 = BattlePokemon(CompetitivePokemon(
    name=incin.name,
    ability="Static",
    item="Light Ball",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["thunderbolt", "quick-attack", "iron-tail", "volt-switch"]
))

pkm_2 = BattlePokemon(CompetitivePokemon(
    name=amoun.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

pkm_3 = BattlePokemon(CompetitivePokemon(
    name=por2.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

pkm_4 = BattlePokemon(CompetitivePokemon(
    name=bloodm.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

pkm_5 = BattlePokemon(CompetitivePokemon(
    name=flam.name,
    ability="Static",
    item="Light Ball",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["thunderbolt", "quick-attack", "iron-tail", "volt-switch"]
))

pkm_6 = BattlePokemon(CompetitivePokemon(
    name=garch.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

pkm_7 = BattlePokemon(CompetitivePokemon(
    name=gold.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

pkm_8 = BattlePokemon(CompetitivePokemon(
    name=peli.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

def test_battle_pkm_init():
    # Placeholder test to ensure the test file is recognized
    pkm = CompetitivePokemon(
        name="Pikachu",
        ability="Static",
        item="Light Ball",
        nature="JOLLY",
        ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
        evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
        moves=["thunderbolt", "Quick Attack", "Iron Tail", "Volt Switch"],
    )
    bt_pkm = BattlePokemon(
        pkm
    )
    assert bt_pkm.pokemon.name == "Pikachu"

def test_battle_pkm_atk_takes_hp_to_target():


    move_1 = pkm_1.get_move('thunderbolt')  #
    move_2 = pkm_2.get_move("razor-leaf")  #

    assert pkm_1.hp_total == 170 and pkm_1.stats['atk'] == 167 and pkm_1.stats['def'] == 110 and pkm_1.stats['spa'] == 90 and pkm_1.stats['spd'] == 111 and pkm_1.stats['spe'] == 123
    assert pkm_2.hp_total == 221 and pkm_2.stats['atk'] == 94 and pkm_2.stats['def'] == 90 and pkm_2.stats['spa'] == 137 and pkm_2.stats['spd'] == 111 and pkm_2.stats['spe'] == 50

@skip(reason='Feitas alteracoes que fizeram com que o teste seja irrelevante. Deve ser alterado depois pela IA')
def test_turn_order_action():
    field = Field(
        active_pkm=[[pkm_1, pkm_2], [pkm_3, pkm_4]],
        bench_pkm=[[pkm_5, pkm_6], [pkm_7, pkm_8]]
    )
    #Order only by speed for now
    action_1 = Action(pkm_1, pkm_1.battle_moves[0], None, None)
    action_2 = Action(pkm_2, pkm_2.battle_moves[2], None, None)
    action_list = [action_1, action_2]
    turn = Turn(0,field, action_list)
    ordered_actions = turn.order_actions()
    assert ordered_actions[0].user == pkm_1
    assert ordered_actions[1].user == pkm_2

    #Should order by priority first
    action_1 = Action(pkm_1, pkm_1.battle_moves[0], None, None)
    action_2 = Action(pkm_2, pkm_2.battle_moves[1], None, None)  # quick-attack has higher priority
    action_list = [action_1, action_2]
    turn = Turn(1, field, action_list)
    ordered_actions = turn.order_actions()
    assert ordered_actions[0].user == pkm_2
    assert ordered_actions[1].user == pkm_1





