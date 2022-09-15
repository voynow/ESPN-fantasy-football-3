import json
import pandas as pd

from utils import configs


def load_master():

    return json.load(open(configs.master_loc, 'rb'))


def normalize(json_data):

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