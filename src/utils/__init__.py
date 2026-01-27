natures = {
    "HARDY": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1, "spd": 1},
    "LONELY": {"atk": 1.1, "def": 0.9, "spatk": 1, "spdef": 1, "spd": 1},
    "BRAVE": {"atk": 1.1, "def": 1, "spatk": 1, "spdef": 1, "spd": 0.9},
    "ADAMANT": {"atk": 1.1, "def": 1, "spatk": 0.9, "spdef": 1, "spd": 1},
    "NAUGHTY": {"atk": 1.1, "def": 1, "spatk": 1, "spdef": 0.9, "spd": 1},
    "BOLD": {"atk": 0.9, "def": 1.1, "spatk": 1, "spdef": 1, "spd": 1},
    "DOCILE": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1, "spd": 1},
    "RELAXED": {"atk": 1, "def": 1.1, "spatk": 1, "spdef": 1, "spd": 0.9},
    "IMPISH": {"atk": 1, "def": 1.1, "spatk": 0.9, "spdef": 1, "spd": 1},
    "LAX": {"atk": 1, "def": 1.1, "spatk": 1, "spdef": 0.9, "spd": 1},
    "TIMID": {"atk": 0.9, "def": 1, "spatk": 1, "spdef": 1, "spd": 1.1},
    "HASTY": {"atk": 1, "def": 0.9, "spatk": 1, "spdef": 1, "spd": 1.1},
    "SERIOUS": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1, "spd": 1},
    "JOLLY": {"atk": 1, "def": 1, "spatk": 0.9, "spdef": 1, "spd": 1.1},
    "NAIVE": {"atk": 1, "def": 1, "spatk": 1, "spdef": 0.9, "spd": 1.1},
    "MODEST": {"atk": 0.9, "def": 1, "spatk": 1.1, "spdef": 1, "spd": 1},
    "MILD": {"atk": 1, "def": 0.9, "spatk": 1.1, "spdef": 1, "spd": 1},
    "QUIET": {"atk": 1, "def": 1, "spatk": 1.1, "spdef": 1, "spd": 0.9},
    "BASHFUL": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1, "spd": 1},
    "RASH": {"atk": 1, "def": 1, "spatk": 1.1, "spdef": 0.9, "spd": 1},
    "CALM": {"atk": 0.9, "def": 1, "spatk": 1, "spdef": 1.1, "spd": 1},
    "GENTLE": {"atk": 1, "def": 0.9, "spatk": 1, "spdef": 1.1, "spd": 1},
    "SASSY": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1.1, "spd": 0.9},
    "CAREFUL": {"atk": 1, "def": 1, "spatk": 0.9, "spdef": 1.1, "spd": 1},
    "QUIRKY": {"atk": 1, "def": 1, "spatk": 1, "spdef": 1, "spd": 1}
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
            return "spatk"
        case "special-defense":
            return "spdef"
        case "speed":
            return "spd"

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

MOVE_TARGET_ENUM = [
    'specific-move', # p.e. Curse, Counter
    'selected-pokemon-me-first', # p.e. me-first, max moves
    'ally', # p.e. Helping Hand
    'users-field', # p.e. Reflect, Light Screen, Tailwind
    'user-or-ally', # p.e. acupressure (only)
    'opponents-field', # p.e. Stealth Rock, Spikes
    'user', # p.e. Swords Dance, Recover
    'random-opponent', # p.e. Thrash, Outrage, Struggle
    'all-other-pokemon', # p.e. Earthquake, Surf
    'selected-pokemon', # p.e. Shadow Ball, Flamethrower
    'all-opponents', # p.e. Blizzard, Rock Slide
    'entire-field', # p.e. Hail, Rain Dance, Trick Room, Grassy Terrain
    'user-and-allies', # p.e. life-dew, howl
    'all-pokemon',  # p.e. Perish Song
    'all-allies', # p.e. Dragon Cheer
    'fainting-pokemon' # p.e. Revival Blessing
]

MOVE_AILMENT_ENUM = [
    'none',
    'paralysis',
    'sleep',
    'freeze',
    'burn',
    'poison',
    'badly-poison',
    'confusion',
    'infatuation',
    'trap',
    'nightmare'
]


