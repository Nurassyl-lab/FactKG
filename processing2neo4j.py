import pickle
import csv
from collections import deque


with open("factkg/factkg_train.pickle", "rb") as f:
    train_data = pickle.load(f)

with open("factkg/factkg_dev.pickle", "rb") as f:
    dev_data = pickle.load(f)

with open("factkg/factkg_test.pickle", "rb") as f:
    test_data = pickle.load(f)

def collect_entities(data):
    ents = set()
    for claim, info in data.items():
        ents.update(info["Entity_set"])
    return ents

# seed_entities = (
#     collect_entities(train_data)
#     | collect_entities(dev_data)
#     | collect_entities(test_data)
# )
evidence_entities = set()

for data in [train_data, dev_data, test_data]:
    for _, info in data.items():
        if "Evidence" in info.keys():
            evidence_entities.update(info["Evidence"].keys())
        elif "existence" in info["types"]:
                evidence_entities.update(info["Entity_set"])
        else:
            print(f"{info.keys()} has no Evidence key")
            print(info)
            exit()


# print("Seed entities:", len(seed_entities))

with open("factkg/dbpedia_2015_undirected_light.pickle", "rb") as f:
    graph = pickle.load(f)
print("Graph loaded with", len(graph), "entities")

with open("factkg/relations_for_final.pickle", "rb") as f:
    allowed_relations = pickle.load(f)
print("Allowed relations:", len(allowed_relations))


K = 2

# nodes = set(seed_entities)
if type(evidence_entities) != set:
    nodes = set(evidence_entities)
else:
    nodes = evidence_entities
edges = set()

# queue = deque([(e, 0) for e in seed_entities])
queue = deque([(e, 0) for e in evidence_entities])
# visited = set(seed_entities)
visited = set(evidence_entities)

while queue:
    current, depth = queue.popleft()
    if depth == K:
        continue

    if current not in graph:
        continue

    for rel, neighbors in graph[current].items():
        if rel not in allowed_relations:
            continue

        for nbr in neighbors:
            edges.add((current, rel, nbr))

            if nbr not in visited:
                visited.add(nbr)
                nodes.add(nbr)
                queue.append((nbr, depth + 1))

print("Final nodes:", len(nodes))
print("Final edges:", len(edges))

with open("nodes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "label"])
    for n in nodes:
        writer.writerow([n, "Entity"])

def normalize_relation(r):
    if r.startswith("~"):
        return "REV_" + r[1:]
    return r

with open("edges.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "type"])
    for s, r, t in edges:
        writer.writerow([s, t, normalize_relation(r)])

