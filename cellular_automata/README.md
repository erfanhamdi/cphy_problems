## Cellular Automata Problem

|        Initial State   | Final State |  Avalanche activity in most recent timesteps  | Avalanche duration distribution |
|:----------:|:-------------:|:-------------: |:-------------:|
|![](/cellular_automata/figs/frame0000.png) |![](/cellular_automata/figs/frame0498.png)| ![](/cellular_automata/figs/Figure_3.png) | ![](/cellular_automata/figs/avalanche_duration_distribution.png) |

## Let it Topple!
Here is a gif made from each step of avalanche.
|        Avalanche! |
|:----------: |
![](/cellular_automata/figs/sandpile_copper.gif)

## Runtime Comparison
I compared my version of implementation with the recursive solution that was presented and here are the results:
|       Method | Runtime | 
|:----------: | :----------: |
| Vectorized | 31.854 |
| Recursive | 9.28 |