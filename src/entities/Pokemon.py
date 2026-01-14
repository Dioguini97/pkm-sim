class Pokemon:
    def __init__(self, name: str, types: list, id: int, base_stats: dict, abilities: list, height: float, weight: float, move_list: list):
        self.name = name
        self.types = types
        self.id = id
        self.base_stats = base_stats
        self.abilities = abilities
        self.height = height
        self.weight = weight
        self.move_list = move_list