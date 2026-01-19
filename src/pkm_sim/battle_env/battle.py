from pkm_sim.battle_env.pokemon import BattlePokemon


class Battle:
    def __init__(self, parties: list[list[BattlePokemon]]):
        self.teams = [] # 4 pkm
        self.parties =  parties # 6 pkm
        self.init_battle()

    def chose_order_pokemon(self):
        for player, party in enumerate(self.parties):
            print(f'Player {player}, choose the order your Pokémon will take (can only chose 4):')
            print(f'{i}. {pokemon.pokemon.name}' for i, pokemon in enumerate(party))
            chosen_order = input('Escolha a ordem colando o número do Pokemon por ordem que quer. (ex. 2 4 6 3)')
            chosen_order = chosen_order.split(' ')
            team = []
            for j in chosen_order:
                self.teams.append(team.append(party[int(j)]))

    def init_battle(self):
        self.chose_order_pokemon()

    def is_battle_over(self):
        return self.have_all_fainted(self.teams[0]) or self.have_all_fainted(self.teams[1])

    def have_all_fainted(self, team: list[BattlePokemon]):
        fainted = [True for pkm in team if pkm.current_hp <= 0]
        return fainted.count(True) == 4