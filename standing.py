import requests
import pandas as pd


url = "https://www.sofascore.com/api/v1/unique-tournament/357/season/69619/standings/total"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://www.sofascore.com/"
}

response = requests.get(url, headers=headers)
data = response.json()


all_standings = []


for group in data['standings']:
    group_name = group.get('name', 'Unknown Group')
    for team in group['rows']:
        team_info = team['team']
        stats = {
            'Group': group_name,
            'Position': team.get('position'),
            'Team Name': team_info.get('name'),
            'Country': team_info.get('country', {}).get('name'),
            'Games Played': team.get('matches'),
            'Wins': team.get('wins'),
            'Draws': team.get('draws'),
            'Losses': team.get('losses'),
            'Goals For': team.get('scoresFor'),
            'Goals Against': team.get('scoresAgainst'),
            'Goal Diff': team.get('scoresFor') - team.get('scoresAgainst'),
            'Points': team.get('points')
        }
        all_standings.append(stats)


df = pd.DataFrame(all_standings)


df.to_csv("all_groups_standings.csv", index=False, encoding='utf-8-sig')

