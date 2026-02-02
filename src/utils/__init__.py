import uuid
from enum import Enum

natures = {
    "HARDY": {"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1},
    "LONELY": {"atk": 1.1, "def": 0.9, "spa": 1, "spd": 1, "spe": 1},
    "BRAVE": {"atk": 1.1, "def": 1, "spa": 1, "spd": 1, "spe": 0.9},
    "ADAMANT": {"atk": 1.1, "def": 1, "spa": 0.9, "spd": 1, "spe": 1},
    "NAUGHTY": {"atk": 1.1, "def": 1, "spa": 1, "spd": 0.9, "spe": 1},
    "BOLD": {"atk": 0.9, "def": 1.1, "spa": 1, "spd": 1, "spe": 1},
    "DOCILE": {"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1},
    "RELAXED": {"atk": 1, "def": 1.1, "spa": 1, "spd": 1, "spe": 0.9},
    "IMPISH": {"atk": 1, "def": 1.1, "spa": 0.9, "spd": 1, "spe": 1},
    "LAX": {"atk": 1, "def": 1.1, "spa": 1, "spd": 0.9, "spe": 1},
    "TIMID": {"atk": 0.9, "def": 1, "spa": 1, "spd": 1, "spe": 1.1},
    "HASTY": {"atk": 1, "def": 0.9, "spa": 1, "spd": 1, "spe": 1.1},
    "SERIOUS": {"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1},
    "JOLLY": {"atk": 1, "def": 1, "spa": 0.9, "spd": 1, "spe": 1.1},
    "NAIVE": {"atk": 1, "def": 1, "spa": 1, "spd": 0.9, "spe": 1.1},
    "MODEST": {"atk": 0.9, "def": 1, "spa": 1.1, "spd": 1, "spe": 1},
    "MILD": {"atk": 1, "def": 0.9, "spa": 1.1, "spd": 1, "spe": 1},
    "QUIET": {"atk": 1, "def": 1, "spa": 1.1, "spd": 1, "spe": 0.9},
    "BASHFUL": {"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1},
    "RASH": {"atk": 1, "def": 1, "spa": 1.1, "spd": 0.9, "spe": 1},
    "CALM": {"atk": 0.9, "def": 1, "spa": 1, "spd": 1.1, "spe": 1},
    "GENTLE": {"atk": 1, "def": 0.9, "spa": 1, "spd": 1.1, "spe": 1},
    "SASSY": {"atk": 1, "def": 1, "spa": 1, "spd": 1.1, "spe": 0.9},
    "CAREFUL": {"atk": 1, "def": 1, "spa": 0.9, "spd": 1.1, "spe": 1},
    "QUIRKY": {"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1}
}

type_matrix = {
    'normal':    {'rock': 0.5, 'ghost': 0,   'steel': 0.5},
    'fire':      {'fire': 0.5, 'water': 0.5, 'grass': 2,   'ice': 2,   'bug': 2,   'rock': 0.5, 'dragon': 0.5, 'steel': 2},
    'water':     {'fire': 2,   'water': 0.5, 'grass': 0.5, 'ground': 2, 'rock': 2,   'dragon': 0.5},
    'electric':  {'water': 2,   'electric': 0.5, 'grass': 0.5, 'ground': 0,   'flying': 2,   'dragon': 0.5},
    'grass':     {'fire': 0.5, 'water': 2,   'grass': 0.5, 'poison': 0.5, 'ground': 2,   'flying': 0.5, 'bug': 0.5, 'rock': 2,   'dragon': 0.5, 'steel': 0.5},
    'ice':       {'fire': 0.5, 'water': 0.5, 'grass': 2,   'ice': 0.5, 'ground': 2,   'flying': 2,   'dragon': 2,   'steel': 0.5},
    'fighting':  {'normal': 2,   'ice': 2,   'rock': 2,   'dark': 2,   'steel': 2,   'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5,   'ghost': 0},
    'poison':    {'grass': 2,   'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0,   'fairy': 2},
    'ground':    {'fire': 2,   'electric': 2, 'grass': 0.5, 'poison': 2,   'flying': 0,   'bug': 0.5, 'rock': 2,   'steel': 2},
    'flying':    {'electric': 0.5, 'grass': 2,   'fighting': 2,   'bug': 2,   'rock': 0.5, 'steel': 0.5},
    'psychic':   {'fighting': 2,   'poison': 2,   'psychic': 0.5, 'dark': 0,   'steel': 0.5},
    'bug':       {'fire': 0.5, 'grass': 2,   'fighting': 0.5, 'poison': 0.5, 'ground': 0.5, 'flying': 0.5, 'psychic': 2,   'dark': 2,   'steel': 0.5, 'fairy': 0.5},
    'rock':      {'fire': 2,   'ice': 2,   'fighting': 0.5, 'ground': 0.5, 'flying': 2,   'bug': 2,   'steel': 0.5},
    'ghost':     {'normal': 0,   'psychic': 2, 'ghost': 2,   'dark': 0.5},
    'dragon':    {'dragon': 2,   'steel': 0.5, 'fairy': 0},
    'dark':      {'fighting': 0.5, 'psychic': 2,   'ghost': 2,   'dark': 0.5, 'fairy': 0.5},
    'steel':     {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2,   'rock': 2,   'steel': 0.5, 'fairy': 2},
    'fairy':     {'fire': 0.5, 'fighting': 2,   'poison': 0.5, 'dragon': 2, 'dark': 2,   'steel': 0.5}
}

def transform_stat_name(stat: str):
    match stat:
        case "hp":
            return "hp"
        case "attack":
            return "atk"
        case "defense":
            return "def"
        case "special-attack":
            return "spa"
        case "special-defense":
            return "spd"
        case "speed":
            return "spe"

def get_type_effectiveness(move_type: str, target_type: str) -> float:
    try:
        return type_matrix[move_type][target_type]
    except KeyError:
        return 1.0

def from_name_to_api_read(name: str) -> str:
    return name.lower().replace(" ", "-").replace(".", "").replace("'", "").replace("é", "e")

stage_multipliers = {
    -6: 2/8,
    -5: 2/7,
    -4: 2/6,
    -3: 2/5,
    -2: 2/4,
    -1: 2/3,
     0: 2/2,
     1: 3/2,
     2: 4/2,
     3: 5/2,
     4: 6/2,
     5: 7/2,
     6: 8/2
}

stage_multipliers_acc_eva = {
    -6: 3/9,
    -5: 3/8,
    -4: 3/7,
    -3: 3/6,
    -2: 3/5,
    -1: 3/4,
    0: 3/3,
    1: 4/3,
    2: 5/3,
    3: 6/3,
    4: 7/3,
    5: 8/3,
    6: 9/3
}

MOVE_CATEGORY = [
    'damage',
    'ailment', # Spore, Perish Song, Toxic
    'net-good-stats', # Swords Dance, Calm Mind
    'heal', # Recover, Soft-Boiled
    'damage+ailment', # Flamethrower, Poison String, porque dá damage e pode causar status
    'swagger', # Swagger, Flatter, raise target stats + inflict status
    'damage+lower', # moves that deal damage and lower target's stats, e.g., Psychic, Mud-slap
    'damage+raise', # moves that deal damage and raise user's stats, e.g., Close Combat, Flame Charge
    'damage+heal' # Giga Drain, Drain Punch
    'ohko', # Fissure, Guillotine, Horn Drill
    'whole-field-effect', # moves that affect the entire field, e.g., Rain Dance, Haze, trick room, grassy terrain, gravity
    'field-effect', # moves that affect one side of the field, e.g., Stealth Rock, Light Screen, Reflect, wide guard
    'force-switch', # Roar, Whirlwind
    'unique' # e.g., Transform, Mimic, Sketch, Metronome, follow me
]

class MoveTarget(Enum):
    SPECIFIC_MOVE = 'specific-move' # p.e. Curse, Counter
    SELECTED_POKEMON_ME_FIRST = 'selected-pokemon-me-first' # p.e. me-first, max moves
    ALLY = 'ally' # p.e. Helping Hand
    USERS_FIELD = 'users-field',# p.e. Reflect, Light Screen, Tailwind
    USER_OR_ALLY = 'user-or-ally' # p.e. acupressure (only)
    OPPONENTS_FIELD = 'opponents-field' # p.e. Stealth Rock, Spikes
    USER='user' # p.e. Swords Dance, Recover
    RANDOM_OPPONENT='random-opponent' # p.e. Thrash, Outrage, Struggle
    ALL_OTHER_POKEMON='all-other-pokemon' # p.e. Earthquake, Surf
    SELECTED_POKEMON='selected-pokemon' # p.e. Shadow Ball, Flamethrower
    ALL_OPPONENTS='all-opponents' # p.e. Blizzard, Rock Slide
    ENTIRE_FIELD='entire-field' # p.e. Hail, Rain Dance, Trick Room, Grassy Terrain
    USER_AND_ALLIES='user-and-allies' # p.e. life-dew, howl
    ALL_POKEMON='all-pokemon' # p.e. Perish Song
    ALL_ALLIES='all-allies' # p.e. Dragon Cheer
    FAINTING_POKEMON= 'fainting-pokemon' # p.e. Revival Blessing

class MoveAilment(Enum):
    UNKNOWN = 'unknown'
    NONE = 'none'
    PAR = 'paralysis'
    SLP = 'sleep'
    FRZ = 'freeze'
    BRN = 'burn'
    PSN = 'poison'
    BPSN = 'badly-poison'
    CONFUSION = 'confusion'
    INFATUATION = 'infatuation'
    TRAP = 'trap'
    NIGHTMARE = 'nightmare'
    TORMENT = 'torment'
    DISABLE = 'disable'
    YAWN = 'yawn'
    HEAL_BLOCK = 'heal-block'
    NO_TYPE_IMMUNITY = 'no-type-immunity'
    LEECH_SEED = 'leech-seed'
    EMBARGO = 'embargo'
    PERISH_SONG = 'perish-song'
    INGRAIN = 'ingrain'
    SILENCE = 'silence'
    TAR_SHOT = 'tar-shot'

class ActionType(Enum):
    ATTACK = 'attack'
    SWITCH = 'switch'
    RUN = 'run'
    
class Transformation(Enum):
    MEGA = 'mega'
    DYNAMAX = 'dynamax'
    TERA = 'tera'

class DamageClass(Enum):
    PHYSICAL = 'physical'
    SPECIAL = 'special'
    STATUS = 'status'

class PokemonType(Enum):
    WATER = 'water'
    FIRE = 'fire'
    GRASS = 'grass'
    ELECTRIC = 'electric'
    FIGHTING = 'fighting'
    ROCK = 'rock'
    GROUND = 'ground'
    ICE = 'ice'
    STEEL = 'steel'
    DARK = 'dark'
    FAIRY = 'fairy'
    PSYCHIC = 'psychic'
    BUG = 'bug'
    FLYING = 'flying'
    POISON = 'poison'
    NORMAL = 'normal'
    GHOST = 'ghost'
    DRAGON = 'dragon'
    STELLAR = 'stellar'

class ItemCategory(Enum):
    STAT_BOOSTS = "stat-boosts"
    EFFORT_DROP = "effort-drop"
    MEDICINE = "medicine"
    OTHER = "other"
    IN_A_PINCH = "in-a-pinch"
    PICKY_HEALING = "picky-healing"
    TYPE_PROTECTION = "type-protection"
    BAKING_ONLY = "baking-only"
    COLLECTIBLES = "collectibles"
    EVOLUTION = "evolution"
    SPELUNKING = "spelunking"
    HELD_ITEMS = "held-items"
    CHOICE = "choice"
    EFFORT_TRAINING = "effort-training"
    BAD_HELD_ITEMS = "bad-held-items"
    TRAINING = "training"
    PLATES = "plates"
    SPECIES_SPECIFIC = "species-specific"
    TYPE_ENHANCEMENT = "type-enhancement"
    EVENT_ITEMS = "event-items"
    GAMEPLAY = "gameplay"
    PLOT_ADVANCEMENT = "plot-advancement"
    UNUSED = "unused"
    LOOT = "loot"
    ALL_MAIL = "all-mail"
    VITAMINS = "vitamins"
    HEALING = "healing"
    PP_RECOVERY = "pp-recovery"
    REVIVAL = "revival"
    STATUS_CURES = "status-cures"
    MULCH = "mulch"
    SPECIAL_BALLS = "special-balls"
    STANDARD_BALLS = "standard-balls"
    DEX_COMPLETION = "dex-completion"
    SCARVES = "scarves"
    ALL_MACHINES = "all-machines"
    FLUTES = "flutes"
    APRICORN_BALLS = "apricorn-balls"
    APRICORN_BOX = "apricorn-box"
    DATA_CARDS = "data-cards"
    JEWELS = "jewels"
    MIRACLE_SHOOTER = "miracle-shooter"
    MEGA_STONES = "mega-stones"
    MEMORIES = "memories"
    Z_CRYSTALS = "z-crystals"
    SPECIES_CANDIES = "species-candies"
    CATCHING_BONUS = "catching-bonus"
    DYNAMAX_CRYSTALS = "dynamax-crystals"
    NATURE_MINTS = "nature-mints"
    CURRY_INGREDIENTS = "curry-ingredients"
    TERA_SHARD = "tera-shard"
    SANDWICH_INGREDIENTS = "sandwich-ingredients"
    TM_MATERIALS = "tm-materials"
    PICNIC = "picnic"

class ItemAttribute(Enum):
    COUNTABLE = 'countable'
    CONSUMABLE = 'consumable'
    USABLE_OVERWORLD = 'usable-overworld'
    USABLE_IN_BATTLE = 'usable-in-battle'
    HOLDABLE_ACTIVE = 'holdable-active'
    HOLDABLE_PASSIVE = 'holdable-passive'
    UNDERGROUND = 'underground'

def generate_uuid():
    return uuid.uuid4()
