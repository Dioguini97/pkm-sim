# class Ailment:
#     """Base class for status ailments in a Pokémon battle environment."""
#
#     def __init__(self, name: str, pokemon=None, duration: int|None = None):
#         self.name = name # Name of the ailment (e.g., Status: "Burn", "Poison", "Perish Song", "Confusion", "Trap??", "Seeded")
#         self.pokemon = pokemon
#         self.duration = duration
#         self.count_turns = 1 if self.duration is None else None
#
#     def tick(self):
#         """Decrease the duration of the ailment by one turn."""
#         if self.duration > 0:
#             self.duration -= 1
#
# class Burn(Ailment):
#     def __init__(self, pokemon):
#         super().__init__("burn", pokemon, None)
#
#     def apply_effect(self):
#         # Apply burn effect (e.g., reduce HP each turn)
#         burn_damage = max(1, self.pokemon.hp_total // 16)
#         self.pokemon.apply_damage(max(1, burn_damage))
#         return f"{self.pokemon.pokemon.name} is hurt by its burn and loses {burn_damage} HP!"
#
# class BadlyPoison(Ailment):
#     def __init__(self, pokemon):
#         super().__init__("badly-poison", pokemon, None)
#
#     def apply_effect(self):
#         poison_damage = max(1, (self.pokemon.hp_total // 16) + (self.count_turns*(self.pokemon.hp_total//16)))
#         self.pokemon.apply_damage(max(1, poison_damage))
#         self.count_turns += 1
#         return f"{self.pokemon.pokemon.name} is hurt by its burn and loses {poison_damage} HP!"