from goofspiel_perfect import *
from goofspiel_noorder import *
from goofspiel_privateonly import *
from goofspiel_nopo import *
from exploitability import Exploitability
import os
import pickle
import numpy as np
from scipy.special import rel_entr
import matplotlib.pyplot as plt

import pyspiel

from open_spiel.python.policy import TabularPolicy


def probability_hist(policy, name=None):
    probs = policy.action_probability_array.flatten()
    logbins = np.logspace(-5, 0, num=20)
    plt.hist(probs, bins=logbins)
    plt.xscale("log")
    plt.yscale("log")
    plt.title(name)
    if fname is not None:
        plt.savefig(f"{name}.png")
    else:
        plt.show()
    plt.close()


def residual_hist(policy, name=None):
    tmp = policy.legal_actions_mask / np.sum(policy.legal_actions_mask, axis=-1, keepdims=True)
    residuals = np.abs(policy.action_probability_array - tmp).mean(axis=-1).flatten()
    plt.hist(residuals, bins=20)
    plt.yscale("log")
    if fname is not None:
        plt.savefig(f"{name}.png")
    else:
        plt.show()
    plt.close()


def kl_hist(policy, name=None):
    data = np.empty(len(policy.action_probability_array))
    for i, (strategy_all, mask) in enumerate(zip(policy.action_probability_array, policy.legal_actions_mask)):
        strategy = strategy_all[mask.astype(bool)]
        data[i] = rel_entr(strategy, np.ones_like(strategy) / len(strategy)).sum()
    plt.hist(data[data > 0], bins=20)
    plt.yscale("log")
    plt.title(name)
    if fname is not None:
        plt.savefig(f"{name}.png")
    else:
        plt.show()
    plt.close()


def prune_low_prob(policy, prob_threshold):
    result = policy.__copy__()
    for info_state in result.state_lookup:
        state_policy = result.policy_for_key(info_state)
        state_policy[state_policy < prob_threshold] = 0
        state_policy /= state_policy.sum()
    return result


def prune_near_uniform(policy, residual_thresold):
    result = policy.__copy__()
    for info_state in result.state_lookup:
        state_policy = result.policy_for_key(info_state)
        legal_action_probs = state_policy[state_policy != 0]
        residuals = np.abs(legal_action_probs - 1 / legal_action_probs.size)
        if residuals.sum() < residual_thresold:
            state_policy[state_policy != 0] = 1 / legal_action_probs.size
    return result

def prune_near_uniform_kl(policy, residual_thresold):
    result = policy.__copy__()
    for i in range(result.action_probability_array.shape[0]):
        strategy_all = policy.action_probability_array[i]
        mask = policy.legal_actions_mask[i]
        strategy = strategy_all[mask.astype(bool)]
        if rel_entr(strategy, np.ones_like(strategy) / len(strategy)).sum() < residual_thresold:
            result.action_probability_array[i] = mask / len(strategy)
    return result


if __name__ == "__main__":
    from info_state_mapping import apply_mapping
    from human_metrics import get_policy_list_from_policy, thinking_isets, total_support_size

    for nc, nt in [(4, 4), (5, 3)]:
    # for nc, nt in [(3, 3), (4, 3), (4, 4), (5, 3)]:
        nc_str = f"num_cards={nc}"
        nt_str = f"num_turns={nt}"
        perfect_game = pyspiel.load_game(
            f"python_goofspiel_perfect({nc_str},{nt_str})")
        e = Exploitability(perfect_game)

        for name in ["noorder", "privateonly", "nopo"]:
            game_name = f"python_goofspiel_{name}_asymmetric_mapped({nc_str},{nt_str})"
            fname = f"{game_name}.pickle"
            print(fname)
            # with open(f"models/asymmetric/{fname}", "rb") as f:
            #     solver = pickle.load(f)
            # avg_policy = solver.average_policy()
            with open(f"models/asymmetric/{fname}", "rb") as f:
                avg_policy = pickle.load(f)

            # kl_hist(avg_policy, f"{nc}-{nt}-kl")
            # probability_hist(avg_policy, f"{nc}-{nt}-prob")
            # # residual_hist(avg_policy, f"{nc}-{nt}-res")

            # for threshold in [0.01, 0.05, 0.10, 0.15, 0.20]:
            for threshold in [0.01, 0.05, 0.10, 0.20, 0.30, 0.40]:
                pruned_policy = prune_near_uniform_kl(avg_policy, threshold)

                policy_stats = ""
                for player in [0, 1]:
                    tlist = thinking_isets(get_policy_list_from_policy(pruned_policy, player))
                    num_t_iset = len(tlist)
                    t_support = total_support_size(tlist)
                    policy_stats += f"(Player {player}: {num_t_iset=}, {t_support=})"

                if name != "perfect":
                    mapped_policy = apply_mapping(name, nc, nt, pruned_policy)
                else:
                    mapped_policy = pruned_policy
                print(f"{threshold=}, {policy_stats}, exploitability={e.exploitability(mapped_policy)}")
                with open(f"models/pruned/{game_name}-{threshold}-kl.pickle", "wb+") as f:
                    pickle.dump(pruned_policy, f)
