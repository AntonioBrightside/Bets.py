import pandas as pd
import datetime

# Display settings
pd.options.display.width = None
pd.options.display.max_columns = None

# Load data
df_538th = pd.read_csv(r'.\data\538th\2022-2023_data.csv')
df_bets = pd.read_csv(r'.\data\marathon data\marathon_data_{}.csv'.format(datetime.datetime.now().date()))
df_spread = pd.read_csv(r'.\data\538th\spread_data.csv')

# Format dates
df_538th['date'] = pd.to_datetime(df_538th['date'], format='%Y-%m-%d')
df_bets['Date Eastern'] = pd.to_datetime(df_bets['Date Eastern'], format='%Y-%m-%d')
df_spread['date'] = pd.to_datetime(df_spread['date'], format='%Y-%m-%d')

# Drop useless data
df_538th = df_538th.drop(columns=['elo1_pre', 'elo2_pre',
                                  'elo1_post', 'elo2_post',
                                  'raptor1_pre', 'raptor2_pre'])

# Join the DF's and clear resulting data
df = df_538th.merge(df_bets, left_on=['date', 'team1', 'team2'], right_on=['Date Eastern', 'team 1', 'team 2'])
df = df.drop(columns=['team 2', 'team 1', 'Date MSK', 'Date Eastern'])
df = df.merge(df_spread, how='inner', left_on=['date', 'team1', 'team2'], right_on=['date', 'team 1', 'team 2'])
df = df.drop(columns=['team 2', 'team 1'])

# Making back up of saving data
df.to_csv(r'.\data\NBA_data back ups\NBA_data_{}.csv'.format(datetime.datetime.now().date()), index=False)

# Check new recorded data for duplicates in saved file and save gathered data
try:
    NBA_data = pd.read_csv(r'.\data\NBA_data.csv')
    NBA_data['date'] = pd.to_datetime(NBA_data['date'], format='%Y-%m-%d')
    if df['date'].loc[int(len(df['date']) - 1)] == NBA_data['date'].loc[int(len(NBA_data['date']) - 1)]:
        print('The data exist. Do not copy in main file')
        exit()
    elif df['date'].loc[int(len(df['date']) - 1)] != NBA_data['date'].loc[int(len(NBA_data['date']) - 1)]:
        NBA_data = pd.concat([NBA_data, df], ignore_index=True)
        print('The data does not exit. Copying data in main file ')
        NBA_data.to_csv(r'.\data\NBA_data.csv', index=False)
    else:
        print('----Unable term. Should check the code---')

except FileNotFoundError:
    df.to_csv(r'.\data\NBA_data.csv', index=False)