from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from utils import generate_uuid


class PokemonParty:
    def __init__(self, pokemons: list[BattlePokemon], name: str = None):
        self.id = generate_uuid()
        self.pokemons = pokemons
        self.name = name
        if name is None:
            self.name = self.id