# Prompt Test Bench

A small tool that measures how well a prompt does one job, so it can be improved with evidence
instead of guesswork.

## The job being tested

Given a recipe, answer one question: **is it vegetarian? (yes / no)**

**The rule:** vegetarian means no meat, poultry, fish or seafood, and nothing made from them
(stock, gelatin, fish sauce, anchovies, lard). Eggs and dairy are fine.

## How it works

1. **Data:** `data/recipes.csv`, recipes with the correct answer already known.
2. **Prompt:** `prompts/v1.txt`, the instructions given to the model.
3. **Run:** `run.py` asks the model about each recipe and checks its answer.
4. **Results:** every run is saved in `results/`, and nothing is overwritten.

## Status

🚧 Just started. Built step by step.
