class Field:
    def __init__(self):
        self.weather = None
        self.terrain = None
        self.gravity = False
        self.trick_room = False
        self.side_conditions = [None, None]  # Assuming two sides in the battle
        self.slot_pkm = [[None, None], [None, None]]

    def set_weather(self, weather):
        self.weather = weather

    def set_terrain(self, terrain):
        self.terrain = terrain

    def set_side_condition(self, side_index, condition):
        if side_index in [0, 1]:
            self.side_conditions[side_index] = condition
        else:
            raise ValueError("side_index must be 0 or 1")