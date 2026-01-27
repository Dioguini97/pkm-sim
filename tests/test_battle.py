from data import Cache
from api.models import CompetitivePokemon
from pkm_sim.battle_env.battle import Battle
from pkm_sim.battle_env.entities.pokemon import BattlePokemon

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
    types=incin.types,
    base_stats=incin.base_stats,
    abilities=incin.abilities,
    id=incin.id,
    height=incin.height,
    weight=incin.weight,
    move_list=incin.move_list,
    img_url=incin.img_url,
    ability="intimidate",
    item="safety-goggles",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["flare-blitz", "fake-out", "knock-off", "parting-shot"],
    evolution_chain_id=incin.evolution_chain_id,
    varieties=incin.varieties
))

pkm_2 = BattlePokemon(CompetitivePokemon(
    name=amoun.name,
    types=amoun.types,
    base_stats=amoun.base_stats,
    abilities=amoun.abilities,
    id=amoun.id,
    height=amoun.height,
    weight=amoun.weight,
    move_list=amoun.move_list,
    img_url=amoun.img_url,
    ability="Regenerator",
    item="sitrus-berry",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spatk": 252, "spdef": 4, "spd": 0},
    moves=["spore", "rage-powder", "protect", "sludge-bomb"],
    evolution_chain_id=amoun.evolution_chain_id,
    varieties=amoun.varieties
))

pkm_3 = BattlePokemon(CompetitivePokemon(
    name=por2.name,
    types=por2.types,
    base_stats=por2.base_stats,
    abilities=por2.abilities,
    id=por2.id,
    height=por2.height,
    weight=por2.weight,
    move_list=por2.move_list,
    img_url=por2.img_url,
    ability="download",
    item="eviolite",
    nature="BOLD",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 252, "spatk": 0, "spdef": 4, "spd": 0},
    moves=["tri-attack", "recover", "ice-beam", "trick-room"],
    evolution_chain_id=por2.evolution_chain_id,
    varieties=por2.varieties
))

pkm_4 = BattlePokemon(CompetitivePokemon(
    name=bloodm.name,
    types=bloodm.types,
    base_stats=bloodm.base_stats,
    abilities=bloodm.abilities,
    id=bloodm.id,
    height=bloodm.height,
    weight=bloodm.weight,
    move_list=bloodm.move_list,
    img_url=bloodm.img_url,
    ability="quark-drive",
    item="life-orb",
    nature="ADAMANT",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 252, "spatk": 0, "spdef": 4, "spd": 0},
    moves=["blood-moon", "hyper-voice", "protect", "earth-power"],
    evolution_chain_id=bloodm.evolution_chain_id,
    varieties=bloodm.varieties
))

pkm_5 = BattlePokemon(CompetitivePokemon(
    name=flam.name,
    types=flam.types,
    base_stats=flam.base_stats,
    abilities=flam.abilities,
    id=flam.id,
    height=flam.height,
    weight=flam.weight,
    move_list=flam.move_list,
    img_url=flam.img_url,
    ability="scrappy",
    item="focus-sash",
    nature="TIMID",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["close-combat", "protect", "tailwind", "brave-bird"],
    evolution_chain_id=flam.evolution_chain_id,
    varieties=flam.varieties
))

pkm_6 = BattlePokemon(CompetitivePokemon(
    name=garch.name,
    types=garch.types,
    base_stats=garch.base_stats,
    abilities=garch.abilities,
    id=garch.id,
    height=garch.height,
    weight=garch.weight,
    move_list=garch.move_list,
    img_url=garch.img_url,
    ability="rough-skin",
    item="rocky-helmet",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["earthquake", "protect", "dragon-claw", "liquidation"],
    evolution_chain_id=garch.evolution_chain_id,
    varieties=garch.varieties
))

