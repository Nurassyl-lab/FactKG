import pickle

with open("factkg/relations_for_final.pickle", "rb") as f:
    relations = pickle.load(f)

print(f"type(relations): {type(relations)}")

with open('relations.txt', 'w') as f:
    f.write('\n'.join(relations))