# Guia de Uso: Arquitetura Move/BattleMove

## Como Usar BattleMove

### 1. Criar um BattleMove a partir de um Move

```python
from api.models import Move
from pkm_sim.battle_env.entities.move import BattleMove

# Move vem do cache ou da API
move = cache.get_move_from_cache("thunderbolt")

# Criar BattleMove com estado dinâmico
battle_move = BattleMove(move)
print(battle_move)  # "Thunderbolt (15/15)"
```

### 2. BattlePokemon cria BattleMoves automaticamente

```python
from pkm_sim.battle_env.entities.pokemon import BattlePokemon

# BattlePokemon.get_info_moves() retorna list[BattleMove]
battle_pokemon = BattlePokemon(competitive_pokemon)

# Obter um move específico
battle_move = battle_pokemon.get_move("Thunderbolt")
# battle_move é do tipo BattleMove
```

### 3. Executar um Move durante a Batalha

```python
from pkm_sim.battle_env.turn import Action, Turn

# Criar Action com BattleMove
action = Action(
    player=0,
    user=attacker,  # BattlePokemon
    battle_move=battle_move,  # BattleMove
    switch=None,
    transformation=None,
    action_type='attack',
    target=1  # índice do alvo
)

# Executar turno (que vai executar moves na Phase 3)
turn = Turn(turn_number=1, field_state=field, actions=[action, action2])
result = turn.execute_turn()

# Resultado contém informação sobre dano, efeitos, etc
print(result['moves'])  # Lista de resultados de moves
```

### 4. Acessar Resultado da Execução de um Move

```python
# BattleMove.execute() retorna dict com:
result = battle_move.execute(attacker, defender, field)

print(result)
# {
#     'success': bool,
#     'damage': int,
#     'effects_applied': ['Pikachu's Spdef was decreased!', ...],
#     'message': str
# }
```

### 5. Gerenciar PP

```python
# Consumir PP
if battle_move.consume_pp(1):  # Tenta consumir 1 PP
    print("Move executado")
else:
    print("Sem PP!")

# Restaurar PP
battle_move.restore_pp(5)  # Restaura 5 PP
battle_move.reset_pp()     # Restaura ao máximo

# Ver PP atual
print(battle_move.pp_remaining)  # 14/15
```

## Fluxo Completo de Batalha

```python
# 1. Setup inicial
from src.pkm_sim.battle_env.battle import Battle
from pkm_sim.battle_env.entities.field import Field
from pkm_sim.battle_env.turn import Turn, Action

battle = Battle(parties=[team1, team2])

# 2. Loop de turnos
while not battle.is_battle_over():
    # Obter ações dos jogadores
    action_p1 = get_action(battle, player=0)  # Retorna Action com BattleMove
    action_p2 = get_action(battle, player=1)

    # Executar turno (5 fases)
    turn = Turn(
        turn_number=battle.number_of_turns,
        field_state=battle.field,
        actions=[action_p1, action_p2]
    )
    result = turn.execute_turn()

    # Processar resultado
    for move_result in result['moves']:
        print(move_result['message'])

    for fainted in result['fainting']:
        print(fainted)

    battle.number_of_turns += 1

# 3. Determinar vencedor
if battle.have_all_fainted(battle.teams[0]):
    print("Player 2 wins!")
else:
    print("Player 1 wins!")
```

## As 5 Fases de um Turno

### Phase 1: Switch Phase
- Pokémon trocam de lugar
- Executado em ordem de **velocidade** (decrescente)
- Ativa abilities de entrada

### Phase 2: Transformation Phase
- Aplicam-se Tera, Mega, Dynamax
- Executado em ordem de **velocidade** (decrescente)

### Phase 3: Move Phase
- Pokémon atacam
- Executado em ordem de **prioridade** (decrescente) e depois **velocidade** (decrescente)
- **`BattleMove.execute()` é chamado aqui**

### Phase 4: Fainting Phase
- Remove Pokémon com HP ≤ 0
- Executado em ordem de **velocidade** (decrescente)
- Desativa abilities

### Phase 5: End-of-Turn Effects
- Weather damage, terrain damage, status damage
- Executed em ordem de **velocidade** (decrescente)
- (TODO: ainda não implementado)

## Arquitetura Interna

```
Move (entities/move.py)
 ↓
 └── Dados estáticos: power, accuracy, type, PP máximo, etc.

BattleMove (battle_env/move.py)
 ├── Dados dinâmicos: PP atual
 ├── execute(user, target, field) → executa o move
 ├── consume_pp() / restore_pp() / reset_pp()
 └── Métodos privados:
     ├── _calculate_damage()
     ├── _check_move_accuracy()
     ├── _apply_secondary_effects()
     ├── _apply_stat_change()
     ├── _apply_status_condition()
     ├── _apply_drain_effect()
     └── _apply_healing_effect()

BattlePokemon (battle_env/pokemon.py)
 ├── battle_moves: list[BattleMove]
 ├── get_info_moves() → cria BattleMove para cada move
 ├── get_move(name) → retorna BattleMove
 └── attack(target, battle_move, field) → delega a battle_move.execute()

Turn (battle_env/turn.py)
 ├── execute_turn() → executa 5 fases
 ├── _execute_move_phase() → ordena e executa BattleMove.execute()
 └── order_actions_for_moves() → ordena por prioridade e velocidade
```

## Exemplos de Testes

Ver ficheiros:
- `tests/test_move_battlemove_integration.py` - Testes de BattleMove
- `tests/test_turn.py` - Testes de Turn e 5 fases

```bash
pytest tests/test_move_battlemove_integration.py -v
pytest tests/test_turn.py -v
```

## TODO Futuros

- [ ] Implementar `_execute_status_move()` com logic completa
- [ ] Implementar `_execute_end_of_turn_phase()` com weather/terrain damage
- [ ] Integrar com Field para fazer trocas reais
- [ ] Implementar transformações reais
- [ ] Melhorar lógica de targeting (multi-target moves)
- [ ] Adicionar ability activation/deactivation
- [ ] Implementar field setters (Stealth Rock, Spikes, etc)
- [ ] Validar targets para cada move
