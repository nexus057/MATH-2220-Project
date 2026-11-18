import pandas as pd
import re

df = pd.read_csv("responses.csv")

print(df.columns.tolist())

respondent_col = df.columns[2]
question_cols = df.columns[3:]

def get_person_name(question):
    question = str(question)

    name = re.sub(
        r"^Do you know\s*",
        "",
        question,
        flags=re.IGNORECASE
    )

    return name.rstrip(" ?")

relationships = []

for _, row in df.iterrows():

    respondent = row[respondent_col]

    if pd.isna(respondent):
        continue

    for question in question_cols:

        response = row[question]
        target = get_person_name(question)

        if pd.isna(response) or str(response).strip() == "":
            continue

        relationships.append({
            "Person 1": respondent,
            "Person 2": target,
            "Response": response
        })

relationships_df = pd.DataFrame(relationships)

print(relationships_df)

relationships_df.to_csv(
    "relationships.csv",
    index=False
)
