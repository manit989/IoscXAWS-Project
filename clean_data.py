import json

with open("data.json", "r") as f:
    data = json.load(f)

clean_data = [
    {
        "username": str(entry["ROLLNO"]),
        "password": entry["FATHER'S NAME"]
    }
    for entry in data
]

with open("clean_data.json", "w") as f:
    json.dump(clean_data, f, indent=4)

print(f"Done. {len(clean_data)} records written to clean_data.json")