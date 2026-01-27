"""
Exemplo completo: Fluxo de uma batalha com a arquitetura Move/BattleMove
Este é um exemplo de pseudocódigo para demonstrar como tudo funciona junto.
"""

# ==============================================================================
# SETUP INICIAL
# ==============================================================================

from src.pkm_sim.battle_env.battle import Battle
from pkm_sim.battle_env.turn import Turn, Action

# 1. Criar duas equipas (cada uma com 6 Pokémon)
from api.models import CompetitivePokemon

# Criar Pokémon competitivos com moves
pikachu = CompetitivePokemon(
    name="Pikachu",
    species_id=25,
    moves=["Thunderbolt", "Quick Attack", "Thunder Wave", "Iron Tail"]
)

charizard = CompetitivePokemon(
    name="Charizard",
    species_id=6,
    moves=["Flare Blitz", "Dragon Claw", "Earthquake", "Roost"]
)

# ... mais Pokémon ...

team1 = [pikachu, charizard]  # Simplificado: só 2 Pokémon
team2 = [blastoise, venusaur]  # Oponente

# 2. Criar batalha
battle = Battle(parties=[team1, team2])

# Resultado: battle.teams contém list[list[BattlePokemon]]
# battle.teams[0] = [BattlePokemon(pikachu), BattlePokemon(charizard)]
# battle.teams[1] = [BattlePokemon(blastoise), BattlePokemon(venusaur)]

# 3. Setup do field
# battle.field.slot_pkm = [[pikachu_battle, charizard_battle], [blastoise_battle, venusaur_battle]]


# ==============================================================================
# TURNO 1: SETUP
# ==============================================================================

print("=== TURN 1 ===")

# Jogador 1 escolhe ação para Pikachu (slot 0 do seu lado)
def choose_action_for_player1() -> Action:
    """Simula o jogador 1 escolhendo uma ação"""
    attacker = battle.teams[0][0]  # Pikachu

    # Obter um move
    battle_move = attacker.get_move("Thunderbolt")  # Retorna BattleMove

    # Criar ação de ataque
    action = Action(
        player=0,
        user=attacker,
        battle_move=battle_move,  # ← BattleMove em vez de Move!
        switch=None,
        transformation=None,
        action_type='attack',
        target=0  # Atacar slot 0 do oponente (Blastoise)
    )
    return action

# Jogador 2 escolhe ação para Blastoise (slot 0 do seu lado)
def choose_action_for_player2() -> Action:
    """Simula o jogador 2 escolhendo uma ação"""
    attacker = battle.teams[1][0]  # Blastoise

    # Obter move
    battle_move = attacker.get_move("Hydro Pump")

    # Criar ação de ataque
    action = Action(
        player=1,
        user=attacker,
        battle_move=battle_move,
        switch=None,
        transformation=None,
        action_type='attack',
        target=0  # Atacar slot 0 do oponente (Pikachu)
    )
    return action

# Obter ações
action_p1 = choose_action_for_player1()
action_p2 = choose_action_for_player2()

print(f"Player 1: {action_p1}")
# Output: Action(Player: 0, User: Pikachu, Move: Thunderbolt)

print(f"Player 2: {action_p2}")
# Output: Action(Player: 1, User: Blastoise, Move: Hydro Pump)


# ==============================================================================
# EXECUTAR TURNO: 5 FASES
# ==============================================================================

turn = Turn(
    turn_number=1,
    field_state=battle.field,
    actions=[action_p1, action_p2]
)

result = turn.execute_turn()

# result = {
#     'turn_number': 1,
#     'switches': [],  # Phase 1: nenhuma troca
#     'transformations': [],  # Phase 2: nenhuma transformação
#     'moves': [
#         # Phase 3: resultado dos moves
#         {
#             'success': True,
#             'damage': 87,
#             'effects_applied': [],
#             'message': "Pikachu used Thunderbolt and dealt 87 damage to Blastoise!"
#         },
#         {
#             'success': True,
#             'damage': 92,
#             'effects_applied': [],
#             'message': "Blastoise used Hydro Pump and dealt 92 damage to Pikachu!"
#         }
#     ],
#     'fainting': [],  # Phase 4: nenhum Pokémon desmaiou
#     'end_of_turn_effects': []  # Phase 5: nenhum efeito de final de turno
# }


# ==============================================================================
# PHASE 1: SWITCH PHASE
# ==============================================================================

print("\n--- PHASE 1: SWITCH PHASE ---")
# Se houvesse ações de switch, aqui seriam executadas em ordem de velocidade
for switch_msg in result['switches']:
    print(switch_msg)


# ==============================================================================
# PHASE 2: TRANSFORMATION PHASE
# ==============================================================================

print("\n--- PHASE 2: TRANSFORMATION PHASE ---")
# Se houvesse transformações (Tera, Mega, Dynamax)
for transform_msg in result['transformations']:
    print(transform_msg)


