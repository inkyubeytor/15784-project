import numpy as np

import pyspiel

DEFAULT_PARAMS = {
    "num_cards": 4,
    "num_turns": 4,
    "abstract_player": 0,
    "players": 2,
    "points_order": "random",
    "returns_type": "win_loss"
}


def get_game_type(short_name="python_goofspiel", long_name="Python Goofspiel"):
    return pyspiel.GameType(
        short_name=short_name,
        long_name=long_name,
        dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
        chance_mode=pyspiel.GameType.ChanceMode.EXPLICIT_STOCHASTIC,
        information=pyspiel.GameType.Information.IMPERFECT_INFORMATION,
        utility=pyspiel.GameType.Utility.ZERO_SUM,
        reward_model=pyspiel.GameType.RewardModel.TERMINAL,
        max_num_players=10,
        min_num_players=2,
        provides_information_state_string=True,
        provides_information_state_tensor=True,
        provides_observation_string=True,
        provides_observation_tensor=True,
        # provides_factored_observation_string=True,
        parameter_specification=DEFAULT_PARAMS
    )


class GoofspielGameBase(pyspiel.Game):
    def __init__(self, game_type, params=DEFAULT_PARAMS):
        self._num_players = params["players"]
        self._num_cards = params["num_cards"]
        self._num_turns = params["num_turns"]

        game_info = pyspiel.GameInfo(
            num_distinct_actions=params["num_cards"],
            max_chance_outcomes=params["num_cards"] if params["points_order"] == "random" else 0,
            num_players=params["players"],
            min_utility=-1.0,
            max_utility=1.0,
            utility_sum=0.0,
            max_game_length=params["num_turns"] * params["players"]
        )

        super().__init__(game_type, game_info, params or dict())

        self.shift = {
            "CARDS": 2 ** np.arange(self._num_players * self._num_cards).reshape((self._num_players, self._num_cards)),
            "BETS": (self._num_cards + 1) ** np.arange(self._num_turns * self._num_players).reshape((self._num_turns, self._num_players)),
            "POINTS": (self._num_cards ** 2) ** np.arange(self._num_players),
            "PRIZES": (self._num_cards + 1) ** np.arange(self._num_cards)
        }

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        raise NotImplementedError
        # return GoofspielState(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        raise NotImplementedError
        # return GoofspielObserver(
        #     iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
        #     self._knowledge_type, self._num_players, self._num_cards, self._num_turns, params)


class GoofspielObserverBase:
    """Observer, conforming to the PyObserver interface (see observation.py)."""

    def __init__(self, iig_obs_type, num_players, num_cards, num_turns, shift, obs_params):
        """Initializes an empty observation tensor."""
        self.tensor = np.zeros(1)
        self.dict = {}

    def set_from(self, state, player):
        """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
        return

    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        raise NotImplementedError
        # if self._knowledge_type == "perfect":  # perfect recall, perfect info
        #     return (
        #         f"p{state.current_player()}"
        #         f"points: {(state.points * SHIFT_POINTS).sum()}"
        #         f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
        #         f"cards: {(state.cards * SHIFT_CARDS).sum()}"
        #         f"bets: {((state.bets + 1) * SHIFT_BETS)[:state._current_turn].sum()}"
        #     )
        # elif self._knowledge_type == "no_order":  # order of past bets not recalled, perfect info
        #     return (
        #         f"p{state.current_player()}"
        #         f"points: {(state.points * SHIFT_POINTS).sum()}"
        #         f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
        #         f"cards: {(state.cards * SHIFT_CARDS).sum()}"
        #     )
        # elif self._knowledge_type == "private_only":  # perfect recall, cannot see other players' bets (but winners known)
        #     return (
        #         f"p{state.current_player()}"
        #         f"points: {(state.points * SHIFT_POINTS).sum()}"
        #         f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
        #         f"bets: {((state.bets + 1) * SHIFT_BETS)[:state._current_turn, player].sum()}"
        #     )
        # elif self._knowledge_type == "no_po":  # order of past bets not recalled, cannot see other players' bets (but winners known)
        #     return (
        #         f"p{state.current_player()}"
        #         f"points: {(state.points * SHIFT_POINTS).sum()}"
        #         f"prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()}"
        #         f"cards: {(state.cards * SHIFT_CARDS)[player].sum()}"
        #     )
        # else:
        #     raise NotImplementedError

