import pickle
import csv
import hashlib
from tqdm import tqdm

def make_claim_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


with open("factkg/dbpedia_2015_undirected_light.pickle", "rb") as f:
    graph = pickle.load(f)

def ground_paths(graph, start_entity, relations, max_paths=10):
    """
    Returns a list of grounded entity paths:
    [
      [E0, E1, E2],
      ...
    ]
    """
    paths = [[start_entity]]

    for rel in relations:
        new_paths = []

        for p in paths:
            curr = p[-1]
            neighbors = graph.get(curr, {}).get(rel, [])

            for nbr in neighbors:
                new_paths.append(p + [nbr])
                if len(new_paths) >= max_paths:
                    break

        paths = new_paths
        if not paths:
            break

    return paths

def build_full_path(entities, relations):
    """
    entities: [E0, E1, ..., Ek]
    relations: [r1, r2, ..., rk]
    """
    full = []
    for i in range(len(relations)):
        full.append(entities[i])
        full.append(relations[i])
    full.append(entities[-1])
    return full

def dump_factkg_split(data, writer, graph):
    for claim_text, info in tqdm(data.items(), desc="Processing claims"):
        cid = make_claim_id(claim_text)

        label = int(info["Label"][0])
        reasoning_types = info["types"]
        entities_in_claim = info["Entity_set"]
        evidence = info["Evidence"]

        num_entities = len(entities_in_claim)
        num_total_paths = sum(len(p) for p in evidence.values())

        for start_entity, relation_paths in evidence.items():
            for relations in relation_paths:
                grounded_entity_paths = ground_paths(
                    graph,
                    start_entity,
                    relations
                )

                for entity_path in grounded_entity_paths:
                    full_path = build_full_path(entity_path, relations)

                    writer.writerow({
                        "claim_id": cid,
                        "claim_text": claim_text,
                        "label": label,
                        "reasoning_types": "|".join(reasoning_types),
                        "start_entity": start_entity,
                        "path_entities": "|".join(entity_path),
                        "path_relations": "|".join(relations),
                        "full_path": "|".join(full_path),
                        "path_length": len(relations),
                        "has_reverse": any(r.startswith("~") for r in relations),
                        "num_entities_in_claim": num_entities,
                        "num_total_paths_for_claim": num_total_paths
                    })

fieldnames = [
    "claim_id",
    "claim_text",
    "label",
    "reasoning_types",
    "start_entity",
    "path_entities",
    "path_relations",
    "full_path",
    "path_length",
    "has_reverse",
    "num_entities_in_claim",
    "num_total_paths_for_claim"
]

with open("factkg_grounded_paths.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    # for split in ["train", "dev", "test"]:
    for split in ["train"]:
        with open(f"factkg/factkg_{split}.pickle", "rb") as pf:
            data = pickle.load(pf)

        dump_factkg_split(data, writer, graph)
