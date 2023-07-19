import pandas as pd
import requests

# Download / Save local
r = requests.get('https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv')
with open(r'.\data\538th\2022-2023_data.csv', 'wb') as f:
    f.write(r.content)
    f.close()

# Display settings
pd.options.display.width = None
pd.options.display.max_columns = None

# Format Data
df = pd.read_csv(r'.\data\538th\2022-2023_data.csv')

df = df.drop(columns=['neutral', 'playoff', 'carm-elo1_pre', 'carm-elo2_pre', 'carm-elo_prob1',
                      'carm-elo_prob2', 'carm-elo1_post', 'carm-elo2_post'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

df = df.round({'elo1_pre': 1, 'elo2_pre': 1, 'elo_prob1': 2, 'elo_prob2': 2, 'elo1_post': 1,
               'elo2_post': 1, 'raptor1_pre': 1, 'raptor2_pre':1, 'raptor_prob1': 2, 'raptor_prob2': 2})

# Save the result
df.to_csv(r'.\data\538th\2022-2023_data.csv', index=False)