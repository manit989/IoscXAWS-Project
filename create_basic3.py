import json

def get_branch(prgname):
    prgname = prgname.upper()
    if "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING" in prgname:
        return "AIML"
    elif "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE" in prgname or "AIDS" in prgname:
        return "AIDS"
    elif "INTERNET OF THINGS" in prgname or "IIOT" in prgname:
        return "IIOT"
    elif "AUTOMATION AND ROBOTICS" in prgname or "AR" in prgname:
        return "AR"
    else:
        return "UNKNOWN"

def get_year(batch):
    year_map = {
        2021: 5,
        2022: 4,
        2023: 3,
        2024: 2,
        2025: 1,
    }
    return year_map.get(batch, 0)

with open("data.json", "r") as f:
    data = json.load(f)

result = []
for entry in data:
    result.append({
        "roll_number": str(entry["ROLLNO"]),
        "name": entry["STUDENT NAME"],
        "branch": get_branch(entry["PRGNAME"]),
        "year": get_year(entry["BATCH"]),
        "parent_name": entry["FATHER'S NAME"]
    })

with open("basic3.json", "w") as f:
    json.dump(result, f, indent=4)

print(f"Done. {len(result)} students written to basic3.json")