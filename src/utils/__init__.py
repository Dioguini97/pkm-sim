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

