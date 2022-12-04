from goofspiel_perfect import *
from goofspiel_noorder import *
from goofspiel_privateonly import *
from goofspiel_nopo import *
from exploitability import Exploitability, map_policy
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

import pyspiel

from open_spiel.python.policy import TabularPolicy


def probability_hist(policy):
    plt.hist(policy.action_probability_array.flatten(), bins=20, range=(1e-8, 1))
    plt.show()


def prune_low_prob(policy, prob_threshold):
    result = policy.__copy__()
    for info_state in result.state_lookup:
        state_policy = result.policy_for_key(info_state)
        state_policy[state_policy < prob_threshold] = 0
        state_policy /= state_policy.sum()
    return result


# untested
def prune_near_uniform(policy, residual_thresold):
    result = policy.__copy__()
    for info_state in result.state_lookup:
        state_policy = result.policy_for_key(info_state)
        legal_action_probs = state_policy[state_policy != 0]
        residuals = np.abs(legal_action_probs - 1 / legal_action_probs.size)
        if residuals.sum() > residual_thresold:
            state_policy[state_policy != 0] = 1 / legal_action_probs.size
    return result


if __name__ == "__main__":
    for name in ["noorder", "perfect"]:
        for nc, nt in [(3, 3), (4, 3), (4, 4), (5, 3)]:
            nc_str = f"num_cards={nc}"
            nt_str = f"num_turns={nt}"
            game = pyspiel.load_game(f"python_goofspiel_{name}({nc_str},{nt_str})")
            fname = f"python_goofspiel_{name}({nc_str},{nt_str}).pickle"
            print(fname)
            with open(f"models/{fname}", "rb") as f:
                solver = pickle.load(f)
            avg_policy = solver.average_policy()

            # probability_hist(avg_policy)

            for threshold in [0.01, 0.05, 0.1, 0.15, 0.2]:  # 0.05 should be similar to 0.2? jknvm apparently not
                print(f"threshold={threshold}")
                perfect_game = pyspiel.load_game(f"python_goofspiel_perfect({nc_str},{nt_str})")
                pruned_policy = prune_low_prob(avg_policy, threshold)
                if name != "perfect":
                    map_fname = f"python_goofspiel_perfect_to_{name}_infoset_mapping({nc_str},{nt_str}).pkl"
                    with open(f"mappings/{map_fname}", "rb") as f:
                        mapping = pickle.load(f)
                    pruned_policy = map_policy(pruned_policy, mapping, perfect_game)
                e = Exploitability(perfect_game)
                print(e.exploitability(pruned_policy))
