import numpy as np

import pyspiel

from goofspiel_base import *
from goofspiel_state import GoofspielStateNoOrder

GAME_TYPE = get_game_type("python_goofspiel_noorder", "Python Goofspiel No Order")


class GoofspielNoOrderGame(GoofspielGameBase):
    def __init__(self, params=DEFAULT_PARAMS):
        super().__init__(GAME_TYPE, params)

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return GoofspielStateNoOrder(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return GoofspielNoOrderObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            self._num_players, self._num_cards, self._num_turns, self.shift, params)


class GoofspielNoOrderObserver(GoofspielObserverBase):
    """Observer, conforming to the PyObserver interface (see observation.py)."""
    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        return (
            f"p{state.current_player()}"
            f"points: {(state.points * self.shift['POINTS']).sum()}"
            f"prizes: {((state.prizes + 1) * self.shift['PRIZES']).sum()}"
            f"cards: {(state.cards * self.shift['CARDS']).sum()}"
        )


pyspiel.register_game(GAME_TYPE, GoofspielNoOrderGame)
