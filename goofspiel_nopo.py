import numpy as np

import pyspiel

from goofspiel_base import *
from goofspiel_state import GoofspielStateNoOrder

GAME_TYPE = get_game_type("python_goofspiel_nopo", "Python Goofspiel No Order Private Only")


class GoofspielNOPOGame(GoofspielGameBase):
    def __init__(self, params=DEFAULT_PARAMS):
        super().__init__(GAME_TYPE, params)

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return GoofspielStateNoOrder(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return GoofspielNOPOObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            self._num_players, self._num_cards, self._num_turns, self.shift, params)


class GoofspielNOPOObserver(GoofspielObserverBase):
    """Observer, conforming to the PyObserver interface (see observation.py)."""
    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        return (
            f"p{state.current_player()}"
            f"points: {(state.points * state.shift['POINTS']).sum()}"
            f"prizes: {((state.prizes + 1) * state.shift['PRIZES']).sum()}"
            f"cards: {(state.cards * state.shift['CARDS'])[player].sum()}"
        )


pyspiel.register_game(GAME_TYPE, GoofspielNOPOGame)
