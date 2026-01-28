from data import Cache
from pkm_sim.battle_env.entities.field import Field
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.turn import Turn, Action
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon

cache = Cache()

pika = cache.get_pokemon_from_cache('pikachu')
bulba = cache.get_pokemon_from_cache('bulbasaur')

pkm_1 = BattlePokemon(CompetitivePokemon(
    name=pika.name,
    ability="Static",
    item="Light Ball",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["thunderbolt", "quick-attack", "iron-tail", "volt-switch"]
))

pkm_2 = BattlePokemon(CompetitivePokemon(
    name=bulba.name,
    ability="Overgrow",
    item="Miracle Seed",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spatk": 252, "spdef": 4, "spd": 0},
    moves=["vine-whip", "quick-attack", "razor-leaf", "sleep-powder"]
))

def test_battle_pkm_init():
    # Placeholder test to ensure the test file is recognized
    pkm = CompetitivePokemon(
        name="Pikachu",
        ability="Static",
        item="Light Ball",
        nature="JOLLY",
        ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
        evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
        moves=["thunderbolt", "Quick Attack", "Iron Tail", "Volt Switch"],
    )
    bt_pkm = BattlePokemon(
        pkm
    )
    assert bt_pkm.pokemon.name == "Pikachu"

def test_battle_pkm_atk_takes_hp_to_target():


    move_1 = pkm_1.get_move('thunderbolt')  #
    move_2 = pkm_2.get_move("razor-leaf")  #

    assert pkm_1.hp_total == 110 and pkm_1.stats['atk'] == 107 and pkm_1.stats['def'] == 60 and pkm_1.stats['spatk'] == 63 and pkm_1.stats['spdef'] == 71 and pkm_1.stats['spd'] == 156
    assert pkm_2.hp_total == 152 and pkm_2.stats['atk'] == 62 and pkm_2.stats['def'] == 69 and pkm_2.stats['spatk'] == 117 and pkm_2.stats['spdef'] == 94 and pkm_2.stats['spd'] == 65

    pkm_1.attack(pkm_2, move_1)
    assert pkm_2.hp_total - 21 < pkm_2.current_hp < pkm_2.hp_total - 17

def test_turn_order_action():
    #Order only by speed for now
    action_1 = Action(pkm_1, pkm_1.battle_moves[0], None, None)
    action_2 = Action(pkm_2, pkm_2.battle_moves[2], None, None)
    action_list = [action_1, action_2]
    turn = Turn(0, Field(), action_list)
    ordered_actions = turn.order_actions()
    assert ordered_actions[0].user == pkm_1
    assert ordered_actions[1].user == pkm_2

    #Should order by priority first
    action_1 = Action(pkm_1, pkm_1.battle_moves[0], None, None)
    action_2 = Action(pkm_2, pkm_2.battle_moves[1], None, None)  # quick-attack has higher priority
    action_list = [action_1, action_2]
    turn = Turn(1, Field(), action_list)
    ordered_actions = turn.order_actions()
    assert ordered_actions[0].user == pkm_2
    assert ordered_actions[1].user == pkm_1


def test_battle_pkm_from_name():
    test = BattlePokemon.from_name('pikachu')
    assert test is not None





