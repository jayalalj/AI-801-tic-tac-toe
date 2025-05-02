AI 801 (Foundations of Artificial Intelligence)
[Spring 2025]


Python version 3.11

Python Packges neded
- collections
- math
- random
- time
- pandas


To Run already configured simulations.
 Use regular Notebook run functionality.

To Configure and run two Agents.
use play game interface:
```python
play_game(game, strategies: dict, verbose=False):
```

- Parmeter 1(game) : game board with desired configuration
- parameter 2 (strategies) : dictionary containing two agents.
- Parameter 3 (verbose) : To display the game board between moves.
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
game: You define the game (in this case, a TwoMoveTicTacToe with specific dimensions and conditions).

strategies: You specify the agents for the two players (X and O). For instance, you could have X use the minimax_search_alpha_beta_prune_hct strategy and O use a random_player.

verbose: If set to True, it will display the game board between each move.


###strategies
   - minmax with Basic Heuristic
   - minmax with Monte Carlo Heuristic
   - greedy
     

see code examples to configure different parameters for different strategies in the notebook

