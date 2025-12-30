# ecolens.py
# EcoLens: simplified ecosystem simulation (predator–prey with resource dynamics)
# Usage: python3 ecolens.py --days 200 --init_prey 80 --init_pred 15
# Outputs: graphs saved to ../graphs, log saved to ../logs/ecolens_history.json

import os, json, argparse, random, math
import numpy as np
import matplotlib.pyplot as plt

# ----------------- CONFIG (paths) -----------------
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
OUT_GRAPHS = os.path.join(BASE_DIR, "graphs")
OUT_LOGS = os.path.join(BASE_DIR, "logs")
os.makedirs(OUT_GRAPHS, exist_ok=True)
os.makedirs(OUT_LOGS, exist_ok=True)

# include your uploaded research doc path in the report
UPLOADED_RESEARCH_DOC = None

# ----------------- Ecosystem model -----------------
class Individual:
    def __init__(self, energy=1.0, efficiency=1.0):
        self.energy = energy
        self.efficiency = efficiency

def run_sim(days=200,
            init_prey=80,
            init_pred=15,
            init_resource=300.0,
            resource_regen=8.0,
            prey_consumption=1.0,
            pred_consumption=2.0,
            prey_repro_thresh=2.0,
            pred_repro_thresh=5.0,
            prey_mut_rate=0.05,
            pred_mut_rate=0.03,
            shock_chance=0.02,
            seed=42):
    random.seed(seed)
    np.random.seed(seed)

    # initialize populations as lists of Individuals
    prey = [Individual(energy=1.0, efficiency=random.uniform(0.6,1.0)) for _ in range(init_prey)]
    predators = [Individual(energy=2.0, efficiency=random.uniform(0.6,1.0)) for _ in range(init_pred)]
    resource = init_resource

    history = {
        "day": [],
        "prey_count": [],
        "pred_count": [],
        "resource": [],
        "prey_avg_eff": [],
        "pred_avg_eff": []
    }

    for day in range(days):
        # resource consumption by prey proportional to efficiency
        prey_need = sum(prey_consumption * (0.5 + p.efficiency) for p in prey)
        available_to_prey = min(resource, prey_need)
        # allocate resource to prey proportional to efficiency
        if prey:
            shares = [(0.5 + p.efficiency) for p in prey]
            total_shares = sum(shares) or 1.0
            for p, share in zip(prey, shares):
                got = available_to_prey * (share / total_shares)
                p.energy += got * p.efficiency * 0.1  # convert resource to energy

        # predation: predators eat prey if prey exist
        random.shuffle(prey)
        random.shuffle(predators)
        eaten_prey = []
        for pred in predators:
            if not prey:
                break
            # predator success probability proportional to predator efficiency vs random
            if random.random() < (0.3 + 0.4 * pred.efficiency):
                target = prey.pop(0)
                pred.energy += pred_consumption * pred.efficiency
                eaten_prey.append(target)

        # reproduction & death for prey
        new_prey = []
        for p in prey:
            # reproduction if energy crosses threshold
            if p.energy > prey_repro_thresh and random.random() < 0.6:
                # child inherits efficiency with small mutation
                child_eff = max(0.05, p.efficiency + random.uniform(-prey_mut_rate, prey_mut_rate))
                new_prey.append(Individual(energy=1.0, efficiency=child_eff))
                p.energy *= 0.6  # reproduction cost
            # survival: baseline survival plus energy factor
            if p.energy > 0.1 and random.random() < (0.7 + 0.2 * (p.energy/ (prey_repro_thresh+1))):
                # small energy decay
                p.energy *= 0.9
                new_prey.append(p)
        # eaten prey don't return

        # predators reproduction & death
        new_preds = []
        for pr in predators:
            if pr.energy > pred_repro_thresh and random.random() < 0.5:
                child_eff = max(0.05, pr.efficiency + random.uniform(-pred_mut_rate, pred_mut_rate))
                new_preds.append(Individual(energy=2.0, efficiency=child_eff))
                pr.energy *= 0.5
            # predator baseline survival
            if pr.energy > 0.5 and random.random() < (0.6 + 0.2 * (pr.energy/(pred_repro_thresh+1))):
                pr.energy *= 0.92
                new_preds.append(pr)

        prey = new_prey
        predators = new_preds

        # resource regeneration and occasional shock
        resource = max(0.0, resource - available_to_prey) + resource_regen
        if random.random() < shock_chance:
            resource *= random.uniform(0.3, 0.7)

        # small environmental pressure: resource carrying capacity effect
        carrying = max(1.0, init_resource * (1 + 0.005 * math.sin(day/10.0)))
        if resource > carrying:
            resource *= 0.98

        # record statistics
        history["day"].append(day)
        history["prey_count"].append(len(prey))
        history["pred_count"].append(len(predators))
        history["resource"].append(resource)
        history["prey_avg_eff"].append(sum((p.efficiency for p in prey), 0.0) / (len(prey) or 1))
        history["pred_avg_eff"].append(sum((p.efficiency for p in predators), 0.0) / (len(predators) or 1))

        # safety cap to avoid explosion
        if len(prey) > 2000:
            prey = prey[:2000]
        if len(predators) > 500:
            predators = predators[:500]

    # end sim
    return history

