# Mini-Courier Planner

Capstone Assignment – Design & Analysis of Algorithms (ETCCDA302), K.R. Mangalam University.

Given parcels and delivery points, the program builds a **prioritised parcel list**, an **optimal packing plan** for one trip, and an **ordered delivery route**.

## Problem design (Phase 1)

| Item | Definition |
|---|---|
| Parcel | `id, weight (kg), priority (1-100), deadline (hours), destination` |
| Truck | one trip, fixed capacity in kg (default 50) |
| Graph | undirected, weighted adjacency list `{node: {neighbour: distance}}`; `Depot` plus customer nodes `C1..Cn` |
| Goal | pick parcels maximising total priority within capacity, then visit their destinations by a short route starting/ending at the depot |

| Step | Algorithm | Why chosen | Complexity |
|---|---|---|---|
| Sorting | Merge Sort (own implementation) | stable, guaranteed O(n log n) | O(n log n) time, O(n) space |
| Packing | 0/1 Knapsack, Dynamic Programming | exact optimum, parcels can't be split | O(n·W) time and space |
| Shortest path | Dijkstra with min-heap | non-negative distances | O((V+E) log V) |
| Route | Nearest-Neighbour TSP | TSP is NP-hard, greedy is fast but approximate | O(k²) lookups + (k+1) Dijkstra runs |

## Files

| File | Purpose |
|---|---|
| `sorting.py` | merge sort + parcel prioritisation |
| `knapsack.py` | DP knapsack, backtracking, table printing |
| `graph.py` | graph build, Dijkstra, nearest-neighbour route |
| `data_gen.py` | dataset generation and CSV/JSON loading |
| `main.py` | full pipeline demo |
| `benchmark.py` | runtime tests, correctness checks, chart |
| `data/` | sample datasets (small: 12 parcels, large: 1000 parcels) |
| `screenshots/` | program output traces and `runtime_chart.png` |


## Results (Phases 2-3, small dataset)

See `screenshots/output_small.txt`: 12 parcels sorted by deadline, DP table printed, 9 parcels chosen (48/50 kg, priority 358), route `Depot -> C1 -> C2 -> C6 -> C4 -> C5 -> Depot`, length 58.

## Performance testing (Phase 4)

`benchmark.py` times each step for n = 10 … 1000 parcels and asserts correctness (sort order, capacity respected, knapsack value matches). The chart is `screenshots/runtime_chart.png`.

Observations (from `screenshots/benchmark_output.txt`):
- Merge sort and a single Dijkstra run stay tiny even at 1000 parcels (a few milliseconds or less).
- Knapsack grows steadily with n (and with capacity W), as expected from O(n*W).
- Route building grows fastest: it runs one Dijkstra per selected stop, so at n = 1000 it overtakes knapsack. Caching or reusing shortest-path results is the best place to optimise.

## Optimisation ideas

- Use a 1-D DP array when the chosen set isn't needed (O(W) space), or keep the table only when backtracking.
- Compute Dijkstra only from stops that are actually selected (already done) and cache results across trips.
- Improve the nearest-neighbour route with **2-opt** local search, or use Christofides for a 1.5-approximation on metric graphs.
- Add multiple trips: repeat knapsack on the remaining parcels until all are delivered.

## Limitations

Nearest-neighbour is not optimal; the knapsack uses integer weights; one truck, one trip.
