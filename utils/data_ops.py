import json
import pandas as pd

from utils import configs


def normalize(json_data):
    """
    Update data structure where data tables are brought to top level 
    """
    for player, obj in json_data.items():

        # bring header attributes to top level
        for key, value in json_data[player]['data']['header'].items():
            json_data[player][key] = value

        # remove header object
        del json_data[player]['data']['header']

        # bring dataset keys to top level
        for dataset, data in obj['data'].items():
            json_data[player][dataset] = data

        # remove data object
        del json_data[player]['data']

    return json_data


def load():
    """
    Load master dataset with tables names accessible by dictionary key
    """
    f_open = open(configs.master_loc, 'rb')
    return normalize(json.load(f_open))


def join_players(json_data):
    """
    Join game statistics partitioned by position
    """
    dfs = {}
    for player, data in json_data.items():
        pos = data['pos']

        for key in data:
            year = key.split("_")[0]

            if year.isnumeric() and len(year) == 4:
                df = pd.DataFrame(data[key])
                df['player'] = player
                df['year'] = int(year)

                if pos in dfs:
                    dfs[pos].append(df)
                else:
                    dfs[pos] = [df]

    for key in dfs:
        dfs[key] = pd.concat(dfs[key])

    return dfs


def get_schedule(week_num):
    """
    Transforming schedule copied from https://www.fftoday.com/nfl/schedule.php
    """
    data_path = 'data/2022_schedule.csv'

    schedule = []
    for row in open(data_path, 'r').readlines():

        remove_strings = "\n", " â¹", " *"
        for string in remove_strings:
            row = row.replace(string, "")
        row = row.split(",")

        if 'Week' in row[0]:
            schedule.append([])
        else:
            schedule[-1].append(row)

    for i, week in enumerate(schedule):
        if i == week_num - 1:
            df = pd.DataFrame(week[1:]).iloc[:, :4]
            df.columns = week[0]
            for col in ["Away Team", "Home Team"]:
                df[col] = df[col].apply(lambda x: x.lower() if x else x)
                df[col] = df[col].apply(lambda x: configs.team_abbreviation_map[x] if x else x)
            return df

def get_opponent_strength(dfs, season=2022, weeks=None):
    """
    Group data by position & opponent and exctact statistics for points scored
    The resulting dataframe can identify strength of an opponen for all positions
    """    
    opp_strength_all_positions = {}
    opp_strength_cols = ["opp", "fpts/g", "std", "var", "min", "max"]

    for pos in dfs:
        df = dfs[pos]
        df_year = df[df['year'] == season]
        if weeks:
            df_year = df_year[df_year['week'].apply(lambda x: int(x) in weeks)]
        df_year['opp'] =  df_year['opp'].apply(lambda x: x.replace("@", ""))

        opp_strength = {col: [] for col in opp_strength_cols}

        for opp, group in df_year.groupby('opp'):

            fpts = group.groupby('week').sum()['fpts']

            opp_strength['opp'].append(opp)
            opp_strength['fpts/g'].append(fpts.mean().round(3))
            opp_strength['std'].append(fpts.std().round(3))
            opp_strength['var'].append(fpts.var().round(3))
            opp_strength['min'].append(fpts.min())
            opp_strength['max'].append(fpts.max())

        opp_strength_all_positions[pos] = pd.DataFrame(opp_strength).sort_values(by='fpts/g', ascending=False).reset_index()

    return opp_strength_all_positions