# Prompt Test Bench: runs a prompt against recipes with known answers and scores the model.

import csv
import json
import urllib.request
from datetime import datetime

MODEL = "llama3.1:8b"
PROMPT_FILE = "prompts/v3.txt"
DATA_FILE = "data/hard.csv"
TEMPERATURE = 0
URL = "http://localhost:11434/api/generate"

def ask_model(prompt):
    data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0}}).encode()
    request = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read())
        return reply["response"]

def clean(answer):
    lines = answer.strip().lower().splitlines()
    last = lines[-1].strip(" *.:")
    if last.startswith("yes"):
        return "yes"
    if last.startswith("no"):
        return "no"
    return last

    
with open(PROMPT_FILE) as f:
    template = f.read()

correct = 0
total = 0 
answers = []
group_total = {}
group_correct = {}

with open(DATA_FILE) as f:
        for row in csv.DictReader(f):
            prompt = template.replace("{recipe}", row["recipe"])
            raw = ask_model(prompt)
            answer = clean(raw)
            expected = row["vegetarian"]
            total += 1
            if answer == expected:
                 correct += 1
                 result = "RIGHT"
            else:
                 result = "WRONG"
            print(f"{result} {row['recipe']} -> model: {answer}, expected: {expected}")
            group = row.get("type", "all")
            group_total[group] = group_total.get(group, 0) + 1
            if answer == expected:
                group_correct[group] = group_correct.get(group, 0) + 1
            answers.append({"recipe": row["recipe"], "answer": answer, "expected": expected, "result": result, "raw": raw})

                  
print(f"\nScore: {correct}/{total}") 
for group in group_total:
     print(f" {group}: {group_correct.get(group, 0)}/{group_total[group]}")

now = datetime.now()
run = {
    "time": now.isoformat(timespec="seconds"),
    "model": MODEL,
    "prompt_file": PROMPT_FILE,
    "data_file": DATA_FILE,
    "temperature": TEMPERATURE,
    "score": correct,
    "total": total,
    "answers": answers,
}

filename = "results/" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
with open(filename, "w") as f:
     json.dump(run, f, indent=2)

print("Saved to", filename)
     