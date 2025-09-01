import requests
import pandas as pd

tournament_id = 357
season_id = 69619
headers = {
    "User-Agent": "Mozilla/5.0"
}

url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/top-players/overall"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Erreur HTTP {response.status_code} lors de la récupération des top joueurs.")
    exit(1)

data = response.json()

top_players_data = data.get("topPlayers", {})
if not top_players_data:
    print("Aucun top player trouvé dans la réponse.")
    exit(0)

stats_types = ["goals", "assists", "yellowCards", "redCards"]

rows = []
for stat in stats_types:
    for p in top_players_data.get(stat, []):
        player = p["player"]
        row = {
            "Player": player.get("name"),
            "Team": p["team"]["name"],
            "Position": player.get("position", ""),
            stat.capitalize(): p["statistics"].get(stat, 0)
        }
        rows.append(row)

df = pd.DataFrame(rows)

columns = ["Player", "Team", "Position"] + [s.capitalize() for s in stats_types]
df = df[columns]

output_file = f"club_world_cup_{season_id}_top_players.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")
