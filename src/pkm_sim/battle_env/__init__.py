import math
import random


def damage_calculation(attacker_stat: int, defender_stat: int, move_power: int, targets: float, weather: float, critical_hit: bool, stab: float, type_: float, burn: float=1.0,GLAIVE_RUSH: int=1.0, PB: float=1.0, other: float=1.0, z_move: float=1.0) -> int:
    # targets is 1 for single target, 0.75 for multiple targets
    # PB is 0.25 if move is second hit from parental bond ability, else 1
    # weather is 1.5 for weather boosting move type, 0.5 for weather weakening move type, else 1
    # GLAIVE_RUSH is 2 if the target used Glaive Rush at previous turn, else 1
    # stab is 1.5 if move type matches attacker's type, 2 if the user as adapbility else 1
    # Type is the type effectiveness. This can be 0.125, 0.25, 0.5 (not very effective); 1 (normally effective); 2, 4, or 8 (super effective)
    # Burn is 0.5 if the attacker is burned, its Ability is not Guts, and the used move is a physical move (other than Facade from Generation VI onward), and 1 otherwise.
    # Other TODO
    # ZMove is 0.25 if the move is a Z-Move or Max Move and the target would be protected from that move (e.g. by Protect), and 1 otherwise.
    # Tera Shield é para tera raids, não vou adicionar.
    if critical_hit:
        critical = 1.5
    else:
        critical = 1.0
    random_ = random.randint(85, 100) / 100.0
    return math.floor(((((2*50/5 + 2) * move_power * (attacker_stat / defender_stat)) / 50) + 2) * targets * PB * weather * GLAIVE_RUSH * critical * random_ * stab * type_ * burn)


