import pickle
from collections import defaultdict, Counter
import hashlib

# Load train data
with open("factkg/factkg_train.pickle", "rb") as f:
    train_data = pickle.load(f)

# Load DBpedia graph
with open("factkg/dbpedia_2015_undirected_light.pickle", "rb") as f:
    graph = pickle.load(f)

def ground_one_path(graph, start_entity, relations):
    path = [start_entity]

    for rel in relations:
        curr = path[-1]
        neighbors = graph.get(curr, {}).get(rel, [])

        if not neighbors:
            return None  # grounding failed

        # deterministic: pick first neighbor
        path.append(next(iter(neighbors)))

    return path

entities = set()
relations = set()
edges = set()
degree = Counter()

for claim_text, info in train_data.items():
    evidence = info["Evidence"]

    for start_entity, relation_paths in evidence.items():
        for rels in relation_paths:
            grounded = ground_one_path(graph, start_entity, rels)

            if grounded is None:
                continue

            # entities
            for e in grounded:
                entities.add(e)

            # relations
            for r in rels:
                relations.add(r)

            # edges
            for i in range(len(rels)):
                src = grounded[i]
                rel = rels[i]
                tgt = grounded[i + 1]

                edges.add((src, rel, tgt))
                degree[src] += 1
                degree[tgt] += 1

num_entities = len(entities)
num_relations = len(relations)
num_edges = len(edges)

print("TRAIN KG STATISTICS")
print("-" * 40)
print(f"Unique entities      : {num_entities}")
print(f"Unique relations     : {num_relations}")
print(f"Traversed edges      : {num_edges}")

if num_entities > 1:
    density = num_edges / (num_entities * (num_entities - 1))
else:
    density = 0

print(f"Graph density        : {density:.6e}")

print("\nTop 20 entities by degree:")
print("-" * 40)

for ent, deg in degree.most_common(20):
    print(f"{ent:40s} {deg}")

