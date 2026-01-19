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
    'confusion',
    'infatuation',
    'trap',
    'nightmare'
]

class Move:
    def __init__(self, id: int, name: str, power: int, accuracy: int, move_type: str, effect_chance: int, damage_class: str, pp: int, priority: int,
                 stat_changes: list, target: str, entries: str, ailment: str, ailment_chance: int, category: str, crit_rate: int,
                 drain: int, flinch_chance: int, healing: int, min_hits: int|None, max_hits: int|None, min_turns: int|None, max_turns: int|None, stat_chance: int):
        self.name = name
        self.power = power
        self.move_type = move_type
        self.accuracy = accuracy
        self.effect_chance = effect_chance # e.g., 20% chance of lower spdef
        self.damage_class = damage_class  # e.g., Physical, Special, Status
        self.pp = pp
        self.priority = priority
        self.stat_changes = stat_changes  # e.g., ('spdef', -1)
        self.target = target  # e.g., 'selected-pokemon', 'all-opponents'
        self.entries = entries  # e.g., "May lower the target's Special Defense by 1 stage."
        self.id = id
        self.ailment = ailment
        self.ailment_chance = ailment_chance
        self.category = category
        self.crit_rate = crit_rate
        self.drain = drain
        self.flinch_chance = flinch_chance
        self.healing = healing
        self.min_hits = min_hits
        self.max_hits = max_hits
        self.min_turns = min_turns
        self.max_turns = max_turns
        self.stat_chance = stat_chance

    def __repr__(self):
        return f"name={self.name}, power={self.power}, accuracy={self.accuracy}, pp={self.pp}\n{self.effect_entries}"

def map_json_to_move(json_data):
    return Move(
        id=json_data['id'],
        name=json_data['name'],
        power=json_data['power'],
        accuracy=json_data['accuracy'],
        move_type=json_data['move_type'],
        effect_chance=json_data.get('effect_chance'),
        damage_class=json_data['damage_class'],
        pp=json_data['pp'],
        priority=json_data['priority'],
        stat_changes=json_data['stat_changes'],
        target=json_data['target'],
        entries=json_data['entries'],
        ailment=json_data['ailment'],
        ailment_chance=json_data['ailment_chance'],
        category=json_data['category'],
        crit_rate=json_data['crit_rate'],
        drain=json_data['drain'],
        flinch_chance=json_data['flinch_chance'],
        healing=json_data['healing'],
        min_hits=json_data['min_hits'],
        max_hits=json_data['max_hits'],
        min_turns=json_data['min_turns'],
        max_turns=json_data['max_turns'],
        stat_chance=json_data['stat_chance']
    )