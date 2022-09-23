import json
from utils import extract, configs
import urllib


def split_on_newline(raw_data):
    """
    Utility function for data preparation
    split raw text on newline characters - semistructuring the text objects
    """
    for key in raw_data:
        raw_data[key] = raw_data[key].replace("\n\n\n", "\n\n")
        raw_data[key] = raw_data[key].split("\n\n")

    for key in raw_data:
        data_split = []
        for item in raw_data[key]:
            data_split.append(item.split("\n"))
        raw_data[key] = data_split

    return raw_data


def prep_raw_data(raw_loc):
    """
    Open raw json and collect data relevant for transformation
    """
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    raw_data = split_on_newline(raw_data)
    return master_raw_data, raw_data


def group(data):
    """
    Separate raw data into groups defined in configs.table_names
    header group accessed by index (0th and 2nd row of raw data)
    other groups accessed by string search
    """
    table_names = configs.table_names
    
    player_dict = {}
    player_dict[table_names[0]] = data[0] + data[2]

    for row in data:
        for string in table_names:
            if row[0] == string:
                string_key = string.replace(" ", "_").lower()
                player_dict[string_key] = row
    
    return player_dict


def transformation_pipeline():

    # raw data preprocessing
    master_raw_data, raw_data = prep_raw_data(configs.raw_loc)

    # transformations
    for k, data in raw_data.items():
        grouped_data = group(data)
        for group_name in grouped_data:
            transformation = configs.function_map[group_name]
            grouped_data = transformation(grouped_data)
            raw_data[k] = grouped_data

    # restructuring
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    return master_raw_data


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

    return master_data


def transform():
    """
    Pipeline for facilitating data tranformation of raw text/json data into 
    a structured josn format, where table-like structures begin to emerge
    """

    transformed_data = transformation_pipeline()
    with open(configs.structured_loc, "w") as f:
        json.dump(transformed_data, f, indent=4)

    joined_data = join_data()
    with open(configs.master_loc, "w") as f:
        json.dump(joined_data, f, indent=4)
        
    