# We build this file together, one small piece at a time.

import csv

with open("prompts/v1.txt") as f:
    template = f.read()

    with open("data/recipes.csv") as f:
        for row in csv.DictReader(f):
            prompt = template.replace("{recipe}", row["recipe"])
            print(prompt)
            print("---")