import requests

from api.models import Pokemon, Move, PokemonSpecies
from api.models import Ability
from utils import transform_stat_name, from_name_to_api_read


class PokeAPIError(Exception):
    """Custom exception for PokeAPI errors."""
    pass

class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2/"

    def get_pokemon_species(self, name_or_id) -> PokemonSpecies:
        """Fetches Pokémon species data by name or ID."""
        url = f"{self.BASE_URL}pokemon-species/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching Pokémon species data: {response.status_code}")
        return PokemonSpecies(
            name=response.json()['name'],
            id=response.json()['id'],
            evolution_chain=self.get_evolution_chain(response.json()['evolution_chain']['url'].split('/')[-2]),
            varieties=[variety for variety in response.json()['varieties']]
        )

    def get_evolution_chain(self, id):
        """Fetches evolution chain data by ID."""
        url = f'{self.BASE_URL}evolution-chain/{id}/'
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching evolution chain data: {response.status_code}")
        return response.json()

    def get_pokemon(self, name_or_id):
        """Fetches Pokémon data by name or ID."""
        url = f"{self.BASE_URL}pokemon/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching Pokémon data: {response.status_code}")
        pokemon = Pokemon(
            name=response.json()['name'],
            types=[t['type']['name'].lower() for t in response.json()['types']],
            id=response.json()['id'],
            abilities=[a['ability']['name'] for a in response.json()['abilities']],
            height=response.json()['height'],
            weight=response.json()['weight'],
            move_list=[m['move']['name'] for m in response.json()['moves']],
            base_stats={transform_stat_name(stat['stat']['name']): stat['base_stat'] for stat in response.json()['stats']},
            img_url=response.json()['sprites']['front_default'],
            evolution_chain=None,
            varieties=None,
            crie_url=response.json()['cries']['latest']
        )
        return pokemon

    def get_ability(self, name_or_id):
        """Fetches ability data by name or ID."""
        pass

    def get_move(self, name_or_id):
        """Fetches move data by name or ID."""
        name_or_id = from_name_to_api_read(name_or_id)
        url = f"{self.BASE_URL}move/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching move data: {response.status_code}")
        json = response.json()
        entry = [x['flavor_text'] for x in json['flavor_text_entries'] if x['language']['name'] == 'en'][0]
        stat_changes=list([transform_stat_name(change['stat']['name']), change['change']] for change in json['stat_changes'])
        move = Move(
            id=json['id'],
            name=json['name'],
            power=json['power'],
            accuracy=json['accuracy'],
            move_type=json['type']['name'],
            effect_chance=json.get('effect_chance'),
            damage_class=json['damage_class']['name'],
            pp=json['pp'],
            priority=json['priority'],
            stat_changes=stat_changes,
            target=json['target']['name'],
            entries=entry,
            crit_rate=json['meta']['crit_rate'],
            ailment=json['meta']['ailment']['name'],
            ailment_chance=json['meta']['ailment_chance'],
            category=json['meta']['category']['name'],
            drain=json['meta']['drain'],
            flinch_chance=json['meta']['flinch_chance'],
            healing=json['meta']['healing'],
            min_hits=json['meta']['min_hits'],
            max_hits=json['meta']['max_hits'],
            min_turns=json['meta']['min_turns'],
            max_turns=json['meta']['max_turns'],
            stat_chance=json['meta']['stat_chance']
        )
        return move

    def get_ability(self, name_or_id):
        """Fetches ability data by name or ID."""
        url = f"{self.BASE_URL}ability/{name_or_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            raise PokeAPIError(f"Error fetching ability data: {response.status_code}")
        json = response.json()
        description = [x['short_effect'] for x in json['effect_entries'] if x['language']['name'] == 'en'][0]
        return Ability(
            id=json['id'],
            name=json['name'],
            description=description
        )


