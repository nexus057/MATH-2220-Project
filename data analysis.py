import numpy as np
import pandas as pd

data = pd.read_csv("responses.csv")
data["Respondent"] = data["Respondent"].astype(str).str.strip()
data["Person"] = data["Person"].astype(str).str.strip()

people = sorted(set(data["Respondent"]) | set(data["Person"]))
index = {person: i for i, person in enumerate(people)}
n = len(people)

known = data[data["Knows"] == 1]
rows = known["Respondent"].map(index).to_numpy()
cols = known["Person"].map(index).to_numpy()

A = np.zeros((n, n), dtype=np.int64)
A[rows, cols] = 1
A[cols, rows] = 1
np.fill_diagonal(A, 0)

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
