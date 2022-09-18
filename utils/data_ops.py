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

    dfs = {}

    for player, data in json_data.items():
        pos = data['pos']

        for key in data:
            year = key.split("_")[0]

            if year.isnumeric() and len(year) == 4:
                df = pd.DataFrame(data[key])
                df['player'] = player
                df['year'] = year

                if pos in dfs:
                    dfs[pos].append(df)
                else:
                    dfs[pos] = [df]

    for key in dfs:
        dfs[key] = pd.concat(dfs[key])

    return dfs