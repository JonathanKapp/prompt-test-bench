# We build this file together, one small piece at a time.

import csv
import json
import urllib.request

MODEL = "llama3.1:8b"
URL = "http://localhost:11434/api/generate"

def ask_model(prompt):
    data = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode()
    request = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read())
        return reply["response"]

with open("prompts/v1.txt") as f:
    template = f.read()

    with open("data/recipes.csv") as f:
        for row in csv.DictReader(f):
            prompt = template.replace("{recipe}", row["recipe"])
            answer = ask_model(prompt)
            print(row["recipe"], "->", answer)
            break
          