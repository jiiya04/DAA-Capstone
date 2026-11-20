"""Phase 4: runtime of each major step for growing input sizes + chart + correctness checks."""
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_gen import DEPOT, generate_edges, generate_parcels
from graph import build_graph, dijkstra, nearest_neighbour_route
from knapsack import knapsack
from sorting import prioritise_parcels

SIZES = [10, 50, 100, 250, 500, 1000]
CAPACITY = 100


def timed(fn, *a):
    t = time.perf_counter()
    out = fn(*a)
    return out, time.perf_counter() - t


def run():
    rows = []
    for n in SIZES:
        locs = max(5, n // 5)
        parcels = generate_parcels(n, locs, seed=n)
        graph = build_graph(generate_edges(locs, seed=n))

        sorted_p, t_sort = timed(prioritise_parcels, parcels)
        (val, chosen, _), t_knap = timed(knapsack, sorted_p, CAPACITY)
        _, t_dij = timed(dijkstra, graph, DEPOT)
        stops = [p["destination"] for p in chosen]
        (_, total, _), t_tsp = timed(nearest_neighbour_route, graph, DEPOT, stops)

        # ---- correctness checks ----
        keys = [(p["deadline"], -p["priority"]) for p in sorted_p]
        assert keys == sorted(keys), "sort incorrect"
        assert sum(p["weight"] for p in chosen) <= CAPACITY, "capacity exceeded"
        assert sum(p["priority"] for p in chosen) == val, "knapsack value mismatch"

        rows.append((n, t_sort, t_knap, t_dij, t_tsp, val, total))
        print(f"n={n:<5} sort={t_sort:.5f}s knapsack={t_knap:.5f}s "
              f"dijkstra={t_dij:.5f}s route={t_tsp:.5f}s | value={val} route_len={total}")
    print("All correctness checks passed.")
    return rows


def plot(rows):
    n = [r[0] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    for idx, name in [(1, "Merge sort"), (2, "Knapsack DP"), (3, "Dijkstra (1 run)"), (4, "NN route")]:
        ax[0].plot(n, [r[idx] for r in rows], marker="o", label=name)
        ax[1].plot(n, [r[idx] for r in rows], marker="o", label=name)
    ax[0].set(title="Runtime vs input size", xlabel="Number of parcels", ylabel="Seconds")
    ax[1].set(title="Runtime vs input size (log scale)", xlabel="Number of parcels",
              ylabel="Seconds", yscale="log")
    for a in ax:
        a.grid(alpha=0.3)
        a.legend()
    fig.tight_layout()
    fig.savefig("screenshots/runtime_chart.png", dpi=150)
    print("Chart saved to screenshots/runtime_chart.png")


if __name__ == "__main__":
    plot(run())
