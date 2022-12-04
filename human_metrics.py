import numpy as np


def get_policy_list(s, player):
    local_policies = []
    avg_policy = s.average_policy()
    legal_actions_mask = avg_policy.legal_actions_mask
    policy_table = avg_policy.action_probability_array
    for state in avg_policy.states_per_player[player]:
        i = avg_policy.state_lookup[state]
        local_policies.append(policy_table[i][legal_actions_mask[i].astype(bool)])
    return local_policies


def thinking_isets(policy_list):
    return [policy for policy in policy_list if not np.allclose(policy, np.ones_like(policy) / len(policy))]


def total_support_size(policy_list):
    count = 0
    for policy in policy_list:
        for ap in policy:
            if ap > 0:
                count += 1
    return count


if __name__ == "__main__":
    import pickle
    with open("models/python_goofspiel_nopo(num_cards=5,num_turns=3).pickle", "rb") as f:
        solver = pickle.load(f)
    for player in [0, 1]:
        print(player)
        plist = get_policy_list(solver, player)
        tlist = thinking_isets(plist)
        print(f"Iset Counts - {len(tlist)} {len(plist)}")
        print(f"Support Counts - {total_support_size(tlist)} {total_support_size(plist)}")
