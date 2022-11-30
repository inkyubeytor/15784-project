import pyspiel
from absl import app, flags
import cProfile
import time

from predictive_cfr import PCFRSolver

from goofspiel import *
from exploitability import *
import resource

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 1, "Number of iterations")
flags.DEFINE_string(
    "game",
    "python_goofspiel(num_cards=4,num_turns=3)",
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", -1,
                     "How often to print the exploitability")


def main(_):
    t0 = time.time()
    game = pyspiel.load_game(FLAGS.game)
    predictive_cfr_solver = PCFRSolver(game)
    e = Exploitability(game)
    t1 = time.time()
    print(f"Setup: {t1 - t0} seconds")

    first_iter_time = 0
    noprint_iter_time = 0
    noprint_iter_count = 0
    print_iter_time = 0
    print_iter_count = 0
    for i in range(FLAGS.iterations):
        t0 = time.time()
        predictive_cfr_solver.evaluate_and_update_policy()
        if FLAGS.print_freq > 0 and i % FLAGS.print_freq == 0:
            conv = e.exploitability(predictive_cfr_solver.average_policy())
            print("Iteration {} exploitability {}".format(i, conv))
        t1 = time.time()
        diff = t1 - t0
        if i == 0:
            first_iter_time += diff
        elif FLAGS.print_freq > 0 and i % FLAGS.print_freq == 0:
            print_iter_time += diff
            print_iter_count += 1
        else:
            noprint_iter_time += diff
            noprint_iter_count += 1

    print(f"First iter time: {first_iter_time}")
    print(f"Print iter average: {print_iter_time / print_iter_count if print_iter_count else 0}")
    print(f"No Print iter average: {noprint_iter_time / noprint_iter_count if noprint_iter_count else 0}")
    print(f"Peak memory usage (KB): {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":

    app.run(main)


    # cProfile.run("app.run(main)", "py_3_3_stats")
    #
    # import pstats
    # from pstats import SortKey
    # p = pstats.Stats("py_3_3_stats")
    # p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(.05)
