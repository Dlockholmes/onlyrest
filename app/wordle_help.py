import json

n = input()

output = []

with open("dictionary data/wordlist_help") as f:
    data = json.loads(f.read())
    for i in data:
        is_al = True
        i = i.lower()
        for idx,j in enumerate(i):
            if(n[idx]=="?"): continue
            if(n[idx]!=j): is_al=False
        if(is_al): output.append(i)

print(output)