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