import json

with open("user2.json", "w") as f:
    json.dump({"name": "Tom", "age": 20}, f, indent=4, ensure_ascii=False)
