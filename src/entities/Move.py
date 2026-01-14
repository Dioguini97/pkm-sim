class Move:
    def __init__(self, id: int, name: str, api_name: str, power: int, accuracy: int, move_type: str, effect_chance: int, damage_class: str, pp: int, priority: int, stat_changes: list, target: str, entries: str):
        self.name = name
        self.api_name = api_name
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

    def __repr__(self):
        return f"name={self.name}, power={self.power}, accuracy={self.accuracy}, pp={self.pp}\n{self.effect_entries}"