# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 
 * PCFR+ (4, 3): 
 * PCFR+ (4, 4): 
 * PCFR+ (5, 3): 

## First Iteration Time

 * PCFR+ (3, 3): 
 * PCFR+ (4, 3): 
 * PCFR+ (4, 4): 
 * PCFR+ (5, 3): 

## Average Iteration Times

 * PCFR+ (3, 3): 
 * PCFR+ (4, 3): 
 * PCFR+ (4, 4): 
 * PCFR+ (5, 3): 

# Memory

## Peak Resident Memory Usage

 * (3, 3): 
 * (4, 3): 
 * (4, 4): 
 * (5, 3): 

# Game Size

## Number of States

 * (3, 3): 
 * (4, 3): 
 * (4, 4): 
 * (5, 3): 
 * (5, 4): 

## Number of Player States

 * (3, 3):  
 * (4, 3): 
 * (4, 4): 
 * (5, 3): 
 * (5, 4): 

## Number of Information Sets

 * (3, 3): 
 * (4, 3): 
 * (4, 4): 
 * (5, 3): 
 * (5, 4): 

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