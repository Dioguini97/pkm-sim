from entities import CompetitivePokemon, Move


def calculate_damage(pokemon_atk: CompetitivePokemon, pokemon_def: CompetitivePokemon, move: Move):

    return (2*pokemon_atk.level/5 + 2)