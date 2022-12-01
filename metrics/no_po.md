# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.12147021293640137
 * PCFR+ (4, 3): 2.5333213806152344
 * PCFR+ (4, 4): 7.399199485778809
 * PCFR+ (5, 3): 28.44742250442505

## First Iteration Time

 * PCFR+ (3, 3): 0.10628652572631836
 * PCFR+ (4, 3): 2.429758071899414
 * PCFR+ (4, 4): 6.086654901504517
 * PCFR+ (5, 3): 28.945765733718872

## Average Iteration Times

 * PCFR+ (3, 3): 0.03465535163879394
 * PCFR+ (4, 3): 0.6167351627349853
 * PCFR+ (4, 4): 2.385424976348877
 * PCFR+ (5, 3): 5.616662273406982

# Memory

## Peak Resident Memory Usage

 * (3, 3): 52004, 52632, 54328, 53380, 55804
 * (4, 3): 101312, 98556, 94620, 103928, 95048
 * (4, 4): 130176, 142984, 127220, 137220, 140732
 * (5, 3): 505912, 504604, 510796, 521912, 504576

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

 * (3, 3): 318
 * (4, 3): 2360
 * (4, 4): 6200
 * (5, 3): 9890
 * (5, 4): 63746

# Solution Quality

## Exploitability in Original Game


# Notes

No bet order information - repr is:
```python
            f"p{self.current_player()}"
            f"points: {(self.points * SHIFT_POINTS).sum()}"
            f"prizes: {((self.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(self.cards * SHIFT_CARDS).sum()}"
            f"bets: {((self.bets + 1) * SHIFT_BETS)[self._current_turn].sum() if self._current_turn < self._num_turns else -1}"
```

No po - string_from is:
```python
                f"p{state.current_player()}"
                f"points: {(state.points * SHIFT_POINTS).sum()}"
                f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
                f"cards: {(state.cards * SHIFT_CARDS)[player].sum()}"
```