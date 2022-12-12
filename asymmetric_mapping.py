import pyspiel
from absl import app, flags
import sys
import pickle

from predictive_cfr import PCFRSolver

from goofspiel_noorder import *
from goofspiel_privateonly import *
from goofspiel_nopo import *

from goofspiel_noorder_asymmetric import *
from goofspiel_privateonly_asymmetric import *
from goofspiel_nopo_asymmetric import *

from exploitability import Exploitability
from info_state_mapping import apply_mapping

from open_spiel.python.policy import TabularPolicy


def apply_asymm_mapping(name, nc, nt, policy1, policy2):
    nc_str = f"num_cards={nc}"
    nt_str = f"num_turns={nt}"

    game = pyspiel.load_game(f"python_goofspiel_{name}({nc_str},{nt_str})")
    mapped_policy = TabularPolicy(game)

    for info_state in mapped_policy.state_lookup:
        mapped_state_policy = mapped_policy.policy_for_key(info_state)
        if "p0" in info_state:
            assert "p1" not in info_state
            state_policy = policy1.policy_for_key(info_state)
        else:
            assert "p1" in info_state
            state_policy = policy2.policy_for_key(info_state)
        mapped_state_policy[:] = state_policy

    return mapped_policy


def main_map_to_symm(_):
    for name_str in ["noorder", "privateonly", "nopo"]:
        for num_cards, num_turns in [(4, 4), (5, 3)]:
            game_str1 = f"python_goofspiel_{name_str}_asymmetric(num_cards={num_cards},num_turns={num_turns},abstract_player=0)"
            game_str2 = f"python_goofspiel_{name_str}_asymmetric(num_cards={num_cards},num_turns={num_turns},abstract_player=1)"
            with open(f"models/asymmetric/{game_str1}.pickle", "rb") as f:
                solver1 = pickle.load(f)
            avg_policy1 = solver1.average_policy()
            with open(f"models/asymmetric/{game_str2}.pickle", "rb") as f:
                solver2 = pickle.load(f)
            avg_policy2 = solver2.average_policy()

            mapped_policy = apply_asymm_mapping(name_str, num_cards, num_turns, avg_policy1, avg_policy2)
            fname = f"python_goofspiel_{name_str}_asymmetric_mapped(num_cards={num_cards},num_turns={num_turns})"
            print(fname)
            with open(f"models/asymmetric/{fname}.pickle", "wb") as f:
                pickle.dump(mapped_policy, f)

            game = pyspiel.load_game(f"python_goofspiel_{name_str}(num_cards={num_cards},num_turns={num_turns})")
            e = Exploitability(game)
            print(e.exploitability(mapped_policy))


def main_map_to_perfect(_):
    for num_cards, num_turns in [(4, 4), (5, 3)]:
        game = pyspiel.load_game(f"python_goofspiel_perfect(num_cards={num_cards},num_turns={num_turns})")
        e = Exploitability(game)
        for name_str in ["noorder", "privateonly", "nopo"]:
            fname = f"python_goofspiel_{name_str}_asymmetric_mapped(num_cards={num_cards},num_turns={num_turns})"
            print(fname)
            with open(f"models/asymmetric/{fname}.pickle", "rb") as f:
                policy = pickle.load(f)

            mapped_policy = apply_mapping(name_str, num_cards, num_turns, policy)
            print(e.exploitability(mapped_policy))


if __name__ == "__main__":
    app.run(main_map_to_perfect)
