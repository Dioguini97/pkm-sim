from pkm_sim.battle_env.entities.pokemon import BattlePokemon


class BattleSlot:
    def __init__(self, side: int, index: int):
        self.side = side
        self.index = index
        self.pokemon: BattlePokemon | None = None
        self.is_protected_by = None

    def is_empty(self):
        return self.pokemon is None


class Field:
    def __init__(self, weather=None, terrain=None, gravity=False, trick_room=False, side_conditions=None, bench_pkm: list[list]=None):
        self.slots = [
            [BattleSlot(0,0), BattleSlot(0,1)],
            [BattleSlot(1, 0), BattleSlot(1, 1)]
        ]
        if side_conditions is None:
            side_conditions = [[], []]
        self.weather = weather
        self.terrain = terrain
        self.gravity = gravity
        self.trick_room = trick_room
        self.side_conditions = side_conditions  # Assuming two sides in the battle
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

    def switch(self, _out: BattleSlot, _in: BattlePokemon):
        print(f'{_out.pokemon.pokemon.name} switches out.')
        self.bench_pkm[_out.side].remove(_in)
        self.bench_pkm[_out.side].append(_out.pokemon)
        _out.pokemon = _in
        print(f'Go {_in.pokemon.name}!')
