entries = []

def get_entries():
    return entries

def add_entry(entry):
    new_entry = {
        "id": len(entries) + 1,
        "name": entry.get("name"),
        "proteins": entry.get("proteins", 0),
        "fats": entry.get("fats", 0),
        "carbs": entry.get("carbs", 0),
        "calories": entry.get("calories", 0)
    }

    entries.append(new_entry)
    return new_entry