class PokemonSpecies:
    def __init__(self, id: int, name: str, evolution_chain, varieties: list=None):
        self.id = id
        self.name = name
        self.evolution_chain = evolution_chain
        self.does_it_evolve = self.can_evolve(self.evolution_chain)
        self.varieties = varieties

    def can_evolve(self, evo_chain) -> bool:
        """Checks if the Pokémon can evolve based on cached species data."""
        if evo_chain['chain']['species']['name'] == self.name:
            if len(evo_chain['chain']['evolves_to']) > 0:
                return True
            else:
                return False
        else:
            for evolution in evo_chain['chain']['evolves_to']:
                if evolution['species']['name'] == self.name:
                    if len(evolution['evolves_to']) > 0:
                        return True
                    else:
                        return False
            return False

class Pokemon(PokemonSpecies):
    def __init__(self, id: int, name: str, evolution_chain, varieties: list|None, types: list, base_stats: dict,
                 abilities: list, height: float, weight: float, move_list: list, img_url: str, crie_url: str):
        super().__init__(id, name, evolution_chain, varieties)
        self.types = types
        self.base_stats = base_stats
        self.abilities = abilities
        self.height = height
        self.weight = weight
        self.move_list = move_list
        self.img_url = img_url
        self.crie_url = crie_url

    def __str__(self):
        return f"{self.name} (ID: {self.id}) - Types: {', '.join(self.types)}\n" \
               f"Base Stats: {self.base_stats}\n" \
               f"Abilities: {', '.join(self.abilities)}\n" \
               f"Height: {self.height}, Weight: {self.weight} \n"


def map_json_to_pkm(json_data):
    return Pokemon(
        name = json_data['name'], types = json_data['types'], id = json_data['id'],
        base_stats = json_data['base_stats'], abilities = json_data['abilities'],
        height = json_data['height'], weight = json_data['weight'], move_list = json_data['move_list'],
        img_url = json_data['img_url'], evolution_chain_id=json_data['evolution_chain_id'],
        varieties=json_data['varieties']
    )

def map_json_to_pkm_sp(json) -> PokemonSpecies:
    pkm = PokemonSpecies(
        name=json['name'],
        id=json['id'],
        evolution_chain_id=json['evolution_chain_id'],
        varieties=json['varieties']
    )
    pkm.does_it_evolve = json['does_it_evolve']
    return pkm