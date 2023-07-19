from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import pytz


# Split data to nested lists to make rows further
def data_maker(data, length, denominator):
    rows = []
    start = 0
    func_finish = denominator
    func_length = length

    for i in range(int(func_length / denominator)):
        rows.append(data[start:func_finish])
        start = func_finish
        func_finish += denominator
    return rows


# Change RUS name of a team to ENG
def team_changer(data):
    counter = 0
    for team in data:
        data.loc[counter] = TEAMS.get(team)
        counter += 1


# Remove specific symbols from rows
def replacer(data, to_replace):
    counter = 0
    if isinstance(to_replace, tuple) | isinstance(to_replace, list):
        for row in data:
            for i in to_replace:
                if i in data.loc[counter]:
                    data.loc[counter] = data.loc[counter].replace(i, '')
            counter += 1
    else:
        for row in data:
            data.loc[counter] = data.loc[counter].replace(to_replace, '')
            counter += 1


# Get-request
NBA_URL = 'https://www.1mbet.win/su/popular/Basketball/NBA+-+69367'
req = requests.get(NBA_URL)
soup = BeautifulSoup(req.text, 'html.parser')

# Collect data
teams = []
numbers = []
dates = []
headers = []
coefficients_raw = []
raw = []
coefficients = []

# Scrapping the teams
for team in soup.find_all('a', attrs={'class': 'member-link'}):
    for character in ['\n']:
        team = team.text.replace(character, '')
        teams.append(team)

teams_split = data_maker(data=teams, length=len(teams), denominator=2)

# Scrapping the teams numbers (Don't use it 'cause useless)
for number in soup.find_all('b', attrs={'class': 'member-number'}):
    for character in ['.']:
        number = number.text.replace(character, '')
        numbers.append(number)

# Scrapping the date of game (IT ONLY WORKS IN 1 CASE!)
for i in soup.find_all('table', attrs={'class': 'member-area-content-table'}):
    if 'маржа' in i.text:
        for date in i.find('td', attrs={'class': 'date date-with-month'}):
            for character in ['\n']:
                date = date.text.replace(character, '')
                date = date.strip()
                dates.append(date)
    else:
        for date in i.find_all('td', attrs={'class': 'date date-short'}):
            for character in ['\n']:
                date = date.text.replace(character, '')
                date = date.strip()
                dates.append(date)

dates_split = data_maker(data=dates, length=len(dates), denominator=1)

# Scrapping the headers
for row in soup.find(attrs={'class': 'coupon-row-item'}).find_all('th'):
    for th in row.find_all('div', attrs={'class': 'tooltip'}):
        for character in ['\n']:
            th = th.text.replace(character, '')
            th = th.strip()
            headers.append(th)

headers.insert(0, 'Гостевая команда')
headers.insert(1, 'Домашняя команда')
headers.insert(2, 'Дата матча')
headers.insert(5, 'Фора Г')
headers.insert(7, 'Фора Д')
headers.insert(9, 'Очки')
headers.insert(11, 'Очки_DEL')

# Scrapping the coefficients
for row in soup.find_all('tr', attrs={'class': 'sub-row'}):
    for cell in row:
        for character in ['\n']:
            cell = cell.text.replace(character, '')
        if cell == '':
            pass
        else:
            cell = cell.strip()
            raw.append(cell)
    coefficients_raw.append(raw)
    raw = []

[coefficients.append(lst[2:]) for lst in coefficients_raw]
coefficients_raw = []

for i in coefficients:
    for cell in i:
        new_cell = cell.split()
        for splitted in new_cell:
            coefficients_raw.append(splitted)

coefficients_split = data_maker(data=coefficients_raw, length=len(coefficients_raw), denominator=10)

# Join data in rows
rows = []

for i in range(int(len(teams_split))):
    rows.append(teams_split[i] + dates_split[i] + coefficients_split[i])

# Create DataFrame
pd.options.display.width = None
pd.options.display.max_columns = None

