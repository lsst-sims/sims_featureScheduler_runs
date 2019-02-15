baseline-like simulations

4 runs, all have a three-tier decision tree with Deep Drilling Fields, blob of observations with pairs, and then greedy algorithm for when it is twilight (or twilight will soon start).

We run them with visits consisting of 2x15s exposures or 1x30s exposure (all filters). The other variation is if pairs are taken in the same filter or mixed. In the case of same, pairs are taken in g+g, r+r, i+i (u, z, y observations are unpaired). For mixed, pairs are taken as g+r, r+i, or z+i). 

| run name | OSF | N obs (millions) |
| ------- | :------: |
| baseline_1exp_pairsmix_10yrs.db  | 77% | 2.58 |
| baseline_2exp_pairsmix_10yrs.db  | 71%  | 2.38 |
| baseline_1exp_pairsame_10yrs.db  | 78% |  2.63 |
| baseline_2exp_pairsame_10yrs.db  | 72% | 2.43 |

