import numpy as np

global SHIFT
SHIFT = {}


def set_shift(num_players, num_cards, num_turns):
    global SHIFT
    SHIFT = {
        "CARDS": 2 ** np.arange(num_players * num_cards).reshape((num_players, num_cards)),
        "BETS": (num_cards + 1) ** np.arange(num_turns * num_players).reshape(
            (num_turns, num_players)),
        "POINTS": (num_cards ** 2) ** np.arange(num_players),
        "PRIZES": (num_cards + 1) ** np.arange(num_cards)
    }
