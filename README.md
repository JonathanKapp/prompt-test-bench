# Prompt Test Bench

A small Python tool that measures how well a prompt does one job, so prompts can be improved with
evidence instead of guesswork.

It runs a local LLM against a set of examples with known answers, scores every reply, and saves each
run so different prompts can be compared fairly.

## The job being tested

Given a recipe, answer one question: **is it vegetarian? (yes / no)**

**The rule:** vegetarian means no meat, poultry, fish or seafood, and nothing made from them
(stock, gelatin, fish sauce, anchovies, lard). Eggs and dairy are fine.

I chose this task because I'm a trained chef, so I could write and check the answer key myself.
It's also harder than it sounds: many recipes hide animal ingredients inside other ingredients
(Worcestershire sauce contains anchovies, marshmallows contain gelatin, dashi is made from fish).

## Results

Model: **Llama 3.1 8B** running locally through [Ollama](https://ollama.com), temperature 0 (so every
run is repeatable).

### Tuning set: 60 recipes (`data/recipes.csv`)

I improved the prompt while looking at these results.

| Prompt | What changed | Score |
|---|---|---|
| v1 | Short question, "answer yes or no" | 55/60 |
| v2 | Added "check each ingredient", but didn't define *vegetarian* | 52/60 |
| **v3** | **Defined vegetarian clearly: what's excluded, and that eggs and dairy are allowed** | **58/60** |
| v4 | v3 + "think step by step" (chain of thought) | 49/60 |
| v5 | v4 + extra rules | 46/60 scored (~51 real, see below) |

### Held-out set: 30 recipes the prompts had never seen (`data/heldout.csv`)

This is the fair test, because no prompt was tuned against these recipes.

| Prompt | Score |
|---|---|
| v1 | 25/30 |
| **v3** | **28/30** |

**v3 beats v1 on unseen recipes.**

## What I found

1. **Defining your terms matters most.** v2 used the word "non vegetarian" without defining it, and
   the model decided eggs weren't vegetarian. It scored *lower* than the plain v1. v3 spelled out the
   rule and scored best on both sets.
2. **Chain of thought made this 8B model worse, not better (58 → 49).** The saved raw replies show
   why: it became over-cautious ("pastry might contain lard" → no), invented facts ("butter is made
   from animal fat"), and sometimes gave an answer that contradicted its own reasoning. It was also
   about 10x slower.
3. **Some "wrong" answers were measurement errors, not model errors.** With v5, the model wrote things
   like `Final answer: no`, which my answer-reader couldn't parse. Five correct answers were scored as
   wrong. Saving the raw reply is what made this visible.
4. **The remaining mistakes are knowledge gaps, not reasoning gaps.** On the held-out set, v3 missed
   only two recipes: Vietnamese spring rolls (the dipping sauce, nuoc cham, contains fish sauce) and
   trifle (jelly contains gelatin). Both are the risky kind of mistake, saying "vegetarian" when it
   isn't. Better wording can't fix these, because the model doesn't know what's in those ingredients.

## How it works

1. **Data:** a CSV of recipes, each with the correct answer.
2. **Prompt:** a text file with a `{recipe}` placeholder.
3. **Run:** `run.py` fills in each recipe, asks the model, reads the yes/no, and compares it to the
   correct answer.
4. **Results:** every run is saved as a JSON file in `results/` (the settings, the score, and the
   model's raw reply for every recipe). Nothing is overwritten.

## Run it yourself

You need Python 3 and [Ollama](https://ollama.com). No other packages are needed.

```bash
ollama pull llama3.1:8b
python3 run.py
```

Choose the prompt and the recipe list with the settings at the top of `run.py`:

```python
MODEL = "llama3.1:8b"
PROMPT_FILE = "prompts/v3.txt"
DATA_FILE = "data/heldout.csv"
```

## Project layout

```
data/recipes.csv    60 recipes used while improving the prompt
data/heldout.csv    30 recipes kept aside for the final test
prompts/            prompt versions v1 to v5
results/            one JSON file per run
run.py              the test bench
```

## What's next

- **v2 of this project: retrieval (RAG).** Since the remaining mistakes are about hidden ingredients,
  the next step is to look up facts about each recipe's ingredients and give them to the model,
  then use this same test bench to measure whether that actually helps.
- Compare a smaller model (Llama 3.2 3B) to see how much model size matters.
- Use Ollama's structured output so the answer-reader can't misread replies.