# ==============================================================================
# PHASE 3: MOVE PHASE
# ==============================================================================

print("\n--- PHASE 3: MOVE PHASE ---")

# Os moves são ordenados automaticamente por:
# 1. Prioridade (maior primeiro)
# 2. Velocidade (maior primeiro)

for move_result in result['moves']:
    print(move_result['message'])

    # BattleMove.execute() foi chamado aqui, retornando move_result
    # Internamente, BattleMove.execute() fez:
    # 1. Verificar accuracy
    # 2. Calcular dano
    # 3. Aplicar dano ao target
    # 4. Aplicar efeitos secundários (stat changes, ailments)
    # 5. Consumir PP

    for effect in move_result['effects_applied']:
        print(f"  → {effect}")


# ==============================================================================
# PHASE 4: FAINTING PHASE
# ==============================================================================

print("\n--- PHASE 4: FAINTING PHASE ---")

# Pokémon desmaiados são removidos em ordem de velocidade
for faint_msg in result['fainting']:
    print(faint_msg)
    # Se um Pokémon desmaia, sua ability é desativada (TODO)


# ==============================================================================
# PHASE 5: END-OF-TURN EFFECTS
# ==============================================================================

print("\n--- PHASE 5: END-OF-TURN EFFECTS ---")

# Weather damage, terrain damage, status damage, etc.
for effect_msg in result['end_of_turn_effects']:
    print(effect_msg)


# ==============================================================================
# DEPOIS DO TURNO
# ==============================================================================

print("\n=== AFTER TURN 1 ===")

# Ver HP atual
print(f"Pikachu HP: {battle.teams[0][0].current_hp}/100")  # 100 - 92 = 8
print(f"Blastoise HP: {battle.teams[1][0].current_hp}/100")  # 100 - 87 = 13

# Ver PP restante dos moves
pikachu_tb = battle.teams[0][0].get_move("Thunderbolt")
print(f"Thunderbolt PP: {pikachu_tb.pp_remaining}/{pikachu_tb.move.pp}")  # 14/15


# ==============================================================================
# TURNO 2: SWITCH
# ==============================================================================

print("\n\n=== TURN 2 ===")

# Pikachu está muito fraco, trocar para Charizard
def choose_action_for_player1_turn2() -> Action:
    """Jogador 1 decide trocar para Charizard"""
    pikachu = battle.teams[0][0]  # Pokémon atual
    charizard = battle.teams[0][1]  # Pokémon do bench

    action = Action(
        player=0,
        user=pikachu,
        battle_move=None,  # ← Sem move
        switch=charizard,  # ← Trocar para Charizard
        transformation=None,
        action_type='switch',
        target=None
    )
    return action

# Blastoise continua atacando
def choose_action_for_player2_turn2() -> Action:
    blastoise = battle.teams[1][0]
    battle_move = blastoise.get_move("Ice Beam")

    action = Action(
        player=1,
        user=blastoise,
        battle_move=battle_move,
        switch=None,
        transformation=None,
        action_type='attack',
        target=0  # Seria Charizard agora
    )
    return action

action_p1 = choose_action_for_player1_turn2()
action_p2 = choose_action_for_player2_turn2()

# Executar turno
turn2 = Turn(
    turn_number=2,
    field_state=battle.field,
    actions=[action_p1, action_p2]
)

result2 = turn2.execute_turn()

# --- PHASE 1: SWITCH PHASE ---
# Pikachu switches to Charizard! (ordenado por velocidade)

# --- PHASE 3: MOVE PHASE ---
# Blastoise used Ice Beam (Pikachu já está out)
# Então Charizard (que entrou) recebe o dano
# Charizard used Flare Blitz and dealt X damage to Blastoise!


# ==============================================================================
# LOOP PRINCIPAL DE BATALHA
# ==============================================================================

print("\n\n=== FULL BATTLE LOOP ===")

battle = Battle(parties=[team1, team2])
turn_count = 1

while not battle.is_battle_over():
    print(f"\n--- TURN {turn_count} ---")

    # Obter ações de ambos os jogadores
    action_p1 = choose_action_for_player(battle, player=0)
    action_p2 = choose_action_for_player(battle, player=1)

    # Executar turno
    turn = Turn(
        turn_number=turn_count,
        field_state=battle.field,
        actions=[action_p1, action_p2]
    )
    result = turn.execute_turn()

    # Processar e mostrar resultado
    print("MOVES:")
    for move_result in result['moves']:
        print(f"  {move_result['message']}")

    print("FAINTING:")
    for faint_msg in result['fainting']:
        print(f"  {faint_msg}")

    turn_count += 1

# Determinar vencedor
if battle.have_all_fainted(battle.teams[0]):
    print("\n✓ PLAYER 2 WINS!")
else:
    print("\n✓ PLAYER 1 WINS!")