df = pd.DataFrame(data=rows, columns=headers)

# Create dictionaries
TEAMS = {'Милуоки Бакс': 'MIL', 'Бостон Селтикс': 'BOS', 'Атланта Хокс': 'ATL', 'Кливленд Кавальерс': 'CLE',
         'Вашингтон Уизардс': 'WAS', 'Индиана Пэйсерс': 'IND', 'Торонто Рэпторс': 'TOR', 'Филадельфия 76-е': 'PHI',
         'Майами Хит': 'MIA', 'Нью-Йорк Никс': 'NYK', 'Бруклин Нетс': 'BRK', 'Чикаго Буллз': 'CHI',
         'Орландо Мэджик': 'ORL', 'Детройт Пистонс': 'DET', 'Шарлотт Хорнетс': 'CHO', 'Денвер Наггетс': 'DEN',
         'Портленд Трэйл Блэйзерс': 'POR', 'Финикс Санз': 'PHO', 'Юта Джаз': 'UTA', 'Мемфис Гриззлис': 'MEM',
         'Даллас Маверикс': 'DAL', 'Лос-Анджелес Клипперс': 'LAC', 'Нью-Орлеан Пеликанс': 'NOP',
         'Сакраменто Кингз': 'SAC', 'Оклахома-Сити Тандер': 'OKC', 'Сан-Антонио Сперс': 'SAS',
         'Миннесота Тимбервулвз': 'MIN', 'Голден Стэйт Уорриорз': 'GSW', 'Лос-Анджелес Лейкерс': 'LAL',
         'Хьюстон Рокетс': 'HOU'}

MONTHS = {'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04', 'май': '05', 'июн': '06',
          'июл': '07', 'авг': '08', 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}

# Format DataFrame
df = df.drop(columns='Очки_DEL')
df = df.set_axis(['team 2', 'team 1', 'Date MSK', 'WIN 2', 'WIN 1',
                  'Handicap 2', 'Coef. Handicap 2', 'Handicap 1', 'Coef. Handicap 1',
                  'Game points', '< Game points', '> Game points'], axis=1, inplace=False)

team_changer(df['team 2'])
team_changer(df['team 1'])

replacer(data=df['Handicap 2'], to_replace=('(', ')'))
replacer(data=df['Handicap 1'], to_replace=['(', ')'])
replacer(data=df['Game points'], to_replace=['(', ')'])

# Convert MSK date into Date Eastern
nested_counter = 0
counter = 0
eastern_time = pytz.timezone('US/Eastern')
df['Date Eastern'] = ''

for i in df['Date MSK']:
    ex = df['Date MSK'].loc[counter].split()
    for a in ex:
        if a in MONTHS:
            ex[nested_counter] = MONTHS.get(a)
        elif nested_counter == 2:
            ex.insert(2, str(datetime.date.today().year))

        nested_counter += 1
    nested_counter = 0
    date = '{}-{}-{} {}'.format(ex[0], ex[1], ex[2], ex[3])
    date = datetime.datetime.strptime(date, '%d-%m-%Y %H:%M')
    df['Date Eastern'].loc[counter] = date.astimezone(eastern_time).date()
    counter += 1

# Format data 2
df['Date Eastern'] = pd.to_datetime(df['Date Eastern'], format='%Y-%m-%d')
df['WIN 2'] = df['WIN 2'].astype('float')
df['WIN 1'] = df['WIN 1'].astype('float')
df['Coef. Handicap 2'] = df['Coef. Handicap 2'].astype('float')
df['Coef. Handicap 1'] = df['Coef. Handicap 1'].astype('float')
df['Game points'] = df['Game points'].astype('float')
df['< Game points'] = df['< Game points'].astype('float')
df['> Game points'] = df['> Game points'].astype('float')

# Saving data in *csv
df.to_csv(r'.\data\marathon data\marathon_data_{}.csv'.format(datetime.datetime.now().date()), index=False)