import requests
import pandas as pd

tournament_id = 357
season_id = 69619
headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}

url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/top-teams/overall"
res = requests.get(url, headers=headers)

if res.status_code != 200:
    print(f" Erreur HTTP {res.status_code} pour top teams")
    exit(1)

data = res.json()
teams_data = data.get("topTeams", {})

rows = []
for stat, stat_list in teams_data.items():
    for t in stat_list:
        team = t.get("team", {})
        row = {
            "Team": team.get("name"),
            "Team_id": team.get("id"),
            "StatType": stat,
            "Value": t.get("statistics", {}).get(stat, None)
        }
        rows.append(row)

df = pd.DataFrame(rows)

df_pivot = df.pivot_table(index=["Team", "Team_id"], columns="StatType", values="Value", aggfunc="first").reset_index()

output = f"club_world_top_teams_{season_id}.xlsx"
df_pivot.to_excel(output, index=False, engine="openpyxl")
