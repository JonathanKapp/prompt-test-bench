# We build this file together, one small piece at a time.

import csv
import json
import urllib.request
from datetime import datetime

MODEL = "llama3.1:8b"
PROMPT_FILE = "prompts/v4.txt"
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

with open("data/recipes.csv") as f:
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
            answers.append({"recipe": row["recipe"], "answer": answer, "expected": expected, "result": result, "raw": raw})

                  
print(f"\nScore: {correct}/{total}") 

now = datetime.now()
run = {
    "time": now.isoformat(timespec="seconds"),
    "model": MODEL,
    "prompt_file": PROMPT_FILE,
    "temperature": TEMPERATURE,
    "score": correct,
    "total": total,
    "answers": answers,
}

filename = "results/" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
with open(filename, "w") as f:
     json.dump(run, f, indent=2)

print("Saved to", filename)
     