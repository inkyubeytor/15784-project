# Time

## Wall clock time 

## Iterations

## Setup Time

## First Iteration Time

## Average Iteration Times

# Memory

## Peak Resident Memory Usage

 * (3, 3): 57452, 57232, 60704, 72672, 60556
 * (4, 3): 250452, 248844, 262972, 248008, 255156
 * (4, 4): 593468, 598832, 594540, 595596, 596872

# Game Size

## Number of States

 * (3, 3): 832
 * (4, 3): 15901
 * (4, 4): 27133
 * (5, 4): 740832

## Number of Player States

 * (3, 3): 546
 * (4, 3): 9284
 * (4, 4): 19556
 * (5, 4): 529522

## Number of Information Sets

 * (3, 3): 486
 * (4, 3): 6056
 * (4, 4): 16328
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