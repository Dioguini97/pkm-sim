import json
from pathlib import Path

from api.pokeAPI import PokeAPIService
from entities import Pokemon, Move
from entities.move import map_json_to_move
from entities.pokemon import map_json_to_pkm


poke_api_service = PokeAPIService()

class Cache:
    """Class to handle caching of Pokémon data."""
    def __init__(self):
        self.CACHE_DIR = Path("C:\\Users\diogo\PycharmProjects\pkm-sim\src\data\cache")
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)


    def get_pokemon_path_from_cache(self, name: str) -> Path:
        """Returns the path to the cached Pokémon data file."""
        return self.CACHE_DIR / "pokemon" / f"{name}.json"

    def get_move_path_from_cache(self, name: str) -> Path:
        """Returns the path to the cached move data file."""
        return self.CACHE_DIR / "move" / f"{name}.json"

    def get_pokemon_from_cache(self, name: str) -> Pokemon:
        """Returns the cached Pokémon data file if it exists, else None."""
        path = self.get_pokemon_path_from_cache(name)
        if self.is_pokemon_in_cache(name):
            with open(path, 'r') as file:
                json_f = json.load(file)
            return map_json_to_pkm(json_f)
        else:
            self.add_pokemon_to_cache(poke_api_service.get_pokemon(name))
            self.get_pokemon_from_cache(name)

    def get_move_from_cache(self, name: str) -> Move:
        """Returns the cached move data file if it exists, else None."""
        path = self.get_move_path_from_cache(name)
        if self.is_move_in_cache(name):
            with open(path, 'r') as file:
                json_f = json.load(file)
            return map_json_to_move(json_f)
        else:
            self.add_move_to_cache(poke_api_service.get_move(name))
            return self.get_move_from_cache(name)

    def is_pokemon_in_cache(self, name: str) -> bool:
        """Checks if the Pokémon data is cached."""
        path = self.get_pokemon_path_from_cache(name)
        return path.exists()

    def is_move_in_cache(self, name: str) -> bool:
        """Checks if the move data is cached."""
        path = self.get_move_path_from_cache(name)
        return path.exists()

    def add_pokemon_to_cache(self, pokemon: Pokemon):
        if not self.is_pokemon_in_cache(pokemon.name):
            file_path = self.CACHE_DIR / "pokemon"/ f"{pokemon.name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(pokemon.__dict__, file, ensure_ascii=False)
        else:
            pass

    def add_move_to_cache(self, move: Move):
        if not self.is_move_in_cache(move.name):
            file_path = self.CACHE_DIR / "move"/ f"{move.name}.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w', encoding="utf-8") as file:
                json.dump(move.__dict__, file, ensure_ascii=False)
        else:
            pass