import numpy as np

import pyspiel

from goofspiel_base import *


# should modify names in GAME_TYPE

class GoofspielPerfectGame(GoofspielGameBase):
    def __init__(self, params=DEFAULT_PARAMS):
        super().__init__(params)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return GoofspielPerfectObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            self._num_players, self._num_cards, self._num_turns, params)


class GoofspielPerfectObserver(GoofspielObserverBase):
    """Observer, conforming to the PyObserver interface (see observation.py)."""
    #
    # def __init__(self, iig_obs_type, num_players, num_cards, num_turns, params):
    #     """Initializes an empty observation tensor."""
    #     super().__init__(iig_obs_type, num_players, num_cards, num_turns, params)

    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        return (
            f"p{state.current_player()}"
            f"points: {(state.points * SHIFT_POINTS).sum()}"
            f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
            f"cards: {(state.cards * SHIFT_CARDS).sum()}"
            f"bets: {((state.bets + 1) * SHIFT_BETS)[:state._current_turn].sum()}"
        )


pyspiel.register_game(GAME_TYPE, GoofspielPerfectGame)
