from data import Cache
from api.models import PokemonSpecies
from pkm_sim.battle_env.battle import Battle
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.pokemon_party import PokemonParty
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
    ability="intimidate",
    item="safety-goggles",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["flare-blitz", "fake-out", "knock-off", "parting-shot"]
))

pkm_2 = BattlePokemon(CompetitivePokemon(
    name=amoun.name,
    ability="Regenerator",
    item="sitrus-berry",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["spore", "rage-powder", "protect", "sludge-bomb"]
))

pkm_3 = BattlePokemon(CompetitivePokemon(
    name=por2.name,
    ability="download",
    item="eviolite",
    nature="BOLD",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 252, "spa": 0, "spd": 4, "spe": 0},
    moves=["tri-attack", "recover", "ice-beam", "trick-room"]
))

pkm_4 = BattlePokemon(CompetitivePokemon(
    name=bloodm.name,
    ability="quark-drive",
    item="life-orb",
    nature="ADAMANT",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 252, "spa": 0, "spd": 4, "spe": 0},
    moves=["blood-moon", "hyper-voice", "protect", "earth-power"]
))

pkm_5 = BattlePokemon(CompetitivePokemon(
    name=flam.name,
    ability="scrappy",
    item="focus-sash",
    nature="TIMID",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["close-combat", "protect", "tailwind", "brave-bird"]
))

pkm_6 = BattlePokemon(CompetitivePokemon(
    name=garch.name,
    ability="rough-skin",
    item="rocky-helmet",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["earthquake", "protect", "dragon-claw", "liquidation"]
))

pkm_7 = BattlePokemon(CompetitivePokemon(
    name=gold.name,
    ability="good-as-gold",
    item="air-balloon",
    nature="MODEST",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 252},
    moves=["shadow-ball", "make-it-rain", "nasty-plot", "protect"]
))

pkm_8 = BattlePokemon(CompetitivePokemon(
    name=peli.name,
    ability="drizzle",
    item="damp-rock",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 4, "spd": 252, "spe": 0},
    moves=["weather-ball", "hurricane", "tailwind", "wide-guard"],
))

pkm_9 = BattlePokemon(CompetitivePokemon(
    name=arch.name,
    ability="stamina",
    item="assault-vest",
    nature="IMPISH",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 4, "def": 252, "spa": 0, "spd": 0, "spe": 0},
    moves=["electro-shot", "body-press", "dragon-pulse", "flash-cannon"],
))

pkm_10 = BattlePokemon(CompetitivePokemon(
    name=basc.name,
    ability="adaptability",
    item="life-orb",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["wave-crash", "last-respects", "protect", "ice-fang"]
))

pkm_11 = BattlePokemon(CompetitivePokemon(
    name=incin.name,
    ability="intimidate",
    item="safety-goggles",
    nature="JOLLY",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 0, "atk": 252, "def": 0, "spa": 0, "spd": 4, "spe": 252},
    moves=["flare-blitz", "fake-out", "knock-off", "parting-shot"]
))

pkm_12 = BattlePokemon(CompetitivePokemon(
    name=amoun.name,
    ability="Regenerator",
    item="sitrus-berry",
    nature="CALM",
    ivs={"hp": 31, "atk": 31, "def": 31, "spa": 31, "spd": 31, "spe": 31},
    evs={"hp": 252, "atk": 0, "def": 0, "spa": 252, "spd": 4, "spe": 0},
    moves=["spore", "rage-powder", "protect", "sludge-bomb"]
))
party_1 = PokemonParty([pkm_1, pkm_2, pkm_3, pkm_4, pkm_5, pkm_6])
party_2 = PokemonParty([pkm_7, pkm_8, pkm_9, pkm_10, pkm_11, pkm_12])
def test_battle_initialization():
    battle = Battle([party_1, party_2])
    assert len(battle.teams) == 2
    assert len(battle.teams[0]) == 4
    assert len(battle.teams[1]) == 4
    assert battle.field.slots[0][0].pokemon == pkm_1
    assert battle.field.slots[0][1].pokemon == pkm_2
    assert battle.field.slots[1][1].pokemon == pkm_8
    assert battle.field.slots[1][0].pokemon == pkm_7
    #battle.execute()


