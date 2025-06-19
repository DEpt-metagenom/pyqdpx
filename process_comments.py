import json

with open('comments.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

print(data['NaCOO9zdSBk'])