pkm_7 = BattlePokemon(CompetitivePokemon(
    name=gold.name,
    types=gold.types,
    base_stats=gold.base_stats,
    abilities=gold.abilities,
    id=gold.id,
    height=gold.height,
    weight=gold.weight,
    move_list=gold.move_list,
    img_url=gold.img_url,
    ability="good-as-gold",
    item="air-balloon",
    nature="MODEST",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 0, "def": 0, "spatk": 252, "spdef": 4, "spd": 252},
    moves=["shadow-ball", "make-it-rain", "nasty-plot", "protect"],
    evolution_chain_id=gold.evolution_chain_id,
    varieties=gold.varieties
))

pkm_8 = BattlePokemon(CompetitivePokemon(
    name=peli.name,
    types=peli.types,
    base_stats=peli.base_stats,
    abilities=peli.abilities,
    id=peli.id,
    height=peli.height,
    weight=peli.weight,
    move_list=peli.move_list,
    img_url=peli.img_url,
    ability="drizzle",
    item="damp-rock",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spatk": 4, "spdef": 252, "spd": 0},
    moves=["weather-ball", "hurricane", "tailwind", "wide-guard"],
    evolution_chain_id=peli.evolution_chain_id,
    varieties=peli.varieties
))

pkm_9 = BattlePokemon(CompetitivePokemon(
    name=arch.name,
    types=arch.types,
    base_stats=arch.base_stats,
    abilities=arch.abilities,
    id=arch.id,
    height=arch.height,
    weight=arch.weight,
    move_list=arch.move_list,
    img_url=arch.img_url,
    ability="stamina",
    item="assault-vest",
    nature="IMPISH",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 4, "def": 252, "spatk": 0, "spdef": 0, "spd": 0},
    moves=["electro-shot", "body-press", "dragon-pulse", "flash-cannon"],
    evolution_chain_id=arch.evolution_chain_id,
    varieties=arch.varieties
))

pkm_10 = BattlePokemon(CompetitivePokemon(
    name=basc.name,
    types=basc.types,
    base_stats=basc.base_stats,
    abilities=basc.abilities,
    id=basc.id,
    height=basc.height,
    weight=basc.weight,
    move_list=basc.move_list,
    img_url=basc.img_url,
    ability="adaptability",
    item="life-orb",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["wave-crash", "last-respects", "protect", "ice-fang"],
    evolution_chain_id=basc.evolution_chain_id,
    varieties=basc.varieties
))

pkm_11 = BattlePokemon(CompetitivePokemon(
    name=incin.name,
    types=incin.types,
    base_stats=incin.base_stats,
    abilities=incin.abilities,
    id=incin.id,
    height=incin.height,
    weight=incin.weight,
    move_list=incin.move_list,
    img_url=incin.img_url,
    ability="intimidate",
    item="safety-goggles",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spatk": 0, "spdef": 4, "spd": 252},
    moves=["flare-blitz", "fake-out", "knock-off", "parting-shot"],
    evolution_chain_id=incin.evolution_chain_id,
    varieties=incin.varieties
))

pkm_12 = BattlePokemon(CompetitivePokemon(
    name=amoun.name,
    types=amoun.types,
    base_stats=amoun.base_stats,
    abilities=amoun.abilities,
    id=amoun.id,
    height=amoun.height,
    weight=amoun.weight,
    move_list=amoun.move_list,
    img_url=amoun.img_url,
    ability="Regenerator",
    item="sitrus-berry",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spatk": 31, "spdef": 31, "spd": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spatk": 252, "spdef": 4, "spd": 0},
    moves=["spore", "rage-powder", "protect", "sludge-bomb"],
    evolution_chain_id=amoun.evolution_chain_id,
    varieties=amoun.varieties
))

def test_battle_initialization():
    battle = Battle([[pkm_1, pkm_2, pkm_3, pkm_4, pkm_5, pkm_6],[pkm_7, pkm_8, pkm_9, pkm_10, pkm_11, pkm_12]])
    assert len(battle.teams) == 2
    assert len(battle.teams[0]) == 4
    assert len(battle.teams[1]) == 4
    assert battle.field.slot_pkm[0][0] == pkm_1
    assert battle.field.slot_pkm[0][1] == pkm_2
    assert battle.field.slot_pkm[1][1] == pkm_8
    assert battle.field.slot_pkm[1][0] == pkm_7


