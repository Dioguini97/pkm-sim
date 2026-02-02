from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.status import Status


class BattleSlot:
    def __init__(self, side: int, index: int):
        self.side = side
        self.index = index
        self.pokemon: BattlePokemon | None = None
        self.is_protected_by = None

    def is_empty(self):
        return self.pokemon is None

    def is_pokemon_fainted(self):
        return (self.pokemon.current_hp <= 0) | (self.pokemon.status == Status.FAINTED)

    def set_pokemon(self, pokemon: BattlePokemon):
        self.pokemon = pokemon


class Field:
    def __init__(self, weather=None, terrain=None, gravity=False, trick_room=False, side_conditions=None, active_pkm: list[list]=None,bench_pkm: list[list]=None):
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
        for ind, team in enumerate(active_pkm):
            for index, pokemon in enumerate(team):
                self.slots[ind][index].set_pokemon(pokemon)
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

    def get_pokemon_number_on_field(self):
        count = 0
        for side in self.slots:
            for slot in side:
                if not slot.is_empty():
                    count += 1
        return count

    def get_foe_effective_slot_number(self, user_side_index: int) -> int:
        foe_side = self.slots[1 - user_side_index]
        return sum(
            1 for slot in foe_side if not slot.is_pokemon_fainted()
        )

    def get_ally_is_fainted_int(self, user_side_index: int, user_slot_index: int):
        return 0 if self.slots[user_side_index][1 - user_slot_index].is_pokemon_fainted() else 1


