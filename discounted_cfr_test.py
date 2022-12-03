import pyspiel
from absl import app, flags
import cProfile
import time

from discounted_cfr import DCFRSolver

from goofspiel import *
from exploitability import *
import resource
import pickle

game_str = "python_goofspiel(num_cards=4,num_turns=3,knowledge_type=no_po)"
print(game_str)

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 300, "Number of iterations")
flags.DEFINE_string(
    "game",
    game_str,
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 1,
                     "How often to print the exploitability")


def main(_):
    t0 = time.time()
    game = pyspiel.load_game(FLAGS.game)
    discounted_cfr_solver = DCFRSolver(game)
    e = Exploitability(game)
    t1 = time.time()
    print(f"Setup: {t1 - t0} seconds")

    first_iter_time = 0
    noprint_iter_time = 0
    noprint_iter_count = 0
    print_iter_time = 0
    print_iter_count = 0
    with open(f"models/{game_str}.log", "w+") as f:
        for i in range(FLAGS.iterations):
            t0 = time.time()
            discounted_cfr_solver.evaluate_and_update_policy()
            if FLAGS.print_freq > 0 and i % FLAGS.print_freq == 0:
                conv = e.exploitability(discounted_cfr_solver.average_policy())
                print("Iteration {} exploitability {}".format(i, conv), file=f)
                print("Iteration {} exploitability {}".format(i, conv))
                if conv < 0.001:
                    break
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

    with open(f"models/{game_str}.pickle", "wb+") as f:
        pickle.dump(discounted_cfr_solver, f)



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
