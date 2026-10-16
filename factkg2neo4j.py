import pickle
import os
import random
import json
from tqdm import tqdm
from neo4j import GraphDatabase
import matplotlib.pyplot as plt

path = "factkg/factkg_train.pickle"

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "11082000"  # <-- Change this!

PATH = "factkg/statistics/"

with open(path, 'rb') as f:
    data = pickle.load(f)

def plot_bar_chart(x, name):
    # x is a dictionary
    # sort x by values in ascending order
    sorted_items = sorted(x.items(), key=lambda item: item[1], reverse=True)
    keys = [k for k, v in sorted_items]
    values = [v for k, v in sorted_items]

    plt.figure(figsize=(10, 6))
    plt.barh(keys[:20], values[:20])
    plt.xlabel('Values')
    plt.ylabel('Keys')
    plt.title('Bar Chart')
    plt.tight_layout()
    plt.savefig(os.path.join(PATH, name))
    plt.close()


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def upload_triple(tx, commands):
    # tx.run(
    #     """
    #     MERGE (h:Entity {name: $head})
    #     MERGE (t:Entity {name: $tail})
    #     MERGE (h)-[r:`%s`]->(t)
    #     """ % relation, head=head, tail=tail
    # )
    tx.run(commands)

def load_triples(triple_commands, head, tail, relation):
        command = f"""
        MERGE (h:Entity {{name: $head}})
        MERGE (t:Entity {{name: $tail}})
        MERGE (h)-[r:`{relation}`]->(t)
        """

### For training KGE I need ###
entities_dict = {} # keys: id, values: entities
relations_dict = {} # keys: id, values: entities
all_triples = [] # for train.txt, test.txt, valid.txt

entity_counter = 0
relations_counter = 0
###############################

with driver.session() as session:
    keys = list(data.keys())
    entities_tracker = {}
    relations_tracker = {}
    for key in tqdm(keys, desc=f"Iterating through `{path}` dataset"):
        sample = data[key]
        evidence = sample["Evidence"]
        entities = list(evidence.keys())
        relations = list(evidence.values())
        for index, (head, tail) in enumerate(zip(entities[:-1], entities[1:])):
            for relation in relations[index]:
                # print(head, relation[0], tail) # triple (head, entity, tail)
                triple = [head, relation[0], tail]
                # session.execute_write(upload_triple, head, relation[0], tail)

                # if head not in list(entities_tracker.keys()):
                #     entities_tracker[head] = 1
                # else:
                #     entities_tracker[head] += 1

                # if relation[0] not in list(relations_tracker.keys()):
                #     relations_tracker[relation[0]] = 1
                # else:
                #     relations_tracker[relation[0]] += 1
                
                # For KGE
                if head not in list(entities_dict.keys()):
                    entities_dict[head] = entity_counter
                    entity_counter += 1
                if tail not in list(entities_dict.keys()):
                    entities_dict[tail] = entity_counter
                    entity_counter += 1
                if relation[0] not in list(relations_dict.keys()):
                    relations_dict[relation[0]] = relations_counter
                    relations_counter += 1
                all_triples.append(triple)

# with open(os.path.join(PATH, "entities_tracker.json"), "w") as f:
#     json.dump(entities_tracker, f, indent=4)

# with open(os.path.join(PATH, "relation_tracker.json"), "w") as f:
#     json.dump(relations_tracker, f, indent=4)

# plot_bar_chart(entities_tracker, "entities_tracker.png")
# plot_bar_chart(relations_tracker, "relations_tracker.png")

# entities_dict should be written into entities.dict file
with open(os.path.join(PATH, "entities.dict"), "w") as f :
    for key, value in entities_dict.items():
        f.write(f"{value}\t{key}\n")

with open(os.path.join(PATH, "relations.dict"), "w") as f :
    for key, value in relations_dict.items():
        f.write(f"{value}\t{key}\n")

# I have a list all_triples
# please use it to create 3 files: train.txt, valid.txt, test.txt
# each triple should be written in the file 

random.shuffle(all_triples)
n = len(all_triples)
train_end = int(0.8 * n)
valid_end = int(0.9 * n)

splits = {
    "train.txt": all_triples[:train_end],
    "valid.txt": all_triples[train_end:valid_end],
    "test.txt": all_triples[valid_end:]
}

for filename, triples in splits.items():
    with open(os.path.join(PATH, filename), "w") as f:
        for triple in triples:
            f.write("\t".join(triple) + "\n")
