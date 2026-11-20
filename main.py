"""Mini-Courier Planner: sort -> knapsack -> Dijkstra -> nearest-neighbour TSP.

Usage:
    python main.py                      # small sample dataset
    python main.py --size large         # large sample dataset
    python main.py --capacity 40        # change truck capacity
"""
import argparse
import time

from data_gen import DEPOT, load_edges, load_parcels
from graph import build_graph, dijkstra, get_path, nearest_neighbour_route
from knapsack import knapsack, print_dp_table
from sorting import prioritise_parcels


def show_parcels(title, parcels, limit=15):
    print(f"\n{title}")
    print(f"{'ID':<7}{'Weight':>7}{'Priority':>9}{'Deadline':>9}  Destination")
    for p in parcels[:limit]:
        print(f"{p['id']:<7}{p['weight']:>7}{p['priority']:>9}{p['deadline']:>9}  {p['destination']}")
    if len(parcels) > limit:
        print(f"... ({len(parcels) - limit} more)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", choices=["small", "large"], default="small")
    ap.add_argument("--capacity", type=int, default=50, help="truck capacity in kg")
    args = ap.parse_args()

    parcels = load_parcels(f"data/parcels_{args.size}.csv")
    graph = build_graph(load_edges(f"data/graph_{args.size}.json"))
    print(f"Loaded {len(parcels)} parcels, {len(graph)} graph nodes, capacity = {args.capacity} kg")

    # ---- Phase 2a: prioritise (Merge Sort) ----
    t = time.perf_counter()
    sorted_parcels = prioritise_parcels(parcels)
    t_sort = time.perf_counter() - t
    show_parcels("Parcels sorted by deadline (then priority):", sorted_parcels)

    # ---- Phase 2b: choose parcels for one trip (DP knapsack) ----
    t = time.perf_counter()
    best_value, chosen, dp = knapsack(sorted_parcels, args.capacity)
    t_knap = time.perf_counter() - t
    if len(sorted_parcels) <= 15:
        print()
        print_dp_table(dp, sorted_parcels)
    show_parcels("Selected parcels for this trip:", chosen)
    print(f"Total weight = {sum(p['weight'] for p in chosen)} / {args.capacity} kg, "
          f"total priority value = {best_value}")

    # ---- Phase 3a: Dijkstra from depot ----
    stops = [p["destination"] for p in chosen]
    t = time.perf_counter()
    dist, prev = dijkstra(graph, DEPOT)
    t_dij = time.perf_counter() - t
    print("\nShortest paths from the depot (Dijkstra):")
    for s in list(dict.fromkeys(stops))[:10]:
        print(f"  {DEPOT} -> {s}: {dist[s]}  via {' -> '.join(get_path(prev, s))}")

    # ---- Phase 3b: delivery route (nearest-neighbour TSP) ----
    t = time.perf_counter()
    order, total, full_path = nearest_neighbour_route(graph, DEPOT, stops)
    t_tsp = time.perf_counter() - t
    print("\nDelivery order :", " -> ".join(order))
    print("Full road path :", " -> ".join(full_path))
    print(f"Total route length = {total}")

    print("\nRuntime summary (seconds):")
    print(f"  sort={t_sort:.6f}  knapsack={t_knap:.6f}  dijkstra(1 run)={t_dij:.6f}  route={t_tsp:.6f}")


if __name__ == "__main__":
    main()
