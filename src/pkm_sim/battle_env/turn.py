from pkm_sim.battle_env.field import Field
from pkm_sim.battle_env.pokemon import BattlePokemon
from entities import Move


class Action:
    def __init__(self,user: BattlePokemon, move: Move|None, switch: BattlePokemon|None, transformation: str|None):
        self.user = user
        self.move = move
        self.switch = switch
        self.transformation = transformation # Tera, Mega, Dynamax, etc.

    def __repr__(self):
        return f"Action(User: {self.user.pokemon.name}, Move: {self.move.name})"


class Turn:
    def __init__(self, turn_number: int, field_state: Field, actions: list[Action]):
        self.turn_number = turn_number
        self.actions = actions
        self.field_state = field_state


    def __repr__(self):
        return f"Turn({self.turn_number}, Actions: {self.actions})"

    def order_actions(self):
        return sorted(
            self.actions,
            key=lambda action: (
                action.move.priority,
                action.user.pokemon.base_stats['spd']
            ),
            reverse=True
        )

    def execute_turn(self):

        # Switch Phase
        ordered_switches = [(action.user, action.switch) for action in self.actions if action.switch is not None]
        for user, switch in ordered_switches:
            pass
        # Transformation Phase TODO later
        # Move Phase
        # Field/Status Effects Phase

        ordered_actions = self.order_actions()
        results = []
        for action in ordered_actions:
            result = action.user.attack(target=action.user, move=action.move)  # Simplified: user attacks itself
            results.append(result)
        return results

