import os
import matplotlib.pyplot as plt

nc, nt = 5, 3
target_type = f"num_cards={nc},num_turns={nt}"

legend_map = {
    "no_order": "No Bet Order",
    "no_po": "NBO-PO",
    "private_only": "Private Only",
    "perfect": "Perfect Info"
}

files = [fname for fname in os.listdir("models") if
         fname.endswith(".log") and target_type in fname]


for file in files:
    legend_name = ""
    for k, v in legend_map.items():
        if k in file:
            legend_name = v

    with open(f"models/{file}", "r") as f:
        data = f.readlines()

    iters = []
    values = []
    for line in data:
        [_, it, _, val] = line.split()
        iters.append(int(it))
        values.append(float(val))

    plt.plot(iters, values, label=legend_name)

plt.legend()
plt.title(target_type)
plt.yscale("log")
plt.savefig(f"{target_type}.png")


