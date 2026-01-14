import requests
from sympy.strategies.core import switch

from entities import Pokemon, Move


class PokeAPIError(Exception):
    """Custom exception for PokeAPI errors."""
    pass

class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name_or_id):
        """Fetches Pokémon data by name or ID."""
        url = f"{self.BASE_URL}pokemon/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching Pokémon data: {response.status_code}")
        pokemon = Pokemon(
            name=response.json()['name'],
            types=[t['type']['name'] for t in response.json()['types']],
            id=response.json()['id'],
            abilities=[a['ability']['name'] for a in response.json()['abilities']]
        )
        return pokemon

    def get_ability(self, name_or_id):
        """Fetches ability data by name or ID."""
        pass

    def get_type(self, name_or_id):
        """Fetches type data by name or ID."""
        pass

    def get_move(self, name_or_id):
        """Fetches move data by name or ID."""
        url = f"{self.BASE_URL}move/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching move data: {response.status_code}")
        json = response.json()
        name = [x['name'] for x in json['names'] if x['language']['name'] == 'en'][0]
        entry = [x['flavor_text'] for x in json['flavor_text_entries'] if x['language']['name'] == 'en'][0]
        stat_changes=list([change['stat']['name'], change['change']] for change in json['stat_changes'])
        for change in stat_changes:
            match change[0]:
                case "attack":
                    change[0] = "atk"
                case "defense":
                    change[0] = "def"
                case "special-attack":
                    change[0] = "spatk"
                case "special-defense":
                    change[0] = "spdef"
                case "speed":
                    change[0] = "spd"
        move = Move(
            id=json['id'],
            name=name,
            api_name=json['name'],
            power=json['power'],
            accuracy=json['accuracy'],
            move_type=json['type']['name'],
            effect_chance=json.get('effect_chance'),
            damage_class=json['damage_class']['name'],
            pp=json['pp'],
            priority=json['priority'],
            stat_changes=stat_changes,
            target=json['target']['name'],
            entries=entry
        )
        return move