import numpy as np

import pyspiel

_DEFAULT_PARAMS = {
    "imp_info": False,
    "num_cards": 4,
    "num_turns": 4,
    "players": 2,
    "points_order": "random",
    "returns_type": "win_loss"
}
_GAME_TYPE = pyspiel.GameType(
    short_name="python_goofspiel",
    long_name="Python Goofspiel",
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
    provides_factored_observation_string=True,
    parameter_specification=_DEFAULT_PARAMS
)

global SHIFT_POINTS
global SHIFT_CARDS
global SHIFT_PRIZES

class GoofspielGame(pyspiel.Game):
    def __init__(self, params=_DEFAULT_PARAMS):
        self._imp_info = params["imp_info"]
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
        super().__init__(_GAME_TYPE, game_info, params or dict())

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return GoofspielState(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return GoofspielObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            self._imp_info, self._num_players, self._num_cards, self._num_turns, params)


class GoofspielState(pyspiel.State):
    def __init__(self, game):
        """Constructor; should only be called by Game.new_initial_state."""
        super().__init__(game)
        self._num_players = game._num_players
        self._num_cards = game._num_cards
        self._num_turns = game._num_turns
        self.cards = np.ones((self._num_players, self._num_cards), dtype=int)
        global SHIFT_CARDS
        SHIFT_CARDS = 2 ** np.arange(self.cards.size).reshape(self.cards.shape)
        self.bets = np.zeros((self._num_turns, self._num_players), dtype=int) - 1
        self.points = np.zeros(self._num_players, dtype=int)
        global SHIFT_POINTS
        SHIFT_POINTS = (game._num_cards ** 2) ** np.arange(self.points.size).reshape(self.points.shape)
        self.prizes = np.zeros(game._num_cards, dtype=int) - 1
        global SHIFT_PRIZES
        SHIFT_PRIZES = (game._num_cards + 1) ** np.arange(self.prizes.size).reshape(self.prizes.shape)
        self._game_over = False
        self._current_turn = 0
        self._next_player = self._num_players

    # OpenSpiel (PySpiel) API functions are below. This is the standard set that
    # should be implemented by every sequential-move game with chance.

    def current_player(self):
        """Returns id of the next player to move, or TERMINAL if game is over."""
        if self._game_over:
            return pyspiel.PlayerId.TERMINAL
        elif self._next_player == self._num_players:
            return pyspiel.PlayerId.CHANCE
        else:
            return self._next_player

    def _legal_actions(self, player):
        """Returns a list of legal actions, sorted in ascending order."""
        assert player >= 0
        return np.where(self.cards[player] == 1)[0]

    def chance_outcomes(self):
        """Returns the possible chance outcomes and their probabilities."""
        assert self.is_chance_node()
        outcomes = [i for i in range(self._num_cards) if i not in self.prizes]
        p = 1.0 / len(outcomes)
        return [(o, p) for o in outcomes]

    def _apply_action(self, action):
        """Applies the specified action to the state."""
        if self.is_chance_node():
            self.prizes[self._current_turn] = action
        else:
            # make bet
            self.cards[self._next_player, action] = 0
            self.bets[self._current_turn, self._next_player] = action
        self._next_player = self._next_player + 1 if self._next_player < self._num_players else 0
        # after all players have bet, reward the player with the highest bet
        # if highest bets tie, throw out the card
        if self._next_player == self._num_players:
            highest_bet = self.bets[self._current_turn].max()
            highest_bidder = np.where(self.bets[self._current_turn] == highest_bet)[0]
            if len(highest_bidder) == 1:
                self.points[highest_bidder[0]] += self.prizes[self._current_turn]
            self._current_turn += 1
        if self._current_turn == self._num_turns:
            self._game_over = True

    def _action_to_string(self, player, action):
        """Action -> string."""
        if player == pyspiel.PlayerId.CHANCE:
            return f"Deal:{action}"
        else:
            return f"Bet:{action}"

    def is_terminal(self):
        """Returns True if the game is over."""
        return self._game_over

    def returns(self):
        """Total reward for each player over the course of the game so far."""
        if not self._game_over:
            return [0.] * self._num_players
        else:
            highest_points = self.points.max()
            winners = np.where(self.points == highest_points)[0]
            if len(winners) == self._num_players:
                return [0.] * self._num_players
            return [1.0 / len(winners) if i in winners else -1.0 / (self._num_players - len(winners)) for i in range(self._num_players)]

    def __str__(self):
        """String for debug purposes. No particular semantics are required."""
        return str((self.prizes, self.cards, self.bets, self.points))


