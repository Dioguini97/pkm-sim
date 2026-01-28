import json
from pathlib import Path

from api.pokeAPI import PokeAPIService
from api.models import Pokemon, Move
from api.models.move import map_json_to_move
from api.models.pokemon import map_json_to_pkm, PokemonSpecies, map_json_to_pkm_sp

poke_api_service = PokeAPIService()

class Cache:
    """Class to handle caching of Pokémon data."""
    def __init__(self):
        self.CACHE_DIR = Path("C:\\Users\diogo\PycharmProjects\pkm-sim\src\data\cache")
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)


    def get_pokemon_species_path_from_cache(self, name: str) -> Path:
        """Returns the path to the cached Pokémon data file."""
        return self.CACHE_DIR / "pokemon-species" / f"{name}.json"

    def get_pokemon_path_from_cache(self, name: str) -> Path:
        """Returns the path to the cached Pokémon data file."""
        return self.CACHE_DIR / "pokemon" / f"{name}.json"

    def get_move_path_from_cache(self, name: str) -> Path:
        """Returns the path to the cached move data file."""
        return self.CACHE_DIR / "move" / f"{name}.json"

    def get_evolution_chain_path_from_cache(self, id: int) -> Path:
        """Returns the path to the cached evolution chain data file."""
        return self.CACHE_DIR / "evolution-chain" / f"{id}.json"

    def get_pokemon_species_from_cache(self, name: str) -> PokemonSpecies:
        """Returns the cached Pokémon species data file if it exists, else None."""
        path = self.get_pokemon_species_path_from_cache(name)
        if self.is_pokemon_species_in_cache(name):
            with open(path, 'r') as file:
                json_f = json.load(file)
            file.close()
            return map_json_to_pkm_sp(json_f)
        else:
            pkm = poke_api_service.get_pokemon_species(name)
            self.add_pokemon_species_to_cache(pkm)
            return pkm

    def get_pokemon_from_cache(self, name: str) -> Pokemon:
        """Returns the cached Pokémon data file if it exists, else None."""
        path = self.get_pokemon_path_from_cache(name)
        if self.is_pokemon_in_cache(name):
            with open(path, 'r') as file:
                json_f = json.load(file)
            return map_json_to_pkm(json_f)
        else:
            pkm = poke_api_service.get_pokemon(name)
            self.add_pokemon_to_cache(pkm)
            return pkm

    def get_move_from_cache(self, name: str) -> Move:
        """Returns the cached move data file if it exists, else None."""
        path = self.get_move_path_from_cache(name)
        if self.is_move_in_cache(name):
            with open(path, 'r') as file:
                json_f = json.load(file)
            return map_json_to_move(json_f)
        else:
            move = poke_api_service.get_move(name)
            self.add_move_to_cache(move)
            return move

    def is_pokemon_in_cache(self, name: str) -> bool:
        """Checks if the Pokémon data is cached."""
        path = self.get_pokemon_path_from_cache(name)
        return path.exists()

    def is_pokemon_species_in_cache(self, name: str) -> bool:
        """Checks if the Pokémon species data is cached."""
        path = self.get_pokemon_species_path_from_cache(name)
        return path.exists()

    def is_move_in_cache(self, name: str) -> bool:
        """Checks if the move data is cached."""
        path = self.get_move_path_from_cache(name)
        return path.exists()

    def is_evolution_chain_in_cache(self, id: int) -> bool:
        """Checks if the evolution chain data is cached."""
        path = self.get_evolution_chain_path_from_cache(id)
        return path.exists()

    def add_pokemon_to_cache(self, pokemon: Pokemon):
        species = self.get_pokemon_species_from_cache(pokemon.name.split('-')[0])
        pokemon.varieties = species.varieties
        pokemon.evolution_chain = species.evolution_chain
        if not self.is_pokemon_in_cache(pokemon.name):
            file_path = self.CACHE_DIR / "pokemon"/ f"{pokemon.name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(pokemon.__dict__, file, ensure_ascii=False, indent=4)
        else:
            pass

    def add_move_to_cache(self, move: Move):
        if not self.is_move_in_cache(move.name):
            file_path = self.CACHE_DIR / "move"/ f"{move.name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(move.__dict__, file, ensure_ascii=False, indent=4)
        else:
            pass

    def add_pokemon_species_to_cache(self, pokemon_species: PokemonSpecies):
        if not self.is_pokemon_species_in_cache(pokemon_species.name):
            file_path = self.CACHE_DIR / "pokemon-species"/ f"{pokemon_species.name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(pokemon_species.__dict__, file, ensure_ascii=False, indent=4)
        else:
            pass

    def get_evolution_chain_from_cache(self, id: int):
        """Returns the cached evolution chain data file if it exists, else None."""
        path = self.CACHE_DIR / "evolution-chain" / f"{id}.json"
        if path.exists():
            with open(path, 'r') as file:
                json_f = json.load(file)
            return json_f
        else:
            evo_chain = poke_api_service.get_evolution_chain(id)
            self.add_evolution_chain_to_cache(id, evo_chain)
            return evo_chain

    def add_evolution_chain_to_cache(self, id, evo_chain):
        if not self.is_evolution_chain_in_cache(id):
            file_path = self.CACHE_DIR / "evolution-chain"/ f"{id}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(evo_chain, file, ensure_ascii=False, indent=4)
        else:
            pass


