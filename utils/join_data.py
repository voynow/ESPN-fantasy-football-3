import json
import urllib

from utils import configs


def join_data():
    """
    Load previous years data and join with current data
    save as json in data folder
    """
    master_data = json.loads(urllib.request.urlopen(configs.historical_data_url).read())
    live_data = json.load(open(configs.structured_loc, 'rb'))

    for player in live_data:
        if player in master_data:
            master_data[player]['data']['2022_gamelog_stats'] = live_data[player]['data']['2022_gamelog_stats']
        else:
            master_data[player] = live_data[player]

    with open(configs.master_loc, "w") as f:
        json.dump(master_data, f, indent=4)