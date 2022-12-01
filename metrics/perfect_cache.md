# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.13155674934387207
 * PCFR+ (4, 3): 3.007814645767212
 * PCFR+ (4, 4): 9.140382766723633
 * PCFR+ (5, 3): 31.730130195617676

## First Iteration Time

 * PCFR+ (3, 3): 0.11388444900512695
 * PCFR+ (4, 3): 2.996018409729004
 * PCFR+ (4, 4): 7.855292558670044
 * PCFR+ (5, 3): 33.411993980407715

## Average Iteration Times

 * PCFR+ (3, 3): 0.03993355751037598
 * PCFR+ (4, 3): 0.7320960903167725
 * PCFR+ (4, 4): 2.401888580322266
 * PCFR+ (5, 3): 7.053470287322998

# Memory

## Peak Resident Memory Usage

 * (3, 3): 63296, 59876, 52236, 50052, 61136
 * (4, 3): 121184, 128292, 125060, 113576, 124452
 * (4, 4): 285316, 291368, 292144, 297832, 287992
 * (5, 3): 782904, 781532, 768264, 769300, 778712

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

 * (3, 3): 546
 * (4, 3): 7304
 * (4, 4): 34952
 * (5, 3): 49010
 * (5, 4): 913010

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

Perfect information - string_from is:
```python
            f"p{state.current_player()}"
            f"points: {(state.points * SHIFT_POINTS).sum()}"
            f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(state.cards * SHIFT_CARDS).sum()}"
            f"bets: {((state.bets + 1) * SHIFT_BETS)[:state._current_turn].sum()}"
```