class GoofspielObserver:
    """Observer, conforming to the PyObserver interface (see observation.py)."""

    def __init__(self, iig_obs_type, imp_info, num_players, num_cards, num_turns, params):
        """Initializes an empty observation tensor."""
        if params:
            raise ValueError(f"Observation parameters not supported; passed {params}")

        # Determine which observation pieces we want to include.
        pieces = [("player", num_players, (num_players,))]
        if iig_obs_type.public_info and not iig_obs_type.perfect_recall:
            pieces.append(("current_prize", 1, (1,)))
            pieces.append(("remaining_prizes", num_cards, (num_cards,)))
        if iig_obs_type.public_info:
            pieces.append(("points", num_players, (num_players,)))
        if imp_info and iig_obs_type.private_info == pyspiel.PrivateInfoType.SINGLE_PLAYER:
            pieces.append(("private_cards", num_cards, (num_cards,)))
        if imp_info and iig_obs_type.public_info:
            pieces.append(("win_sequence", num_cards, (num_cards,)))
        if iig_obs_type.public_info and iig_obs_type.perfect_recall:
            pieces.append(("prizes", num_cards, (num_cards,)))
        if imp_info and iig_obs_type.perfect_recall and iig_obs_type.private_info == pyspiel.PrivateInfoType.SINGLE_PLAYER:
            pieces.append(("private_action_sequence", num_turns, (num_turns,)))
        if iig_obs_type.public_info and not imp_info:
            pieces.append(("cards", num_players * num_cards, (num_players, num_cards)))

        # Build the single flat tensor.
        total_size = sum(size for name, size, shape in pieces)
        self.tensor = np.zeros(total_size, np.float32)

        # Build the named & reshaped views of the bits of the flat tensor.
        self.dict = {}
        index = 0
        for name, size, shape in pieces:
            self.dict[name] = self.tensor[index:index + size].reshape(shape)
            index += size

    def set_from(self, state, player):
        """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
        self.tensor.fill(0)
        if "player" in self.dict:
            self.dict["player"][player] = 1
        if "points" in self.dict:
            self.dict["points"] = state.points
        if "prizes" in self.dict:
            self.dict["prizes"] = state.prizes
        if "current_prize" in self.dict:
            self.dict["current_prize"] = state.prizes[state._current_turn]
        if "remaining_prizes" in self.dict:
            remain = np.ones(state._num_cards)
            remain[state.prizes[:state._current_turn + 1]] = 0
            self.dict["remaining_prizes"] = remain
        if "win_sequence" in self.dict:
            self.dict["win_sequence"] = np.argmax(state.bets, axis=1)
        if "private_action_sequence" in self.dict:
            self.dict["private_action_sequence"] = state.bets[:, player]
        if "cards" in self.dict:
            self.dict["cards"] = state.cards
        if "private_cards" in self.dict:
            self.dict["private_cards"] = state.cards[player]

    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        return f"p{player} points: {(state.points * SHIFT_POINTS).sum()} prizes: {((state.prizes + 1) * SHIFT_PRIZES).sum()} cards: {(state.cards * SHIFT_CARDS).sum()}"



# Register the game with the OpenSpiel library

pyspiel.register_game(_GAME_TYPE, GoofspielGame)
