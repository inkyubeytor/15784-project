import pyspiel
from absl import app, flags
import sys

from predictive_cfr import PCFRSolver

from goofspiel import *

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 10, "Number of iterations")
flags.DEFINE_string(
    "game",
    "python_goofspiel(num_cards=4,num_turns=3)",
    # "turn_based_simultaneous_game(game=goofspiel(imp_info=False,num_cards=3,players=2,points_order=random))",
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 10,
                     "How often to print the exploitability")

def state_count(game):
    root = game.new_initial_state()
    def state_count_helper(state):
        count_me = int(state.current_player() != pyspiel.PlayerId.CHANCE and state.current_player() != pyspiel.PlayerId.TERMINAL)
        return count_me + sum(state_count_helper(state.child(a)) for a in state.legal_actions(state.current_player()))

    return state_count_helper(root)


def state_size(game):
    size = 0
    r = game.new_initial_state()
    size += sys.getsizeof(r)
    for v in vars(r).values():
        size += sys.getsizeof(v)
    return size


def str_collision(game):
    strs = set()
    r = game.new_initial_state()
    queue = [r]
    while queue:
        s = queue.pop()
        if s.current_player() != pyspiel.PlayerId.TERMINAL:
            info = str(s)
            if info in strs:
                print(info)
            else:
                if s.current_player() != pyspiel.PlayerId.CHANCE:
                    strs.add(info)
            for a in s.legal_actions(s.current_player()):
                queue.append(s.child(a))
    print(f"{len(strs)=}")


def main(_):
    game = pyspiel.load_game(FLAGS.game)
    print(f"Game tree size: {state_count(game)}")
    state_counter = PCFRSolver(game)
    str_collision(game)
    print(f"A state is {state_size(game)} bytes")
    print(f"Infoset policy shape: {state_counter._current_policy.action_probability_array.shape}")


if __name__ == "__main__":
    app.run(main)
