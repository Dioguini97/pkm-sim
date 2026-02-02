from pkm_sim.battle_env.entities.field import Field
from pkm_sim.battle_env.entities.pokemon import BattlePokemon
from pkm_sim.battle_env.entities.pokemon_party import PokemonParty
from pkm_sim.battle_env.turn import Action, Turn


class Battle:
    def __init__(self, parties: list[PokemonParty]):
        self.id = id(self)
        self.teams: list[list[BattlePokemon]] = [] # 4 pkm
        self.parties =  parties # 6 pkm
        self.field = None  # Placeholder for Field object
        self.number_of_turns = 0
        self.init_battle()

    def chose_order_pokemon(self, player_ind: int, player_order: list[int]):
        if len(player_order) != 4:
            raise Exception('You have to chose 4 Pokemon!')
        team: list[BattlePokemon] = []
        for ind, pkm in enumerate(self.parties[player_ind].pokemons):
            if ind in player_order:
                team.append(pkm)
        self.teams.append(team)


    def init_battle(self):
        for player in range(len(self.parties)):
            self.chose_order_pokemon(player, [0,1,2,3]) # tenho que arranjar maneira de fazer esta parte TODO
        self.set_up_field()

    def is_battle_over(self):
        return self.have_all_fainted(self.teams[0]) or self.have_all_fainted(self.teams[1])

    def have_all_fainted(self, team: list[BattlePokemon]):
        return all(pkm.current_hp <= 0 for pkm in team)

    def set_up_field(self):
        field = Field(
            weather=None,
            terrain=None,
            gravity=False,
            trick_room=False,
            side_conditions=[None, None],
            active_pkm=[self.teams[0][:2], self.teams[1][:2]],
            bench_pkm=[self.teams[0][2:], self.teams[1][2:]]
        )
        self.field = field

    def switch_pokemon(self, team_ind: int, slot_ind: int, switch: BattlePokemon):
        self.teams[team_ind][slot_ind].reset_stat_changes()
        self.field.slot_pkm[team_ind][slot_ind] = switch
        self.field.bench_pkm.remove(switch)
        self.field.bench_pkm.append(self.teams[team_ind][slot_ind])

    def choose_action(self, team_ind: int, slot_ind: int):
        print(f'Player {team_ind+1}, choose action for {self.teams[team_ind][slot_ind].pokemon}')
        action_type = input('Choose action: Attack, Switch, Run\n').lower()
        if action_type == 'attack':
            transformation = input('Choose transformation (tera, mega, dynamax, else -> none): ').lower()
            transformation = None if transformation not in ['tera', 'mega', 'dynamax'] else transformation
            for ind, move in enumerate(self.teams[team_ind][slot_ind].battle_moves):
                print(f'{ind}. {move.move.name} (PP: {move.move.pp})')
            move_ind = int(input('Choose move index: '))
            move = self.teams[team_ind][slot_ind].battle_moves[move_ind]
            print('Chose your target: ')
            for ind, pkm in enumerate(self.field.slot_pkm[1 - team_ind]):
                print(f'{ind}. {pkm.pokemon.name} (HP: {(pkm.current_hp/pkm.hp_total)*100}%)')
            target = int(input('Choose target index: '))
            return Action(team_ind, slot_ind, move, None, transformation, action_type, target)
        elif action_type == 'switch':
            for ind, pkm in enumerate(self.field.bench_pkm[team_ind]):
                if pkm.current_hp > 0:
                    print(f'{ind}. {pkm}')
            switch_ind = int(input('Choose switch index: '))
            switch = self.teams[team_ind][switch_ind]
            return Action(team_ind, slot_ind, None, switch, None, action_type, None)
        else:
            return Action(team_ind, slot_ind, None, None, None, "run", None)

    def execute(self):
        while not self.is_battle_over():
            self.number_of_turns += 1
            print(f'--- Turn {self.number_of_turns} ---')
            actions = []
            for team_ind in range(2):
                for slot_ind in range(2):
                    action = self.choose_action(team_ind, slot_ind)
                    actions.append(action)
            turn = Turn(self.number_of_turns, self.field, actions)
            turn.execute_turn()
            # results = turn.execute_turn()
            # for result in results:
            #     print(result)
        print('Battle Over!')
