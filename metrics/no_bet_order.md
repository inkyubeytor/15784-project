# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.13869881629943848
 * DCFR  (3, 3): 0.1427750587463379
 * PCFR+ (4, 3): 2.960529327392578
 * DCFR  (4, 3): 3.0067269802093506
 * PCFR+ (4, 4): 8.894626379013062
 * DCFR  (4, 4): 8.478917360305786
 * PCFR+ (5, 3): 32.11988854408264
 * DCFR  (5, 3): 33.105321168899536

## First Iteration Time

 * PCFR+ (3, 3): 0.11390161514282227
 * DCFR  (3, 3): 0.11876630783081055
 * PCFR+ (4, 3): 2.746701717376709
 * DCFR  (4, 3): 2.754946231842041
 * PCFR+ (4, 4): 6.843999624252319
 * DCFR  (4, 4): 6.6827638149261475
 * PCFR+ (5, 3): 31.021987915039062
 * DCFR  (5, 3): 30.709473133087158

## Average Iteration Times

 * PCFR+ (3, 3): 0.039648399353027344
 * DCFR  (3, 3): 0.04375154495239258
 * PCFR+ (4, 3): 0.7290927696228028
 * DCFR  (4, 3): 0.7640924263000488
 * PCFR+ (4, 4): 2.375682373046875
 * DCFR  (4, 4): 2.4495444107055664
 * PCFR+ (5, 3): 7.064613456726074
 * DCFR  (5, 3): 7.2502094173431395

# Memory

## Peak Resident Memory Usage

 * (3, 3): 47808, 49720, 55792, 55824, 56216
 * (4, 3): 108200, 112856, 105864, 104172, 106424
 * (4, 4): 163224, 175244, 177088, 172620, 176880
 * (5, 3): 613188, 610700, 623220, 613304, 611104

# Game Size

## Number of States

 * (3, 3): 832
 * (4, 3): 15901
 * (4, 4): 27133
 * (5, 3): 158688
 * (5, 4): 740832

## Number of Player States

 * (3, 3): 546
 * (4, 3): 9284
 * (4, 4): 19556
 * (5, 3): 76930
 * (5, 4): 529522

## Number of Information Sets

 * (3, 3): 486
 * (4, 3): 6056
 * (4, 4): 16328
 * (5, 3): 38210
 * (5, 4): 339938

# Solution Quality

## Exploitability in Original Game


# Notes

Bet order doesn't matter - repr is:
```python
            f"p{self.current_player()}"
            f"points: {(self.points * SHIFT_POINTS).sum()}"
            f"prizes: {((self.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(self.cards * SHIFT_CARDS).sum()}"
            f"bets: {((self.bets + 1) * SHIFT_BETS)[self._current_turn].sum() if self._current_turn < self._num_turns else -1}"
```

Bet order doesn't matter - string_from is:
```python
            f"p{state.current_player()}"
            f"points: {(state.points * SHIFT_POINTS).sum()}"
            f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(state.cards * SHIFT_CARDS).sum()}"
```