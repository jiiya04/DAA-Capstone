"""Dataset generators (random but reproducible via seed) and file I/O."""
import csv
import json
import random

DEPOT = "Depot"


def generate_parcels(n, n_locations, seed=1):
    rnd = random.Random(seed)
    return [
        {
            "id": f"P{i+1:04d}",
            "weight": rnd.randint(1, 15),
            "priority": rnd.randint(1, 100),
            "deadline": rnd.randint(1, 48),
            "destination": f"C{rnd.randint(1, n_locations)}",
        }
        for i in range(n)
    ]


def generate_edges(n_locations, extra_edges=None, seed=1):
    """Connected random graph: Depot + C1..Cn."""
    rnd = random.Random(seed)
    nodes = [DEPOT] + [f"C{i}" for i in range(1, n_locations + 1)]
    edges = set()
    for i in range(1, len(nodes)):                       # spanning tree => connected
        edges.add((nodes[rnd.randint(0, i - 1)], nodes[i], rnd.randint(1, 20)))
    extra = extra_edges if extra_edges is not None else n_locations * 2
    for _ in range(extra):
        a, b = rnd.sample(nodes, 2)
        edges.add((a, b, rnd.randint(1, 20)))
    return sorted(edges)


def save_parcels(path, parcels):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "weight", "priority", "deadline", "destination"])
        w.writeheader()
        w.writerows(parcels)


def load_parcels(path):
    with open(path) as f:
        return [
            {"id": r["id"], "weight": int(r["weight"]), "priority": int(r["priority"]),
             "deadline": int(r["deadline"]), "destination": r["destination"]}
            for r in csv.DictReader(f)
        ]


def save_edges(path, edges):
    with open(path, "w") as f:
        json.dump([list(e) for e in edges], f, indent=1)


def load_edges(path):
    with open(path) as f:
        return [tuple(e) for e in json.load(f)]


if __name__ == "__main__":
    # Creates the sample datasets in data/
    save_parcels("data/parcels_small.csv", generate_parcels(12, 6, seed=7))
    save_edges("data/graph_small.json", generate_edges(6, extra_edges=6, seed=7))
    save_parcels("data/parcels_large.csv", generate_parcels(1000, 200, seed=11))
    save_edges("data/graph_large.json", generate_edges(200, seed=11))
    print("Sample datasets written to data/")
