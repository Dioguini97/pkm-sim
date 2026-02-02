from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.pokemon_builder.competitive_pokemon import CompetitivePokemon


class PokemonConfig:
    def __init__(self, name, species, moves, tera_type, ability, nature, ivs=None, evs=None, item=None):
        self.name = name
        self.species = species
        self.moves = moves
        self.tera_type = tera_type
        self.ability = ability
        self.nature = nature
        self.ivs = ivs
        self.evs = evs
        self.item = item

    def get_battle_pokemon(self):
        competitive_pokemon = CompetitivePokemon(
            name=self.species,
            nickname=self.name,
            ability=self.ability,
            nature=self.nature,
            moves=self.moves,
            ivs=self.ivs,
            evs=self.evs,
            item=self.item
        )
        return BattlePokemon(competitive_pokemon)