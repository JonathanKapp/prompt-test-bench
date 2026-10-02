# We build this file together, one small piece at a time.

import csv

with open("data/recipes.csv") as f:
    for row in csv.DictReader(f):
        print(row["recipe"], "->", row["vegetarian"])
        