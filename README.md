AI 801 (Foundations of Artificial Intelligence)
[Spring 2025]


Python version 3.11

Python Packges neded
collections
math
random
time
pandas


To Run already configured simulations.
 Use regular Notebook run functionality.

To Configure and run two Agents.
use play game interface:
```python
play_game(game, strategies: dict, verbose=False):
```

- Parmeter 1 : game board with desired configuration
- parameter 2: dictionary containing two agents.
- Parameter 3: To display the game board between moves.
ex:
```python
play_game(
           TwoMoveTicTacToe(height=5, width=5, k=5),
           dict(
               
               X=lambda game, state: minimax_search_alpha_beta_prune_hct(game, state, 2, lambda g, s, p: heuristic_evaluation_monte_carlo(g, s, p, simulations=5))[1],
               O=random_player,
           ),
           verbose=False
       )
```
