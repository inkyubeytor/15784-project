import numpy as np

import pyspiel

from goofspiel_base import *
from goofspiel_state import GoofspielStateNoOrder

GAME_TYPE = get_game_type("python_goofspiel_nopo_asymmetric", "Python Goofspiel No Order Private Only Asymmetric")


class GoofspielNOPOAsymmetricGame(GoofspielGameBase):
    def __init__(self, params=DEFAULT_PARAMS):
        self._abstract_player = params["abstract_player"]
        super().__init__(GAME_TYPE, params)

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return GoofspielStateNoOrder(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return GoofspielNOPOAsymmetricObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            self._abstract_player, self._num_players, self._num_cards, self._num_turns, self.shift, params)


class GoofspielNOPOAsymmetricObserver(GoofspielObserverBase):
    """Observer, conforming to the PyObserver interface (see observation.py)."""
    def __init__(self, iig_obs_type, abstract_player, num_players, num_cards, num_turns, shift, obs_params):
        self.abstract_player = abstract_player
        super().__init__(iig_obs_type, num_players, num_cards, num_turns, shift, obs_params)

    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        if player == self.abstract_player:
            return (
                f"p{state.current_player()}"
                f"points: {(state.points * state.shift['POINTS']).sum()}"
                f"prizes: {((state.prizes + 1) * state.shift['PRIZES']).sum()}"
                f"cards: {(state.cards * state.shift['CARDS'])[player].sum()}"
            )
        else:
            return (
                f"p{state.current_player()}"
                f"points: {(state.points * state.shift['POINTS']).sum()}"
                f"prizes: {((state.prizes + 1) * state.shift['PRIZES']).sum()}"
                f"cards: {(state.cards * state.shift['CARDS']).sum()}"
                f"bets: {((state.bets + 1) * state.shift['BETS'])[:state._current_turn].sum()}"
            )


pyspiel.register_game(GAME_TYPE, GoofspielNOPOAsymmetricGame)
