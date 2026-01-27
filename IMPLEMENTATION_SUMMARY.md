# Implementação: Padrão Move/BattleMove

## Resumo

Foi implementado o padrão `Move`/`BattleMove` similar ao padrão existente `Pokemon`/`BattlePokemon`. Isto separa dados estáticos de moves (definição) do estado dinâmico durante a batalha (PP restante, efeitos aplicados).

## Ficheiros Criados/Modificados

### 1. **Novo: `src/pkm_sim/battle_env/move.py`**

**Classe `BattleMove`:**
- Encapsula um `Move` com estado dinâmico (PP restante)
- Métodos principais:
  - `execute(user, target, field)` - Executa o move completo com todas as fases
  - `consume_pp()` / `restore_pp()` / `reset_pp()` - Gerenciar PP
  
**Métodos de execução:**
- `_check_move_accuracy()` - Verifica hit com accuracy e evasion stages
- `_calculate_damage()` - Calcula dano baseado em stats, tipos, STAB, crit, etc
- `_apply_secondary_effects()` - Aplica stat changes e ailments
- `_apply_drain_effect()` - Aplica efeito de drain
- `_apply_healing_effect()` - Aplica efeito de healing
- `_execute_status_move()` - Executa moves de status (TODO)

**Estrutura de resultado:**
```python
result = {
    'success': bool,
    'damage': int,
    'effects_applied': list[str],
    'message': str
}
```

### 2. **Modificado: `src/pkm_sim/battle_env/pokemon.py`**

- **Import:** Adicionado `from pkm_sim.battle_env.move import BattleMove`
- **`__init__`:** `self.battle_moves` agora contém `list[BattleMove]` em vez de `list[Move]`
- **`attack()`:** Simplificado para delegar lógica a `BattleMove.execute()`
- **`get_info_moves()`:** Retorna `list[BattleMove]` criando instância de `BattleMove` para cada move
- **`get_move()`:** Retorna `BattleMove` e compara por `battle_move.move.name`

### 3. **Modificado: `src/pkm_sim/battle_env/turn.py`**

- **Classe `Action`:** `move` → `battle_move` (tipo `BattleMove`)
- **Método `execute_turn()`:** Refatorado para 5 fases completas:
  1. **Phase 1 - Switch Phase:** Trocas em ordem de velocidade
  2. **Phase 2 - Transformation Phase:** Transformações (Tera, Mega, etc) em ordem de velocidade
  3. **Phase 3 - Move Phase:** Ataques em ordem de prioridade e velocidade
  4. **Phase 4 - Fainting Phase:** Remove Pokémon desmaiados em ordem de velocidade
  5. **Phase 5 - End-of-Turn Phase:** Efeitos finais (TODO)

**Novos métodos privados:**
- `_execute_switch_phase()`
- `_execute_transformation_phase()`
- `_execute_move_phase()` - Chama `battle_move.execute()`
- `_execute_fainting_phase()` - Remove Pokémon com HP ≤ 0
- `_execute_end_of_turn_phase()` - (TODO)

## Fluxo de Execução

### Exemplo: Um Pokémon usando um ataque

```
1. Action criada com BattleMove
2. Turn.execute_turn() é chamado
3. Turn._execute_move_phase() ordena moves por prioridade + velocidade
4. Para cada move ordenado:
   a. BattleMove.execute(user, target, field) é chamado
   b. Verifica accuracy
   c. Calcula dano
   d. Aplica dano ao target
   e. Aplica secondary effects (stat changes, ailments)
   f. Consome PP
   g. Retorna dict com resultado
5. Turn._execute_fainting_phase() remove Pokémon desmaiados
6. Turn._execute_end_of_turn_phase() aplica efeitos finais (TODO)
```

## Benefícios desta Arquitetura

✅ **Separação de responsabilidades:** Move define o move, BattleMove executa na batalha  
✅ **Reutilização:** Cada BattleMove reutiliza a mesma instância de Move  
✅ **Extensibilidade:** Fácil adicionar novos efeitos de move  
✅ **Testabilidade:** BattleMove.execute() é independente e testável  
✅ **Acesso a Field:** Moves podem consultar weather, terrain, side conditions  

## TODOs Futuros

1. **move.py:**
   - Implementar `_execute_status_move()` com lógica completa
   - Adicionar efeitos de field setters (Stealth Rock, Spikes, etc)
   - Implementar multi-target moves corretamente

2. **turn.py:**
   - Implementar `_execute_end_of_turn_phase()` com weather/terrain damage
   - Integrar com Field para realmente trocar Pokémon em `_execute_switch_phase()`
   - Implementar transformações reais em `_execute_transformation_phase()`
   - Melhorar lógica de targeting (`action.target`)
   - Desativar abilities quando Pokémon desmaia

3. **pokemon.py:**
   - Adicionar método `activate_ability_on_entry()`
   - Adicionar método `deactivate_ability_on_exit()`

4. **battle.py:**
   - Integrar `Turn.execute_turn()` no loop principal da batalha
   - Implementar método `choose_action()` para retornar `Action` com `BattleMove`

## Tipo de Modificações

- ✅ Sem breaking changes significativas (compatibilidade mantida)
- ✅ Código compilável e sem erros de sintaxe
- ✅ Future annotations para evitar circular imports
- ✅ Type hints corretos com TYPE_CHECKING
