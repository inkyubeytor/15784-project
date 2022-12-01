# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.1223611831665039
 * PCFR+ (4, 3): 2.5801351070404053
 * PCFR+ (4, 4): 7.193093299865723
 * PCFR+ (5, 3): 28.59132981300354

## First Iteration Time

 * PCFR+ (3, 3): 0.10910248756408691
 * PCFR+ (4, 3): 2.6499276161193848
 * PCFR+ (4, 4): 7.193093299865723
 * PCFR+ (5, 3): 31.589855432510376

## Average Iteration Times

 * PCFR+ (3, 3): 0.03354649543762207
 * PCFR+ (4, 3): 0.659803056716919
 * PCFR+ (4, 4): 2.4871413612365725
 * PCFR+ (5, 3): 5.721386251449585

# Memory

## Peak Resident Memory Usage

 * (3, 3): 55680, 60680, 48432, 49488, 51404
 * (4, 3): 104536, 96848, 103996, 103276, 97724
 * (4, 4): 213580, 221724, 213444, 220852, 222236
 * (5, 3): 641700, 647732, 655108, 654136, 644756

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