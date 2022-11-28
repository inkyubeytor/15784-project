import pyspiel
from absl import app, flags
from open_spiel.python.algorithms import exploitability
import cProfile

from predictive_cfr import PCFRSolver

from goofspiel import *
from exploitability import *

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 5, "Number of iterations")
flags.DEFINE_string(
    "game",
    "python_goofspiel(num_cards=3,num_turns=3)",
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 1,
                     "How often to print the exploitability")


def main(_):
    game = pyspiel.load_game(FLAGS.game)
    predictive_cfr_solver = PCFRSolver(game)
    e = Exploitability(game)
    for i in range(FLAGS.iterations):
        predictive_cfr_solver.evaluate_and_update_policy()
        if i % FLAGS.print_freq == 0:
            conv = e.exploitability(predictive_cfr_solver.average_policy())
            print("Iteration {} exploitability {}".format(i, conv))


if __name__ == "__main__":
    # app.run(main)
    cProfile.run("app.run(main)", "py_3_3_stats")

    import pstats
    from pstats import SortKey
    p = pstats.Stats("py_3_3_stats")
    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(.05)
