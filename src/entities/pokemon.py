class Pokemon:
    def __init__(self, name: str, types: list, id: int, base_stats: dict, abilities: list, height: float, weight: float, move_list: list, img_url: str):
        self.name = name
        self.types = types
        self.id = id
        self.base_stats = base_stats
        self.abilities = abilities
        self.height = height
        self.weight = weight
        self.move_list = move_list
        self.img_url = img_url

    def __str__(self):
        return f"{self.name} (ID: {self.id}) - Types: {', '.join(self.types)}\n" \
               f"Base Stats: {self.base_stats}\n" \
               f"Abilities: {', '.join(self.abilities)}\n" \
               f"Height: {self.height}, Weight: {self.weight} \n"

def map_json_to_pkm(json_data):
    name = json_data['name']
    types = [t for t in json_data['types']]
    id = json_data['id']
    base_stats = json_data['base_stats']
    abilities = [ability for ability in json_data['abilities']]
    height = json_data['height']
    weight = json_data['weight']
    move_list = [move for move in json_data['move_list']]
    img_url = json_data['img_url']

    return Pokemon(name, types, id, base_stats, abilities, height, weight, move_list, img_url)