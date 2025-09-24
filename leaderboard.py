import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # מיון מהגבוה לנמוך
            data.sort(key=lambda x: x["score"], reverse=True)
            return data
        except:
            return []

def save_leaderboard(entries):
    # מיון מהגבוה לנמוך
    entries.sort(key=lambda x: x["score"], reverse=True)
    entries = entries[:20]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

def add_score(name, score):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score})
    save_leaderboard(entries)
