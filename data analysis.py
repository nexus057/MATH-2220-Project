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

# Labelled version (names as row/column headers), saved for reference
pd.DataFrame(A, index=people, columns=people).to_csv("adjacency_matrix.csv")

# ---- 3. Ask for the two people ----
you = input("Your name: ").strip()
recipient = input("Recipient's name: ").strip()

if you not in index or recipient not in index:
    raise SystemExit("One of those names isn't in the data.")

s, t = index[you], index[recipient]

# ---- 4. Degrees of separation via powers of A ----
# (A^k)[i, j] = number of walks of length k from person i to person j.
# The degree of separation is the smallest k with (A^k)[s, t] > 0.
# Column t of A^k is A^k e_t, which we build one step at a time:
#     A^k e_t = A (A^(k-1) e_t)
e_t = np.zeros(n, dtype=np.int64)
e_t[t] = 1
columns = [e_t]  # columns[k] = column t of A^k

distance = None
for k in range(n):
    if columns[k][s] > 0:
        distance = k
        break
    columns.append(A @ columns[k])

if distance is None:
    raise SystemExit("These two people aren't connected.")

# ---- 5. Recover a shortest path using the same columns ----
# From the current person, step to any friend m who still has a walk of
# length (remaining - 1) to the recipient.
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
