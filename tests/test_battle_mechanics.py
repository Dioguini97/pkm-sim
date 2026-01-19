from pkm_sim.battle_env import damage_calculation

def test_damage_calculation():
    damage = damage_calculation(
        123, 161, 65, 1, 1, 1, 1, False, 1.5, 4, 1, 1, 1)
    # assert 112 <= damage <= 136