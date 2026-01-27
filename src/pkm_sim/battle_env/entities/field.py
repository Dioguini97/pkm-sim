class Field:
    def __init__(self, weather=None, terrain=None, gravity=False, trick_room=False, side_conditions=None, slot_pkm=None, bench_pkm=None):
        if slot_pkm is None:
            slot_pkm = [[None, None], [None, None]]
        if bench_pkm is None:
            bench_pkm = [[None, None], [None, None]]
        if side_conditions is None:
            side_conditions = [None, None]
        self.weather = weather
        self.terrain = terrain
        self.gravity = gravity
        self.trick_room = trick_room
        self.side_conditions = side_conditions  # Assuming two sides in the battle
        self.slot_pkm = slot_pkm
        self.bench_pkm = bench_pkm

    def set_weather(self, weather):
        self.weather = weather

    def set_terrain(self, terrain):
        self.terrain = terrain

    def set_side_condition(self, side_index, condition):
        if side_index in [0, 1]:
            self.side_conditions[side_index] = condition
        else:
            raise ValueError("side_index must be 0 or 1")