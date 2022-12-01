# Time

## Iterations

## Setup Time

 * PCFR+ (3, 3): 0.13670706748962402
 * PCFR+ (4, 3): 2.8438713550567627
 * PCFR+ (4, 4): 8.908080816268921
 * PCFR+ (5, 3): 30.790974617004395

## First Iteration Time

 * PCFR+ (3, 3): 0.1633763313293457
 * PCFR+ (4, 3): 3.835965633392334
 * PCFR+ (4, 4): 10.351541996002197
 * PCFR+ (5, 3): 48.37255835533142

## Average Iteration Times

 * PCFR+ (3, 3): 0.09305655479431152
 * PCFR+ (4, 3): 1.555087080001831
 * PCFR+ (4, 4): 4.917275657653809
 * PCFR+ (5, 3): 16.965002403259277

# Memory

## Peak Resident Memory Usage (KB)

 * (3, 3): 48096, 45636, 55784, 50844, 49720
 * (4, 3): 74096, 70204, 87604, 81716, 89004
 * (4, 4): 170496, 182704, 170128, 172168, 171220
 * (5, 3): 280200, 284124, 279236, 292456, 286596

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