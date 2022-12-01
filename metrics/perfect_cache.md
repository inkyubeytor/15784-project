# Time

## Wall clock time 

## Iterations

## Setup Time

## First Iteration Time

## Average Iteration Times

# Memory

## Peak Resident Memory Usage

 * (3, 3): 71044, 62168, 60148, 69348, 74612
 * (4, 3): 264252, 261396, 263232, 263548, 269732
 * (4, 4): 735336, 731216, 737180, 736712, 733088

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