import pyspiel
from absl import app, flags
from open_spiel.python.algorithms import exploitability

from predictive_cfr import PCFRSolver

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 500, "Number of iterations")
flags.DEFINE_string(
    "game",
    "turn_based_simultaneous_game(game=goofspiel(imp_info=True,num_cards=4,players=2,points_order=descending))",
    "Name of the game")
flags.DEFINE_integer("players", 2, "Number of players")
flags.DEFINE_integer("print_freq", 10,
                     "How often to print the exploitability")


def main(_):
    game = pyspiel.load_game(FLAGS.game)
    predictive_cfr_solver = PCFRSolver(game)

    for i in range(FLAGS.iterations):
        predictive_cfr_solver.evaluate_and_update_policy()
        if i % FLAGS.print_freq == 0:
            conv = exploitability.exploitability(
                game, predictive_cfr_solver.average_policy())
            print("Iteration {} exploitability {}".format(i, conv))


if __name__ == "__main__":
    app.run(main)
