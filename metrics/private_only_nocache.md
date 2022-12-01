# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.12154030799865723
 * PCFR+ (4, 3): 2.636789560317993
 * PCFR+ (4, 4): 8.025944709777832
 * PCFR+ (5, 3): 28.12081241607666

## First Iteration Time

 * PCFR+ (3, 3): 0.1442093849182129
 * PCFR+ (4, 3): 3.66465163230896
 * PCFR+ (4, 4): 9.649292469024658
 * PCFR+ (5, 3): 42.60993218421936

## Average Iteration Times

 * PCFR+ (3, 3): 0.07603873252868652
 * PCFR+ (4, 3): 1.4787302017211914
 * PCFR+ (4, 4): 5.1330500507354735
 * PCFR+ (5, 3): 13.478730001449584

# Memory

## Peak Resident Memory Usage

 * (3, 3): 49008, 49984, 49904, 48632, 56308
 * (4, 3): 66240, 68676, 66076, 70028, 76912
 * (4, 4): 128748, 124680, 126324, 119556, 126180
 * (5, 3): 212456, 207024, 216464, 223228, 226736

# Game Size

## Number of States

 * (3, 3): 1066
 * (4, 3): 26773
 * (4, 4): 68245
 * (5, 3): 322656
 * (5, 4): 3346656

## Number of Player States

 * (3, 3): 606 
 * (4, 3): 11156
 * (4, 4): 38804
 * (5, 3): 98530
 * (5, 4): 1394530

## Number of Information Sets

 * (3, 3): 426
 * (4, 3): 3608
 * (4, 4): 17144
 * (5, 3): 16130
 * (5, 4): 231266

# Solution Quality

## Exploitability in Original Game


# Notes

Perfect information - repr is:
```python
            f"p{self.current_player()}"
            f"points: {(self.points * SHIFT_POINTS).sum()}"
            f"prizes: {((self.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(self.cards * SHIFT_CARDS).sum()}"
            f"bets: {((self.bets + 1) * SHIFT_BETS).sum()}"
```

Private only - string_from is:
```python
                f"p{state.current_player()}"
                f"points: {(state.points * SHIFT_POINTS).sum()}"
                f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
                f"bets: {((state.bets + 1) * SHIFT_BETS)[:state._current_turn, player].sum()}"
```