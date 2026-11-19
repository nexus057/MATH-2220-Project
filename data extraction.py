import pandas as pd

INPUT = "The Seven Degrees of Morse College c_o 2029 (Responses) - Form Responses 1.csv"
OUTPUT = "responses.csv"

df = pd.read_csv(INPUT)

# Find the respondent-name column and all the "Do you know ...?" columns
name_col = [c for c in df.columns if c.startswith("What is your full name")][0]
question_cols = [c for c in df.columns if c.startswith("Do you know ")]

# Clean respondent names; if someone submitted twice, keep their latest response
df["Respondent"] = df[name_col].astype(str).str.strip()
df = df.drop_duplicates("Respondent", keep="last")

# One row per (respondent, listed person)
long = df.melt(
    id_vars="Respondent",
    value_vars=question_cols,
    var_name="Person",
    value_name="Answer",
)

# "Do you know Jane Doe?" -> "Jane Doe"
long["Person"] = (
    long["Person"]
    .str.replace(r"^Do you know\s+", "", regex=True)
    .str.replace(r"\?\s*$", "", regex=True)
    .str.strip()
)

# Ticked ("I know this person.") -> 1, blank -> 0
long["Knows"] = (long["Answer"].fillna("").astype(str).str.strip() != "").astype(int)

# Drop rows where someone is paired with themselves
long = long[long["Respondent"] != long["Person"]]

long = long.sort_values(["Respondent", "Person"])
long[["Respondent", "Person", "Knows"]].to_csv(OUTPUT, index=False)

print("Respondents:", long["Respondent"].nunique())
print("People on the list:", long["Person"].nunique())
print("Rows written:", len(long))
print("Known (1s):", long["Knows"].sum())
