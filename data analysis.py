import numpy as np
import pandas as pd

data = pd.read_csv("relationships.csv", usecols=[0, 1])
data.columns = ["Person1", "Person2"]
data = data.dropna()
data["Person1"] = data["Person1"].astype(str).str.strip()
data["Person2"] = data["Person2"].astype(str).str.strip()
data = data[
    (data["Person1"] != "")
    & (data["Person2"] != "")
    & (data["Person1"] != data["Person2"])
]
people = sorted(set(data["Person1"]) | set(data["Person2"]))
index = {person: i for i, person in enumerate(people)}
n = len(people)

A = np.zeros((n, n), dtype=np.int64)
rows = data["Person1"].map(index).to_numpy()
cols = data["Person2"].map(index).to_numpy()
A[rows, cols] = 1
A[cols, rows] = 1

pd.DataFrame(A, index=people, columns=people).to_csv("adjacency_matrix.csv")

# ---- Ask for the two people ----
person1 = input("Your name: ").strip()
person2 = input("Recipient's name: ").strip()

if person1 not in index or person2 not in index:
    raise SystemExit("One of those names isn't in the data.")

s, t = index[person1], index[person2]

# ---- Degrees of separation via powers of A ----
e_t = np.zeros(n, dtype=np.int64)
e_t[t] = 1
columns = [e_t]

distance = None
for k in range(n):
    if columns[k][s] > 0:
        distance = k
        break
    columns.append(A @ columns[k])

if distance is None:
    raise SystemExit("These two people aren't connected.")

# ---- Recover a shortest path using the same columns ----
path = [s]
current = s
for remaining in range(distance, 0, -1):
    for m in np.flatnonzero(A[current]):
        if columns[remaining - 1][m] > 0:
            current = m
            path.append(m)
            break

print("Degrees of separation:", distance)
print("Shortest path:", " -> ".join(people[p] for p in path))
print("Number of shortest paths:", columns[distance][s])
