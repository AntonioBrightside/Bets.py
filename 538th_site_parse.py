from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import re


# Get-requset function
def connection(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup


# Get-request
URL = 'https://projects.fivethirtyeight.com/2023-nba-predictions/games/?ex_cid=rrpromo'
soup = connection(URL)

# Making dictionary to standartify teams names
TEAMS = {'Celtics': 'BOS', 'Bucks': 'MIL', 'Hawks': 'ATL', 'Cavaliers': 'CLE',
         'Wizards': 'WAS', 'Raptors': 'TOR', 'Knicks': 'NY', '76ers': 'PHI',
         'Pacers': 'IND', 'Heat': 'MIA', 'Bulls': 'CHI', 'Nets': 'BRK', 'Magic': 'ORL',
         'Hornets': 'CHO', 'Pistons': 'DET', 'Trail Blazers': 'POR', 'Nuggets': 'DEN',
         'Jazz': 'UTA', 'Suns': 'PHO', 'Mavericks': 'DAL', 'Grizzlies': 'MEM',
         'Pelicans': 'NOP', 'Kings': 'SAC', 'Clippers': 'LAC', 'Timberwolves': 'MIN',
         'Thunder': 'OKC', 'Warriors': 'GSW', 'Spurs': 'SAS', 'Lakers': 'LAL', 'Rockets': 'HOU'}

# Trying to understand what data we should gather and join with main DataSet
for h3 in soup.find('h3'):
    date_tag = h3.text + ', 2022'
    try:
        date = datetime.datetime.strptime(date_tag, '%A, %b. %d, %Y').date()
    except ValueError:
        pass

# Gathering the data
data_teams = []
data_spread = []

for game in soup.find('div', attrs={'class': 'games-section extra-space-0'}).find_all(attrs={'class': 'tr team'}):
    for team in TEAMS.keys():
        if re.match(team, game.text):
            data_teams.append(TEAMS.get(team))

for spread in soup.find('div', attrs={'class': 'games-section extra-space-0'}).find_all(attrs={'class': 'td number spread'}):
    data_spread.append(spread.text)

# Join the data
data = []

if len(data_teams) == len(data_spread):

    start = 0
    finish = 2
    for num in range(int(len(data_teams) / 2)):
        data.append(data_teams[start:finish])
        start += 2
        finish += 2

    counter = 0
    start = 0
    finish = 2
    for num in range(int(len(data_spread) / 2)):
        for i in data_spread[start:finish]:
            data[counter].append(i)
        counter += 1
        start += 2
        finish += 2

    counter = 0
    for num in range(len(data)):
        data[num].insert(0, date)

else:
    print('Something went wrong. Check the dictionary')

# Creating DF
df = pd.DataFrame(data=data,
                         columns=['date', 'team 2', 'team 1', 'spread team 2', 'spread team 1'])

# Saving as file
df.to_csv(r'.\data\538th\spread_data.csv', index=False)

print(df)