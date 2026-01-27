from enum import Enum


class Status(Enum):
    """Enum representing various status conditions in a Pokémon battle environment."""

    BURN = "burn"
    PARALYSIS = "paralysis"
    POISON = "poison"
    BADLY_POISON = "badly-poison"
    SLEEP = "sleep"
    FROZEN = "frozen"
    FAINTED = "fainted"

class Effect(Enum):
    """Enum representing various condition effect in a Pokémon battle environment."""

    CONFUSION = "confusion"
    TRAPPED = "trapped"
    SEEDED = "seeded"
    PERISH_SONG = "perish-song"