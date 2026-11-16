
import pandas as pd
import re

# Read the Google Forms responses
df = pd.read_csv("responses.csv")

# Inspect the actual column headers
print(df.columns.tolist())

# Based on your screenshot:
# Column C = respondent's name
# Column D onwards = questions about other people

respondent_col = df.columns[2]
question_cols = df.columns[3:]

# Extract the person's name from each question header
def get_person_name(question):
    question = str(question)

    # Removes the common question prefix
    name = re.sub(
        r"^Do you know\s*",
        "",
        question,
        flags=re.IGNORECASE
    )

    return name.rstrip(" ?")

# Convert wide-format data into long-format data
relationships = []

for _, row in df.iterrows():

    respondent = row[respondent_col]

    if pd.isna(respondent):
        continue

    for question in question_cols:

        response = row[question]
        target = get_person_name(question)

        # Ignore empty responses
        if pd.isna(response) or str(response).strip() == "":
            continue

        relationships.append({
            "Person 1": respondent,
            "Person 2": target,
            "Response": response
        })

# Create a new DataFrame
relationships_df = pd.DataFrame(relationships)

print(relationships_df)

# Export the extracted relationships
relationships_df.to_csv(
    "relationships.csv",
    index=False
)
