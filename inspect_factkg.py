print("Step 0.1.1")
import pickle
from pprint import pprint

with open("factkg/factkg_train.pickle", "rb") as f:
    train_data = pickle.load(f)

print(type(train_data))
print(len(train_data))

print("\nStep 0.1.2 --> Since train_data is a dictionary, I will print one key-value pair")
keys = list(train_data.keys())
id = 40000
key, value = keys[id], train_data[keys[id]]
print(f"Key: {key}")
print(f"Value: {value}")

print("\nStep 0.1.3 --> I skipped it because sample is not that big")

print("\nStep 0.2.1 --> value has a key 'Entity_set', I will print it")
entities = value["Entity_set"]
print(f"Entities: {entities}")
print(f"Type of entities: {type(entities)} of {type(entities[0])}")

print("\nStep 0.2.2 --> value has a key instead of Path and it's called 'Evidence'. This output I don't quite understand tho, there seems to be more than one relation between nodes?")
evidence = value["Evidence"]
print(f"Evidence: {evidence}")
print(f"Type: {type(evidence)}")

print("\nStep 0.3.1")
with open("factkg/dbpedia_2015_undirected_light.pickle", "rb") as f:
    graph = pickle.load(f)

print(type(graph))
print(len(graph))

print("\nStep 0.3.2")
# pick a random entity
entity = next(iter(graph.keys()))
print("Entity:", entity)

adj = graph[entity]
print(type(adj))
print(adj.keys())

rel = next(iter(adj.keys()))
print("Relation:", rel)
print("Neighbors:", list(adj[rel])[:5])

print("\nStep 0.4 --> relations is a list not a dictionary")
with open("factkg/relations_for_final.pickle", "rb") as f:
    relations = pickle.load(f)

print(type(relations))
print(len(relations))

# show first few
for k in relations[:10]:
    print(k)

print("\nStep 0.5")
e = entities[0]
print(e in graph)
