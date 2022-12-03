import pyspiel
from absl import app, flags
import sys
import pickle

from predictive_cfr import PCFRSolver

from goofspiel_perfect import *
from goofspiel_noorder import *
from goofspiel_privateonly import *
from goofspiel_nopo import *


def generate_mapping(game):
    """Counts the number of non-terminal non-chance states."""
    root = game.new_initial_state()
    mapping = {}
    def generate_mapping_helper(state):
        count_me = int(state.current_player() != pyspiel.PlayerId.CHANCE and state.current_player() != pyspiel.PlayerId.TERMINAL)
        if count_me > 0:
            mapping[get_perfect_string(state)] = state.information_state_string()
        return count_me + sum(generate_mapping_helper(state.child(a)) for a in state.legal_actions(state.current_player()))
    generate_mapping_helper(root)
    return mapping


def get_perfect_string(state):
    return (
        f"p{state.current_player()}"
        f"points: {(state.points * state.shift['POINTS']).sum()}"
        f"prizes: {((state.prizes + 1) * state.shift['PRIZES']).sum()}"
        f"cards: {(state.cards * state.shift['CARDS']).sum()}"
        f"bets: {((state.bets + 1) * state.shift['BETS'])[:state._current_turn].sum()}"
    )


def main(_):
    for name_str in ["noorder", "privateonly", "nopo"]:
        for num_cards, num_turns in [(3, 3), (4, 3), (4, 4), (5, 3)]:
            game_str = f"python_goofspiel_{name_str}(num_cards={num_cards},num_turns={num_turns})"
            game = pyspiel.load_game(game_str)
            mapping = generate_mapping(game)
            filename = f"mappings/python_goofspiel_perfect_to_{name_str}_infoset_mapping(num_cards={num_cards},num_turns={num_turns}).pkl"
            with open(filename, "wb") as f:
                pickle.dump(mapping, f)


if __name__ == "__main__":
    app.run(main)
