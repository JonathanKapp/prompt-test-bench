# We build this file together, one small piece at a time.

import csv
import json
import urllib.request

MODEL = "llama3.1:8b"
URL = "http://localhost:11434/api/generate"

def ask_model(prompt):
    data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0}}).encode()
    request = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read())
        return reply["response"]

def clean(answer):
    answer = answer.strip().lower()
    if answer.startswith("yes"):
        return "yes"
    if answer.startswith("no"):
        return answer
    

with open("prompts/v1.txt") as f:
    template = f.read()

correct = 0
total = 0 

with open("data/recipes.csv") as f:
        for row in csv.DictReader(f):
            prompt = template.replace("{recipe}", row["recipe"])
            answer = clean(ask_model(prompt))
            expected = row["vegetarian"]
            total += 1
            if answer == expected:
                 correct += 1
                 result = "RIGHT"
            else:
                 result = "WRONG"
            print(f"{result} {row['recipe']} -> model: {answer}, expected: {expected}")
                  
print(f"\nScore: {correct}/{total}") 
          