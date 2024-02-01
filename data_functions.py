import pybaseball as pb
import pandas as pd
import os
from tqdm import tqdm

DEFAULT_START_YEAR = 2015
DEFAULT_END_YEAR = 2023
MINIMUM_PA = 300

# Get batter data for the model, minimum 300 PA
def get(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR, exclude_2020=True, force_update=False):
    if not os.path.exists('data'):
        os.mkdir('data')

    for season in tqdm(range(start_year, end_year+1), desc='Getting data'):
        if season == 2020 and exclude_2020:
            continue
        
        if os.path.exists(f'data/batting_{season}.csv') and not force_update:
            continue

        data = pb.batting_stats(season, qual=MINIMUM_PA, ind=1)
        data.to_csv(f'data/batting_{season}.csv')

# Load batter data for the model
def load(start_year=DEFAULT_START_YEAR, end_year=DEFAULT_END_YEAR):
    data = pd.DataFrame()

    all_data = {}
    for season in range(start_year, end_year+1):
        try:
            all_data[season] = pd.read_csv(f'./data/batting_{season}.csv')
        except FileNotFoundError:
            continue

    for season in tqdm(range(start_year+1, end_year+1), desc='Loading data'):
        prior = all_data.get(season-1)
        current = all_data.get(season)

        if prior is None or current is None:
            continue

        merged_data = pd.merge(prior, current, on='Name', suffixes=('_prev', '_curr'))
        data = pd.concat([data, merged_data], ignore_index=True)

    return data