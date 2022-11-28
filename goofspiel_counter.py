import pyspiel
from absl import app, flags
from open_spiel.python.algorithms import exploitability

from predictive_cfr import PCFRSolver

from goofspiel import *

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 10, "Number of iterations")
flags.DEFINE_string(
    "game",
    "python_goofspiel(num_cards=4,num_turns=4)",
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 10,
                     "How often to print the exploitability")

def state_count(game):
    root = game.new_initial_state()
    def state_count_helper(state):
        return 1 + sum(state_count_helper(state.child(a)) for a in state.legal_actions(state.current_player()))

    return state_count_helper(root)

def main(_):
    game = pyspiel.load_game(FLAGS.game)
    print(f"Game tree size: {state_count(game)}")
    state_counter = PCFRSolver(game)
    print(f"Infoset policy shape: {state_counter._current_policy.action_probability_array.shape}")


if __name__ == "__main__":
    app.run(main)