# ----------------- plotting utilities -----------------
def plot_ecolens(history, out_dir):
    days = history["day"]
    fig, ax1 = plt.subplots(figsize=(9,4))
    ax1.plot(days, history["prey_count"], label="Prey count")
    ax1.plot(days, history["pred_count"], label="Predator count")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Population")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(days, history["resource"], label="Resource", color="tab:green", alpha=0.6)
    ax2.set_ylabel("Resource")
    # combine legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper right")
    plt.title("EcoLens: Population and Resource over Time")
    plt.tight_layout()
    p1 = os.path.join(out_dir, "ecolens_pop_resource.png")
    plt.savefig(p1)
    plt.close()

    # plot efficiency trends
    plt.figure(figsize=(9,3))
    plt.plot(days, history["prey_avg_eff"], label="Prey avg efficiency")
    plt.plot(days, history["pred_avg_eff"], label="Pred avg efficiency")
    plt.xlabel("Day")
    plt.ylabel("Avg efficiency")
    plt.title("EcoLens: Trait (efficiency) over time")
    plt.legend()
    plt.tight_layout()
    p2 = os.path.join(out_dir, "ecolens_efficiency.png")
    plt.savefig(p2)
    plt.close()

    # population phase plot (prey vs predator)
    plt.figure(figsize=(5,5))
    plt.plot(history["prey_count"], history["pred_count"], marker=".", linewidth=0.5)
    plt.xlabel("Prey count")
    plt.ylabel("Predator count")
    plt.title("EcoLens: Phase plot (Predator vs Prey)")
    plt.tight_layout()
    p3 = os.path.join(out_dir, "ecolens_phase.png")
    plt.savefig(p3)
    plt.close()

    return [p1,p2,p3]

# ----------------- CLI and runner -----------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=200)
    parser.add_argument("--init_prey", type=int, default=80)
    parser.add_argument("--init_pred", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    history = run_sim(days=args.days,
                      init_prey=args.init_prey,
                      init_pred=args.init_pred,
                      seed=args.seed)

    # save history
    out_json = os.path.join(OUT_LOGS, "ecolens_history.json")
    with open(out_json, "w") as f:
        json.dump(history, f, indent=2)

    # plot and save graphs
    imgs = plot_ecolens(history, OUT_GRAPHS)

    # summary report
    report = {
        "description": "EcoLens predator-prey-resource simulation",
        "parameters": {
            "days": args.days,
            "init_prey": args.init_prey,
            "init_pred": args.init_pred,
            "seed": args.seed
        },
        "graphs": imgs,
        "log": out_json,
        "uploaded_research_doc": UPLOADED_RESEARCH_DOC
    }
    with open(os.path.join(OUT_LOGS, "ecolens_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    print("EcoLens complete. Graphs:", imgs)
    print("Report saved to", os.path.join(OUT_LOGS, "ecolens_report.json"))

if __name__ == "__main__":
    main()
