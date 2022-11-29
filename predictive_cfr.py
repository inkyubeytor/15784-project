import numpy as np

from open_spiel.python.algorithms import cfr


_InfoStateNode = cfr._InfoStateNode  # pylint: disable=protected-access


class _PCFRSolver(cfr._CFRSolver):  # pylint: disable=protected-access
    """
    Implements Predictive CFR+ from https://arxiv.org/pdf/2007.14358.pdf.
    Largely derived from the DCFR implementation.
    """

    def __init__(self, game, alternating_updates, linear_averaging,
                 regret_matching_plus, gamma):
        """Copied initialization from DCFR. """
        super(_PCFRSolver, self).__init__(game, alternating_updates,
                                          linear_averaging,
                                          regret_matching_plus)
        self.gamma = gamma
        self.optimism = {}
        self.cache = {}

        # We build a list of the nodes for all players, which will be updated
        # within `evaluate_and_update_policy`.
        self._player_nodes = [[] for _ in range(self._num_players)]
        for info_state in self._info_state_nodes.values():
            self._player_nodes[info_state.player].append(info_state)

    def _initialize_info_state_nodes(self, state):
        """Initializes info_state_nodes. This is also copied from DCFR.
        We override the parent function, to add the current player information
        at the given node. This is used because we want to do updates for all nodes
        for a specific player.
        Args:
          state: The current state in the tree walk. This should be the root node
            when we call this function from a CFR solver.
        """
        if state.is_terminal():
            return

        if state.is_chance_node():
            for action, unused_action_prob in state.chance_outcomes():
                self._initialize_info_state_nodes(state.child(action))
            return

        current_player = state.current_player()
        info_state = state.information_state_string(current_player)

        info_state_node = self._info_state_nodes.get(info_state)
        if info_state_node is None:
            legal_actions = state.legal_actions(current_player)
            info_state_node = _InfoStateNode(
                legal_actions=legal_actions,
                index_in_tabular_policy=self._current_policy.state_lookup[
                    info_state])
            info_state_node.player = current_player
            self._info_state_nodes[info_state] = info_state_node

        for action in info_state_node.legal_actions:
            self._initialize_info_state_nodes(state.child(action))


    def _compute_counterfactual_regret_for_player(self, state, policies,
                                                  reach_probabilities, player):
        """Increments the cumulative regrets and policy for `player`. This is
          copied from the DCFR function, as we still want to have linear or
          quadratic averaging available. However, we also store 'optimism' values
          for optimistic updates.

        Args:
          state: The initial game state to analyze from.
          policies: Unused. To be compatible with the `_CFRSolver` signature.
          reach_probabilities: The probability for each player of reaching `state`
            as a numpy array [prob for player 0, for player 1,..., for chance].
            `player_reach_probabilities[player]` will work in all cases.
          player: The 0-indexed player to update the values for. If `None`, the
            update for all players will be performed.
        Returns:
          The utility of `state` for all players, assuming all players follow the
          current policy defined by `self.Policy`.
        """
        if state.is_terminal():
            return np.asarray(state.returns())

        if state.is_chance_node():
            state_value = 0.0
            for action, action_prob in state.chance_outcomes():
                assert action_prob > 0
                k = (str(state), action)
                if k in self.cache:
                    new_state = self.cache[k]
                else:
                    new_state = state.child(action)
                    self.cache[k] = new_state
                old = reach_probabilities[-1]
                reach_probabilities[-1] *= action_prob
                state_value += action_prob * self._compute_counterfactual_regret_for_player(
                    new_state, policies, reach_probabilities, player)
                reach_probabilities[-1] = old
            return state_value

        current_player = state.current_player()
        info_state = state.information_state_string(current_player)

        # No need to continue on this history branch as no update will be performed
        # for any player.
        # The value we return here is not used in practice. If the conditional
        # statement is True, then the last taken action has probability 0 of
        # occurring, so the returned value is not impacting the parent node value.
        if all(reach_probabilities[:-1] == 0):
            return np.zeros(self._num_players)

        state_value = np.zeros(self._num_players)

        # The utilities of the children states are computed recursively. As the
        # regrets are added to the information state regrets for each state in that
        # information state, the recursive call can only be made once per child
        # state. Therefore, the utilities are cached.
        children_utilities = {}

        info_state_node = self._info_state_nodes[info_state]
        if policies is None:
            info_state_policy = self._get_infostate_policy(info_state)
        else:
            info_state_policy = policies[current_player](info_state)
        for action in state.legal_actions():
            action_prob = info_state_policy.get(action, 0.)
            k = (str(state), action)
            if k in self.cache:
                new_state = self.cache[k]
            else:
                new_state = state.child(action)
                self.cache[k] = new_state
            old = reach_probabilities[current_player]
            reach_probabilities[current_player] *= action_prob
            child_utility = self._compute_counterfactual_regret_for_player(
                new_state,
                policies=policies,
                reach_probabilities=reach_probabilities,
                player=player)
            reach_probabilities[current_player] = old

            state_value += action_prob * child_utility
            children_utilities[action] = child_utility

        # If we are performing alternating updates, and the current player is not
        # the current_player, we skip the cumulative values update.
        # If we are performing simultaneous updates, we do update the cumulative
        # values.
        simulatenous_updates = player is None
        if not simulatenous_updates and current_player != player:
            return state_value

        reach_prob = reach_probabilities[current_player]
        counterfactual_reach_prob = (
                np.prod(reach_probabilities[:current_player]) *
                np.prod(reach_probabilities[current_player + 1:]))
        state_value_for_player = state_value[current_player]

        for action, action_prob in info_state_policy.items():
            cfr_regret = counterfactual_reach_prob * (
                    children_utilities[action][
                        current_player] - state_value_for_player)
            self.optimism[(info_state_node.index_in_tabular_policy, action)] = cfr_regret

            info_state_node = self._info_state_nodes[info_state]
            info_state_node.cumulative_regret[action] += cfr_regret
            scale = self._iteration ** self.gamma
            if self._linear_averaging:
                info_state_node.cumulative_policy[action] += (
                        reach_prob * action_prob * scale)
            else:
                info_state_node.cumulative_policy[
                    action] += reach_prob * action_prob

        return state_value

    def evaluate_and_update_policy(self):
        """Performs a single step of policy evaluation and policy improvement.
          We add the optimism values to cumulative regret right before the
          update, then remove them right after the update.
        """
        self._iteration += 1
        if self._alternating_updates:
            for current_player in range(self._game.num_players()):
                self.optimism = {}
                self._compute_counterfactual_regret_for_player(
                    self._root_node,
                    policies=None,
                    reach_probabilities=np.ones(self._game.num_players() + 1),
                    player=current_player)
                for info_state in self._player_nodes[current_player]:
                    for action in info_state.cumulative_regret.keys():
                        info_state.cumulative_regret[action] += self.optimism.get((info_state.index_in_tabular_policy, action), 0)
                cfr._update_current_policy(self._current_policy,
                                           self._info_state_nodes)  # pylint: disable=protected-access
                for info_state in self._player_nodes[current_player]:
                    for action in info_state.cumulative_regret.keys():
                        info_state.cumulative_regret[action] -= self.optimism.get((info_state.index_in_tabular_policy, action), 0)


class PCFRSolver(_PCFRSolver):

    def __init__(self, game, gamma=2):
        super(PCFRSolver, self).__init__(
            game,
            regret_matching_plus=True,
            alternating_updates=True,
            linear_averaging=True,
            gamma=gamma)
