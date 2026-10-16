import pickle
import os
import random

path = "factkg/factkg_train.pickle"
# path = "factkg/dbpedia_2015_undirected_light.pickle"

with open(path, 'rb') as f:
    data = pickle.load(f)

print("==========================================")
print(f"5 Random samples from {path}")
for i in range(5):
    sample_key = list(data.keys())[random.randint(0, len(data.keys()))]
    sample = data[sample_key]
    print("Random sample key:", sample_key, "Sample Statement:", sample, "\n", sep="\n")
print("==========================================")

# * How many entities appear in more than 1 type of Factual Claims
# entities = {}
# keys = list(data.keys())
# for key in keys:
#     sample = data[key]
#     entity_set = sample["Entity_set"]
#     type = sample["types"]
#     for entity in entity_set:

